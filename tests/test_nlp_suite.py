import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("backend"))

from app.nlp.intent_classifier import get_intent_classifier
from app.nlp.hybrid_retriever import get_hybrid_retriever
from app.nlp.ner_extractor import get_ner_extractor
from app.nlp.evaluator import get_evaluation_engine

class TestNLPSuite(unittest.TestCase):
    def test_01_intent_classifier(self):
        clf = get_intent_classifier()
        self.assertTrue(clf.is_trained)
        self.assertIn("svm", clf.evaluation_results["models"])
        self.assertIn("naive_bayes", clf.evaluation_results["models"])

        # Test query routing
        p1 = clf.predict("How many days of casual leave do I get?")
        self.assertEqual(p1["intent"], "Leave Policy")

        p2 = clf.predict("What is the SAP Concur hotel per diem?")
        self.assertEqual(p2["intent"], "Reimbursement")

        p3 = clf.predict("Who approves my IT access ticket in ServiceHub?")
        self.assertEqual(p3["intent"], "Approval Workflow")

        p4 = clf.predict("Where is Day 1 new hire induction held?")
        self.assertEqual(p4["intent"], "Employment Policy")

    def test_02_hybrid_retriever(self):
        ret = get_hybrid_retriever()
        self.assertGreater(len(ret.chunks), 0)

        # Hybrid search
        res = ret.search_hybrid("Earned annual leave balance cap", alpha=0.5, limit=3)
        self.assertGreater(len(res), 0)
        top = res[0]
        self.assertEqual(top["chunk_id"], "DSP-HR-001_s1")
        self.assertIn("hybrid_score", top)
        self.assertIn("tfidf_score", top)
        self.assertIn("semantic_score", top)

    def test_03_ner_extractor(self):
        extractor = get_ner_extractor()
        text = "Employees receive 18 days of Earned Annual Leave per financial year, and 26 weeks of Maternity Leave."
        entities = extractor.extract_entities(text)
        labels = {e["label"]: e["text"] for e in entities}

        self.assertIn("LEAVE_TYPE", labels)
        self.assertIn("DURATION", labels)
        self.assertIn("ELIGIBILITY_PERIOD", labels)

    def test_04_evaluation_engine(self):
        engine = get_evaluation_engine()
        results = engine.evaluate_all(force_refresh=False)
        self.assertIn("retrieval", results)
        self.assertIn("classification", results)
        self.assertIn("ner", results)
        self.assertGreater(results["summary"]["hybrid_mrr"], 0.7)
        self.assertGreater(results["ner"]["precision"], 0.0)

if __name__ == "__main__":
    unittest.main()

