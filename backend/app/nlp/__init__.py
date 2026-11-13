"""
NLP Laboratory Module for DSP KnowledgeHub AI.
Provides Intent Classification, Hybrid Retrieval, NER, and Benchmark Evaluation.
"""

from app.nlp.intent_classifier import IntentClassifier, get_intent_classifier
from app.nlp.hybrid_retriever import HybridRetriever, get_hybrid_retriever
from app.nlp.ner_extractor import HREntityExtractor, get_ner_extractor
from app.nlp.evaluator import NLPEvaluationEngine, get_evaluation_engine

__all__ = [
    "IntentClassifier",
    "get_intent_classifier",
    "HybridRetriever",
    "get_hybrid_retriever",
    "HREntityExtractor",
    "get_ner_extractor",
    "NLPEvaluationEngine",
    "get_evaluation_engine",
]
