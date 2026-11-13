"""
Named Entity Recognition (NER) Module for DSP KnowledgeHub AI.

Extracts structured HR and enterprise information from policy documents using spaCy (en_core_web_sm)
augmented with a custom EntityRuler pipeline preceding statistical NER.
Custom Concepts Extracted:
- LEAVE_TYPE (e.g., Annual leave, Earned Leave, Casual Leave, Maternity Leave)
- DURATION (e.g., 18 days, 45 days, 26 weeks, 48 hours, 3 consecutive business days)
- ELIGIBILITY_PERIOD (e.g., 12 months, 6 months, financial year, FY2026-27, Days 15–30)
Standard Concepts Extracted:
- DATE, ORG, MONEY, GPE, TIME, LAW, PRODUCT
"""

import os
import re
import logging
from typing import Dict, Any, List, Optional, Set, Tuple

import spacy
from spacy.pipeline import EntityRuler

logger = logging.getLogger(__name__)

# Entity definitions and friendly descriptions
ENTITY_DESCRIPTIONS = {
    "LEAVE_TYPE": "Authorized HR absence and leave policy category",
    "DURATION": "Specified time span, notice period, or operational SLA",
    "ELIGIBILITY_PERIOD": "Qualifying employment window or statutory timeline",
    "ORG": "Companies, regulatory bodies, and internal software portals",
    "MONEY": "Monetary limits, per diems, lodging allowances, or expenses",
    "DATE": "Absolute or relative dates and statutory calendar milestones",
    "TIME": "Operational cut-offs and daily clock times",
    "GPE": "Geographical locations, cities, and metro tiers",
    "LAW": "Statutory legislation, acts, and regulatory mandates",
    "PRODUCT": "Specialized software systems, terminal keys, or certifications"
}


def create_hr_ner_pipeline(model_name: str = "en_core_web_sm") -> spacy.language.Language:
    """
    Initializes spaCy NLP pipeline and inserts custom EntityRuler BEFORE the statistical NER pipe.
    """
    nlp = spacy.load(model_name)

    # Insert EntityRuler before the default 'ner' pipe so exact domain rules take precedence
    ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})

    patterns = [
        # ─── 1. LEAVE_TYPE Patterns ──────────────────────────────────
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "earned"}, {"LOWER": "annual"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "earned"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "annual"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "annual"}, {"LOWER": "earned"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "casual"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "sick"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "casual/sick"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "maternity"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "paternity"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "bereavement"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "adoption"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "parental"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "compensatory"}, {"LOWER": "off"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "comp"}, {"LOWER": "off"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "sabbatical"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"LOWER": "unpaid"}, {"LOWER": "leave"}]},
        {"label": "LEAVE_TYPE", "pattern": [{"TEXT": {"IN": ["EL", "CL", "SL", "CL/SL"]}}]},

        # ─── 2. DURATION Patterns ─────────────────────────────────────
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["day", "days"]}}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": "consecutive"}, {"LOWER": "days"}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": "consecutive"}, {"LOWER": "business"}, {"LOWER": "days"}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": "working"}, {"LOWER": "days"}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": "calendar"}, {"LOWER": "days"}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": "business"}, {"LOWER": "days"}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["week", "weeks"]}}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["month", "months"]}}]},
        {"label": "DURATION", "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["hour", "hours"]}}]},
        {"label": "DURATION", "pattern": [{"TEXT": {"REGEX": r"^\d+-hour$"}}]},
        {"label": "DURATION", "pattern": [{"TEXT": {"REGEX": r"^\d+-calendar-day$"}}]},
        {"label": "DURATION", "pattern": [{"TEXT": {"REGEX": r"^\d+-day$"}}]},
        {"label": "DURATION", "pattern": [{"TEXT": {"REGEX": r"^\d+-working-day$"}}]},

        # ─── 3. ELIGIBILITY_PERIOD Patterns ───────────────────────────
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"LOWER": "financial"}, {"LOWER": "year"}]},
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"LOWER": "calendar"}, {"LOWER": "year"}]},
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"TEXT": {"REGEX": r"^[Ff][Yy]\d{4}(-\d{2,4})?$"}}]},
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"LOWER": "quarterly"}, {"LOWER": "basis"}]},
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"LOWER": "probation"}, {"LOWER": "period"}]},
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"LOWER": "days"}, {"TEXT": {"REGEX": r"^\d+[–-]\d+$"}}]},
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"TEXT": "6"}, {"LOWER": "months"}]},
        {"label": "ELIGIBILITY_PERIOD", "pattern": [{"TEXT": "12"}, {"LOWER": "months"}]},

        # ─── 4. Standard Entity Enhancements (ORG, MONEY, LAW, PRODUCT)
        {"label": "ORG", "pattern": [{"TEXT": {"IN": ["DSPAMC", "DSP", "AMFI", "SEBI", "CCIL", "NSCCL", "CRISIL", "ICRA"]}}]},
        {"label": "ORG", "pattern": [{"LOWER": "peoplepulse"}]},
        {"label": "ORG", "pattern": [{"LOWER": "servicehub"}]},
        {"label": "ORG", "pattern": [{"LOWER": "compliancedesk"}]},
        {"label": "ORG", "pattern": [{"LOWER": "sap"}, {"LOWER": "concur"}]},
        {"label": "ORG", "pattern": [{"LOWER": "servicenow"}]},
        {"label": "LAW", "pattern": [{"LOWER": "maternity"}, {"LOWER": "benefit"}, {"LOWER": "act"}]},
        {"label": "PRODUCT", "pattern": [{"TEXT": {"REGEX": r"^[Nn][Ii][Ss][Mm]-Series-[A-Za-z0-9\-]+$"}}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "bloomberg"}, {"LOWER": "terminal"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "refinitiv"}, {"LOWER": "eikon"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "qdrant"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "cisco"}, {"LOWER": "anyconnect"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "globalprotect"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "microsoft"}, {"LOWER": "authenticator"}]},
        {"label": "PRODUCT", "pattern": [{"LOWER": "yubikey"}]},
        {"label": "MONEY", "pattern": [{"TEXT": {"REGEX": r"^₹[\d,]+(/[a-zA-Z]+)?$"}}]}
    ]

    ruler.add_patterns(patterns)
    return nlp


