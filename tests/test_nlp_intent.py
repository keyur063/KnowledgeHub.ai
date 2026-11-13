import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("backend"))

from app.nlp.intent_classifier import IntentClassifier, get_intent_classifier

class TestIntentClassifier(unittest.TestCase):
    def test_training_and_evaluation(self):
        clf = IntentClassifier()
        results = clf.train_and_evaluate()
        self.assertEqual(results["status"], "success")
        self.assertIn("naive_bayes", results["models"])
        self.assertIn("svm", results["models"])
        self.assertGreater(results["models"]["svm"]["accuracy"], 0.6)
        self.assertGreater(results["models"]["naive_bayes"]["accuracy"], 0.6)
        self.assertEqual(len(results["models"]["svm"]["confusion_matrix"]["matrix"]), 4)

    def test_predictions(self):
        clf = get_intent_classifier()
        pred_leave = clf.predict("How many days of earned leave do I get per year?")
        self.assertEqual(pred_leave["intent"], "Leave Policy")
        self.assertGreater(pred_leave["confidence"], 0.5)

        pred_reimb = clf.predict("What is the daily per diem hotel allowance for Mumbai?")
        self.assertEqual(pred_reimb["intent"], "Reimbursement")
        self.assertGreater(pred_reimb["confidence"], 0.5)

        pred_approval = clf.predict("What is the manager approval SLA for leave?")
        self.assertEqual(pred_approval["intent"], "Approval Workflow")
        self.assertGreater(pred_approval["confidence"], 0.5)

        pred_employment = clf.predict("Where do new joiners report on Day 1 for induction?")
        self.assertEqual(pred_employment["intent"], "Employment Policy")
        self.assertGreater(pred_employment["confidence"], 0.5)

if __name__ == "__main__":
    unittest.main()
