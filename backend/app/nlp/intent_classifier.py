"""
Query Intent Classification Module for DSP KnowledgeHub AI.

Provides TF-IDF feature extraction, text preprocessing, model training,
and evaluation comparing Multinomial Naive Bayes (MultinomialNB) and Linear SVM (LinearSVC).
Routes employee HR and enterprise inquiries to designated policy domains.
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

logger = logging.getLogger(__name__)

# Default dataset path
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "nlp"
INTENT_DATASET_FILE = DATA_DIR / "intent_dataset.json"


def clean_text(text: str) -> str:
    """
    Standard text normalization and preprocessing for queries.
    - Lowers casing
    - Normalizes currency and numeric symbols
    - Strips non-alphanumeric punctuation while keeping hyphens in compound words
    - Collapses multiple whitespaces
    """
    if not text:
        return ""
    text = text.lower().strip()
    # Normalize currency references
    text = re.sub(r"[₹$€£]", " currency ", text)
    # Replace punctuation with spaces, keeping standard hyphens in compound words like nism-series
    text = re.sub(r"[^\w\s\-]", " ", text)
    # Collapse extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


class IntentClassifier:
    """
    Intent Classifier for DSP KnowledgeHub AI.
    Routes queries to 'Leave Policy', 'Reimbursement', 'Approval Workflow', 'Employment Policy'.
    """

    def __init__(self, dataset_path: Optional[str] = None):
        self.dataset_path = Path(dataset_path) if dataset_path else INTENT_DATASET_FILE
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.nb_model: Optional[MultinomialNB] = None
        self.svm_model: Optional[LinearSVC] = None
        self.calibrated_svm: Optional[CalibratedClassifierCV] = None
        self.classes: List[str] = []
        self.is_trained: bool = False
        self.best_model_name: str = "svm"
        self.evaluation_results: Optional[Dict[str, Any]] = None

    def load_dataset(self) -> Tuple[List[str], List[str]]:
        """Load labeled query examples from the JSON dataset."""
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Intent dataset not found at {self.dataset_path}")

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        queries = [item["query"] for item in data]
        labels = [item.get("category") or item.get("intent") for item in data]
        return queries, labels

    def train_and_evaluate(
        self,
        test_size: float = 0.25,
        random_state: int = 42
    ) -> Dict[str, Any]:
        """
        Preprocesses queries, extracts TF-IDF features, trains both MultinomialNB
        and LinearSVC models, and computes comparative evaluation metrics:
        Accuracy, Precision, Recall, F1-score, Confusion Matrix, and Per-class metrics.
        """
        queries, labels = self.load_dataset()
        self.classes = sorted(list(set(labels)))

        # Clean raw text
        cleaned_queries = [clean_text(q) for q in queries]

        # Stratified train-test split for reproducible evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            cleaned_queries,
            labels,
            test_size=test_size,
            random_state=random_state,
            stratify=labels
        )

        # 1. Feature Extraction: TF-IDF with unigrams and bigrams
        eval_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
            min_df=1
        )
        X_train_tfidf = eval_vectorizer.fit_transform(X_train)
        X_test_tfidf = eval_vectorizer.transform(X_test)

        # 2. Train Multinomial Naive Bayes
        nb = MultinomialNB(alpha=0.2)
        nb.fit(X_train_tfidf, y_train)
        nb_pred = nb.predict(X_test_tfidf)

        # 3. Train Linear Support Vector Classifier (SVM)
        svm = LinearSVC(C=1.0, random_state=random_state, max_iter=3000)
        svm.fit(X_train_tfidf, y_train)
        svm_pred = svm.predict(X_test_tfidf)

        # Calculate metrics for Naive Bayes
        nb_metrics = self._calculate_model_metrics(y_test, nb_pred, self.classes)

        # Calculate metrics for Linear SVM
        svm_metrics = self._calculate_model_metrics(y_test, svm_pred, self.classes)

        # Determine winner
        best_model = "svm" if svm_metrics["f1_score"] >= nb_metrics["f1_score"] else "naive_bayes"
        self.best_model_name = best_model

        # 4. Now fit final models on the entire dataset for production inference
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
            min_df=1
        )
        X_all_tfidf = self.vectorizer.fit_transform(cleaned_queries)

        self.nb_model = MultinomialNB(alpha=0.2)
        self.nb_model.fit(X_all_tfidf, labels)

        self.svm_model = LinearSVC(C=1.0, random_state=random_state, max_iter=3000)
        self.svm_model.fit(X_all_tfidf, labels)

        # Calibrated SVM for reliable confidence/probabilities
        self.calibrated_svm = CalibratedClassifierCV(
            LinearSVC(C=1.0, random_state=random_state, max_iter=3000),
            cv=3
        )
        self.calibrated_svm.fit(X_all_tfidf, labels)

        self.is_trained = True

        comparison_summary = (
            f"LinearSVC achieved an F1-score of {svm_metrics['f1_score']:.4f} "
            f"(Accuracy {svm_metrics['accuracy']:.4f}) compared to MultinomialNB's F1-score of "
            f"{nb_metrics['f1_score']:.4f} (Accuracy {nb_metrics['accuracy']:.4f}). "
            f"{'LinearSVC' if best_model == 'svm' else 'MultinomialNB'} selected as primary classifier."
        )

        results = {
            "status": "success",
            "dataset_info": {
                "total_samples": len(queries),
                "train_samples": len(X_train),
                "test_samples": len(X_test),
                "classes": self.classes,
                "vocabulary_size": len(self.vectorizer.vocabulary_)
            },
            "models": {
                "naive_bayes": {
                    "name": "Multinomial Naive Bayes",
                    **nb_metrics
                },
                "svm": {
                    "name": "Linear Support Vector Machine (LinearSVC)",
                    **svm_metrics
                }
            },
            "best_model": best_model,
            "comparison": {
                "accuracy_diff": round(svm_metrics["accuracy"] - nb_metrics["accuracy"], 4),
                "f1_diff": round(svm_metrics["f1_score"] - nb_metrics["f1_score"], 4),
                "winner": best_model,
                "summary": comparison_summary
            }
        }

        self.evaluation_results = results
        logger.info(f"IntentClassifier trained. Best model: {best_model} (F1: {results['models'][best_model]['f1_score']})")
        return results

    def _calculate_model_metrics(
        self,
        y_true: List[str],
        y_pred: np.ndarray,
        labels: List[str]
    ) -> Dict[str, Any]:
        """Compute standard classification evaluation metrics."""
        acc = float(accuracy_score(y_true, y_pred))
        prec = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
        rec = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
        f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
        macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))

        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred, labels=labels).tolist()

        # Per-class metrics
        report = classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
        per_class = {}
        for label in labels:
            if label in report:
                per_class[label] = {
                    "precision": round(float(report[label]["precision"]), 4),
                    "recall": round(float(report[label]["recall"]), 4),
                    "f1_score": round(float(report[label]["f1-score"]), 4),
                    "support": int(report[label]["support"])
                }

        return {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "macro_f1": round(macro_f1, 4),
            "confusion_matrix": {
                "labels": labels,
                "matrix": cm
            },
            "per_class": per_class
        }

    def predict(
        self,
        query: str,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Predict the HR domain intent for a given user query.
        Returns predicted intent, confidence score, and distribution across all categories.
        """
        if not self.is_trained:
            self.train_and_evaluate()

        cleaned = clean_text(query)
        if not cleaned:
            return {
                "query": query,
                "intent": "General",
                "confidence": 0.0,
                "model_used": model_name or self.best_model_name,
                "probabilities": {cls: 0.0 for cls in self.classes}
            }

        query_vec = self.vectorizer.transform([cleaned])
        chosen_model = (model_name or self.best_model_name).lower()

        if chosen_model in ["naive_bayes", "nb", "multinomialnb"]:
            predicted_class = self.nb_model.predict(query_vec)[0]
            probs = self.nb_model.predict_proba(query_vec)[0]
            model_key = "naive_bayes"
        else:
            # Use Calibrated LinearSVC
            predicted_class = self.calibrated_svm.predict(query_vec)[0]
            probs = self.calibrated_svm.predict_proba(query_vec)[0]
            model_key = "svm"

        prob_dict = {
            cls: round(float(p), 4)
            for cls, p in zip(self.classes, probs)
        }
        confidence = float(probs[list(self.classes).index(predicted_class)])

        return {
            "query": query,
            "intent": predicted_class,
            "confidence": round(confidence, 4),
            "model_used": model_key,
            "probabilities": prob_dict
        }


# Global Singleton instance
_intent_classifier_instance: Optional[IntentClassifier] = None


def get_intent_classifier() -> IntentClassifier:
    """Obtain or initialize the global IntentClassifier instance."""
    global _intent_classifier_instance
    if _intent_classifier_instance is None:
        _intent_classifier_instance = IntentClassifier()
        _intent_classifier_instance.train_and_evaluate()
    return _intent_classifier_instance