class HREntityExtractor:
    """
    High-level NER extraction service for HR policy documents and queries.
    """

    def __init__(self, model_name: str = "en_core_web_sm"):
        self.nlp = create_hr_ner_pipeline(model_name)

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract and structure all detected entities from arbitrary text."""
        if not text or not text.strip():
            return []

        doc = self.nlp(text)
        entities = []
        seen = set()

        for ent in doc.ents:
            key = (ent.text.strip(), ent.label_)
            if key not in seen:
                seen.add(key)
                desc = ENTITY_DESCRIPTIONS.get(ent.label_)
                if not desc:
                    try:
                        desc = spacy.explain(ent.label_) or ent.label_
                    except Exception:
                        desc = ent.label_
                entities.append({
                    "text": ent.text.strip(),
                    "label": ent.label_,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                    "description": desc
                })

        return entities

    def extract_entities_by_type(self, text: str) -> Dict[str, List[str]]:
        """Return a mapping of entity label to list of extracted entity texts."""
        entities = self.extract_entities(text)
        grouped: Dict[str, List[str]] = {}
        for ent in entities:
            label = ent["label"]
            grouped.setdefault(label, []).append(ent["text"])
        return grouped

    def evaluate_benchmark(
        self,
        benchmark_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluate NER extraction precision, recall, and F1 against annotated benchmark dataset.
        Matching considers entity text (case-insensitive substring or match) and entity label.
        """
        total_expected = 0
        total_extracted = 0
        true_positives = 0

        per_label_stats: Dict[str, Dict[str, int]] = {}

        for item in benchmark_items:
            query = item.get("question") or item.get("query", "")
            expected_list = item.get("expected_entities", [])
            total_expected += len(expected_list)

            extracted = self.extract_entities(query)
            total_extracted += len(extracted)

            for exp in expected_list:
                exp_text = exp["text"].lower().strip()
                exp_label = exp["label"]

                per_label_stats.setdefault(exp_label, {"tp": 0, "fp": 0, "fn": 0, "expected": 0})
                per_label_stats[exp_label]["expected"] += 1

                # Check if extracted contains a match
                matched = False
                for ext in extracted:
                    ext_text = ext["text"].lower().strip()
                    ext_label = ext["label"]

                    # Accept exact match or containment with matching label
                    if (ext_label == exp_label or (exp_label in ["DATE", "DURATION", "ELIGIBILITY_PERIOD"] and ext_label in ["DATE", "DURATION", "ELIGIBILITY_PERIOD"])) and (exp_text in ext_text or ext_text in exp_text):
                        matched = True
                        break

                if matched:
                    true_positives += 1
                    per_label_stats[exp_label]["tp"] += 1
                else:
                    per_label_stats[exp_label]["fn"] += 1

        precision = (true_positives / total_extracted) if total_extracted > 0 else 0.0
        recall = (true_positives / total_expected) if total_expected > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

        label_breakdown = {}
        for lbl, stats in per_label_stats.items():
            l_tp = stats["tp"]
            l_exp = stats["expected"]
            l_recall = (l_tp / l_exp) if l_exp > 0 else 0.0
            label_breakdown[lbl] = {
                "expected": l_exp,
                "true_positives": l_tp,
                "recall": round(l_recall, 4)
            }

        return {
            "total_benchmark_questions": len(benchmark_items),
            "total_expected_entities": total_expected,
            "total_extracted_entities": total_extracted,
            "true_positives": true_positives,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "accuracy": round(recall, 4),  # Entity recall against ground-truth
            "label_breakdown": label_breakdown
        }


# Global Singleton instance
_hr_ner_instance: Optional[HREntityExtractor] = None


def get_ner_extractor() -> HREntityExtractor:
    """Obtain or initialize the global HREntityExtractor instance."""
    global _hr_ner_instance
    if _hr_ner_instance is None:
        _hr_ner_instance = HREntityExtractor()
    return _hr_ner_instance
