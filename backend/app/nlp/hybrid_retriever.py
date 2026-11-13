"""
Hybrid Information Retrieval Module for DSP KnowledgeHub AI.

Combines:
1. Lexical / Keyword matching via Scikit-learn TF-IDF + Cosine Similarity (S_TF-IDF)
2. Dense Semantic retrieval via SentenceTransformer ('all-MiniLM-L6-v2') (S_semantic)
3. Convex Hybrid Fusion: Score = alpha * S_TF-IDF + (1 - alpha) * S_semantic
4. Intent-guided category filtering integrated with Query Intent Classification.
"""

import os
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

# Ensure offline loading for cached HuggingFace models
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.knowledge_service import DSPAMC_DOCUMENTS
from app.nlp.intent_classifier import clean_text, get_intent_classifier

logger = logging.getLogger(__name__)

# Intent-to-Document Category Mapping
INTENT_TO_DOC_CATEGORIES = {
    "Leave Policy": ["HR"],
    "Reimbursement": ["Finance"],
    "Approval Workflow": ["HR", "IT", "Finance", "Compliance", "Operations"],
    "Employment Policy": ["HR", "Compliance", "IT"],
}


class HybridRetriever:
    """
    Hybrid Retriever combining TF-IDF and SentenceTransformer representations.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        documents: Optional[List[Dict[str, Any]]] = None
    ):
        self.model_name = model_name
        self.raw_documents = documents if documents is not None else DSPAMC_DOCUMENTS
        self.chunks: List[Dict[str, Any]] = []
        self.chunk_texts: List[str] = []

        # Models & Vector Representations
        self.tfidf_vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix: Optional[np.ndarray] = None
        self.semantic_model = None
        self.chunk_embeddings: Optional[np.ndarray] = None

        self._build_chunks()
        self._initialize_index()

    def _build_chunks(self):
        """Chunk all approved documents into retrieval passages with unique chunk IDs."""
        self.chunks = []
        for doc in self.raw_documents:
            doc_id = doc["id"]
            doc_title = doc["title"]
            category = doc["category"]
            department = doc.get("department", "")

            sections = doc.get("sections", [])
            for idx, sec in enumerate(sections):
                chunk_id = f"{doc_id}_s{idx + 1}"
                section_name = sec.get("section", f"Section {idx + 1}")
                page = sec.get("page", 1)
                content = sec.get("content", "")
                keywords = " ".join(sec.get("keywords", []))

                # Rich chunk representation for TF-IDF and dense embeddings
                text_to_index = (
                    f"{doc_title} ({category} - {department}). {section_name}. "
                    f"Keywords: {keywords}. {content}"
                )

                self.chunks.append({
                    "chunk_id": chunk_id,
                    "document_id": doc_id,
                    "document_title": doc_title,
                    "category": category,
                    "department": department,
                    "section": section_name,
                    "page": page,
                    "content": content,
                    "text_to_index": text_to_index,
                })

        self.chunk_texts = [c["text_to_index"] for c in self.chunks]
        logger.info(f"Built {len(self.chunks)} chunk passages across {len(self.raw_documents)} documents.")

    def _initialize_index(self):
        """Build TF-IDF vocabulary matrix and precompute SentenceTransformer embeddings."""
        # 1. TF-IDF Vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
            min_df=1
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.chunk_texts)

        # 2. Check for precomputed chunk embeddings on disk
        cache_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "nlp", "chunk_embeddings.npy")
        if os.path.exists(cache_path):
            try:
                self.chunk_embeddings = np.load(cache_path)
                logger.info(f"Loaded {len(self.chunk_embeddings)} precomputed chunk embeddings from disk.")
            except Exception as e:
                logger.warning(f"Failed to load cached embeddings: {e}")

        # 3. SentenceTransformer Embedding Model (lazy loaded if needed)
        try:
            from sentence_transformers import SentenceTransformer
            self.semantic_model = SentenceTransformer(self.model_name, local_files_only=True)
            if self.chunk_embeddings is None:
                raw_embeddings = self.semantic_model.encode(
                    self.chunk_texts,
                    normalize_embeddings=True,
                    show_progress_bar=False
                )
                self.chunk_embeddings = np.array(raw_embeddings, dtype=np.float32)
                try:
                    np.save(cache_path, self.chunk_embeddings)
                except Exception:
                    pass
            logger.info("SentenceTransformer model successfully initialized.")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer ({e}). Falling back to dense TF-IDF representations.")
            if self.chunk_embeddings is None:
                dense = self.tfidf_matrix.toarray().astype(np.float32)
                norms = np.linalg.norm(dense, axis=1, keepdims=True)
                norms[norms == 0] = 1.0
                self.chunk_embeddings = dense / norms

    def _get_candidate_indices(self, category_filter: Optional[str] = None) -> List[int]:
        """Filter chunk candidate indices by document category or mapped intent."""
        if not category_filter:
            return list(range(len(self.chunks)))

        # Normalize filter
        filter_lower = category_filter.strip().lower()

        # Check if filter matches intent mapping
        target_categories = None
        for intent_key, mapped_cats in INTENT_TO_DOC_CATEGORIES.items():
            if intent_key.lower() == filter_lower:
                target_categories = [c.lower() for c in mapped_cats]
                break

        if target_categories is None:
            target_categories = [filter_lower]

        indices = [
            i for i, chunk in enumerate(self.chunks)
            if chunk["category"].lower() in target_categories
        ]

        # If filtering is too restrictive and returns no chunks, fallback to all chunks
        return indices if indices else list(range(len(self.chunks)))

    def search_tfidf(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Keyword-only retrieval using TF-IDF and Cosine Similarity."""
        q_cleaned = clean_text(query)
        q_vec = self.tfidf_vectorizer.transform([q_cleaned])
        sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        candidates = self._get_candidate_indices(category)
        scored = [(i, float(sims[i])) for i in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)

        results = []
        for rank, (idx, score) in enumerate(scored[:limit], start=1):
            chunk = self.chunks[idx]
            results.append({
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "document_title": chunk["document_title"],
                "section": chunk["section"],
                "page": chunk["page"],
                "content": chunk["content"],
                "category": chunk["category"],
                "score": round(score, 4),
                "retrieval_mode": "tfidf"
            })
        return results

    def search_semantic(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Dense semantic retrieval using SentenceTransformer."""
        if self.semantic_model is not None:
            q_emb = self.semantic_model.encode([query], normalize_embeddings=True)[0]
        else:
            q_vec = self.tfidf_vectorizer.transform([clean_text(query)]).toarray()[0]
            norm = np.linalg.norm(q_vec)
            q_emb = q_vec / (norm if norm > 0 else 1.0)

        # Dot product with pre-normalized chunk embeddings = cosine similarity
        sims = np.dot(self.chunk_embeddings, q_emb)
        # Normalize/clip to [0, 1] range
        sims = np.clip(sims, 0.0, 1.0)

        candidates = self._get_candidate_indices(category)
        scored = [(i, float(sims[i])) for i in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)

        results = []
        for rank, (idx, score) in enumerate(scored[:limit], start=1):
            chunk = self.chunks[idx]
            results.append({
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "document_title": chunk["document_title"],
                "section": chunk["section"],
                "page": chunk["page"],
                "content": chunk["content"],
                "category": chunk["category"],
                "score": round(score, 4),
                "retrieval_mode": "semantic"
            })
        return results

    def search_hybrid(
        self,
        query: str,
        alpha: float = 0.5,
        limit: int = 5,
        category: Optional[str] = None,
        auto_filter_intent: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Hybrid Information Retrieval combining TF-IDF and Semantic scores:
        Score = alpha * S_TF-IDF + (1 - alpha) * S_semantic
        Supports filtering by predicted intent category from Step 2.
        """
        alpha = max(0.0, min(1.0, float(alpha)))
        predicted_intent = None

        if auto_filter_intent and not category:
            classifier = get_intent_classifier()
            pred = classifier.predict(query)
            if pred["confidence"] >= 0.40:
                category = pred["intent"]
                predicted_intent = pred["intent"]

        # 1. TF-IDF Similarity
        q_cleaned = clean_text(query)
        q_vec = self.tfidf_vectorizer.transform([q_cleaned])
        tfidf_sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        # 2. Semantic Similarity
        if self.semantic_model is not None:
            q_emb = self.semantic_model.encode([query], normalize_embeddings=True)[0]
        else:
            q_vec_dense = q_vec.toarray()[0]
            norm = np.linalg.norm(q_vec_dense)
            q_emb = q_vec_dense / (norm if norm > 0 else 1.0)

        sem_sims = np.dot(self.chunk_embeddings, q_emb)
        sem_sims = np.clip(sem_sims, 0.0, 1.0)

        # 3. Hybrid Fusion: Score = alpha * S_TF-IDF + (1 - alpha) * S_semantic
        hybrid_scores = (alpha * tfidf_sims) + ((1.0 - alpha) * sem_sims)

        candidates = self._get_candidate_indices(category)
        scored = [
            (
                i,
                float(hybrid_scores[i]),
                float(tfidf_sims[i]),
                float(sem_sims[i])
            )
            for i in candidates
        ]
        scored.sort(key=lambda x: x[1], reverse=True)

        results = []
        for rank, (idx, h_score, tf_score, sem_score) in enumerate(scored[:limit], start=1):
            chunk = self.chunks[idx]
            results.append({
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "document_title": chunk["document_title"],
                "section": chunk["section"],
                "page": chunk["page"],
                "content": chunk["content"],
                "category": chunk["category"],
                "score": round(h_score, 4),
                "hybrid_score": round(h_score, 4),
                "tfidf_score": round(tf_score, 4),
                "semantic_score": round(sem_score, 4),
                "alpha": alpha,
                "filtered_category": category,
                "predicted_intent": predicted_intent,
                "retrieval_mode": "hybrid"
            })
        return results


# Global Singleton instance
_hybrid_retriever_instance: Optional[HybridRetriever] = None


def get_hybrid_retriever() -> HybridRetriever:
    """Obtain or initialize the global HybridRetriever instance."""
    global _hybrid_retriever_instance
    if _hybrid_retriever_instance is None:
        _hybrid_retriever_instance = HybridRetriever()
    return _hybrid_retriever_instance
