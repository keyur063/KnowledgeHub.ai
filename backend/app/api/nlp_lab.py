"""
DSP KnowledgeHub AI — NLP Laboratory API Endpoints.

Provides REST endpoints for:
1. Retrieval, Intent Classification, and NER Benchmark Evaluation (/benchmark)
2. Live Query Intent Prediction with confidence scores (/classify)
3. Hybrid, Semantic, and TF-IDF Retrieval execution (/retrieve)
4. Structured HR Named Entity Extraction (/extract-entities)
5. NLP Lab Engine Overview and telemetry (/overview)
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from fastapi import APIRouter, Query, HTTPException, status

from app.schemas.schemas import APIResponse, ResponseMetadata
from app.nlp.intent_classifier import get_intent_classifier
from app.nlp.hybrid_retriever import get_hybrid_retriever
from app.nlp.ner_extractor import get_ner_extractor
from app.nlp.evaluator import get_evaluation_engine

router = APIRouter(prefix="/nlp-lab", tags=["NLP Laboratory & Evaluation"])


# ─── Pydantic Request Models ──────────────────────────────────────────

class ClassifyRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Query text to classify into HR domain intents")
    model: Optional[str] = Field(None, description="Classifier model to use: 'svm' or 'naive_bayes'")


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    mode: str = Field("hybrid", description="Retrieval mode: 'hybrid', 'tfidf', or 'semantic'")
    alpha: float = Field(0.5, ge=0.0, le=1.0, description="Fusion weight for TF-IDF (1.0 = pure TF-IDF, 0.0 = pure semantic)")
    category: Optional[str] = Field(None, description="Optional category filter (e.g. 'Leave Policy', 'Finance', 'HR')")
    auto_intent: bool = Field(False, description="Automatically infer category using Query Intent Classifier")
    limit: int = Field(5, ge=1, le=20, description="Maximum number of chunks to return")


class ExtractNERRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text passage to extract HR named entities from")


# ─── Endpoints ────────────────────────────────────────────────────────

@router.get("/benchmark", response_model=APIResponse)
async def get_nlp_benchmark(force_refresh: bool = Query(False, description="Force re-evaluation of all benchmark models")):
    """
    Execute and return quantitative evaluation metrics across the ground-truth benchmark:
    - Retrieval: Precision@5, Recall@5, MRR, Latency for TF-IDF vs. Semantic vs. Hybrid
    - Classification: Naive Bayes vs. LinearSVC (Accuracy, F1, Confusion Matrix)
    - Named Entity Recognition: Precision, Recall, F1, Per-entity type stats
    """
    engine = get_evaluation_engine()
    results = engine.evaluate_all(force_refresh=force_refresh)

    return APIResponse(
        success=True,
        data=results,
        metadata=ResponseMetadata(
            timestamp=datetime.now(timezone.utc),
            source="nlp_benchmark_evaluator",
            data_status="LIVE_EVALUATED",
            is_demo=False
        )
    )


@router.post("/classify", response_model=APIResponse)
async def classify_query_intent(request: ClassifyRequest):
    """
    Classify employee inquiry into one of the 4 HR intent categories:
    - Leave Policy
    - Reimbursement
    - Approval Workflow
    - Employment Policy
    """
    classifier = get_intent_classifier()
    prediction = classifier.predict(request.query, model_name=request.model)

    return APIResponse(
        success=True,
        data=prediction,
        metadata=ResponseMetadata(
            timestamp=datetime.now(timezone.utc),
            source="nlp_intent_classifier",
            data_status="LIVE_INFERENCE",
            is_demo=False
        )
    )


@router.post("/retrieve", response_model=APIResponse)
async def search_hybrid_retrieval(request: RetrieveRequest):
    """
    Execute information retrieval using TF-IDF, Dense Semantic, or Hybrid Fusion:
    Score = alpha * S_TF-IDF + (1 - alpha) * S_semantic
    """
    retriever = get_hybrid_retriever()
    mode = request.mode.lower().strip()

    if mode == "tfidf":
        results = retriever.search_tfidf(request.query, limit=request.limit, category=request.category)
    elif mode == "semantic":
        results = retriever.search_semantic(request.query, limit=request.limit, category=request.category)
    else:
        results = retriever.search_hybrid(
            request.query,
            alpha=request.alpha,
            limit=request.limit,
            category=request.category,
            auto_filter_intent=request.auto_intent
        )

    return APIResponse(
        success=True,
        data={
            "query": request.query,
            "mode": mode,
            "alpha": request.alpha,
            "total_results": len(results),
            "results": results
        },
        metadata=ResponseMetadata(
            timestamp=datetime.now(timezone.utc),
            source="nlp_hybrid_retriever",
            data_status="LIVE_RETRIEVAL",
            is_demo=False
        )
    )


@router.post("/extract-entities", response_model=APIResponse)
async def extract_named_entities(request: ExtractNERRequest):
    """
    Extract structured HR concepts (LEAVE_TYPE, DURATION, ELIGIBILITY_PERIOD)
    and standard entities (ORG, MONEY, DATE, TIME) from a text passage.
    """
    extractor = get_ner_extractor()
    entities = extractor.extract_entities(request.text)

    return APIResponse(
        success=True,
        data={
            "text": request.text,
            "entity_count": len(entities),
            "entities": entities
        },
        metadata=ResponseMetadata(
            timestamp=datetime.now(timezone.utc),
            source="nlp_ner_extractor",
            data_status="LIVE_EXTRACTION",
            is_demo=False
        )
    )


@router.get("/overview", response_model=APIResponse)
async def get_nlp_lab_overview():
    """Retrieve operational status and configuration of all NLP lab components."""
    classifier = get_intent_classifier()
    retriever = get_hybrid_retriever()

    return APIResponse(
        success=True,
        data={
            "status": "OPERATIONAL",
            "components": {
                "intent_classifier": {
                    "classes": classifier.classes,
                    "vocabulary_size": len(classifier.vectorizer.vocabulary_) if classifier.vectorizer else 0,
                    "best_model": classifier.best_model_name,
                    "is_trained": classifier.is_trained
                },
                "hybrid_retriever": {
                    "model_name": retriever.model_name,
                    "total_chunks": len(retriever.chunks),
                    "supported_modes": ["tfidf", "semantic", "hybrid"]
                },
                "ner_extractor": {
                    "base_model": "en_core_web_sm",
                    "custom_ruler": True,
                    "custom_entities": ["LEAVE_TYPE", "DURATION", "ELIGIBILITY_PERIOD"]
                }
            }
        },
        metadata=ResponseMetadata(
            timestamp=datetime.now(timezone.utc),
            source="nlp_lab_telemetry",
            data_status="HEALTHY",
            is_demo=False
        )
    )

