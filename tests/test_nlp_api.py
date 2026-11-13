import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("backend"))

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.nlp_lab import router

test_app = FastAPI()
test_app.include_router(router, prefix="/api/v1")

class TestNLPLabAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(test_app)

    def test_overview_endpoint(self):
        response = self.client.get("/api/v1/nlp-lab/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["status"], "OPERATIONAL")

    def test_classify_endpoint(self):
        payload = {"query": "How many days of maternity leave are provided?"}
        response = self.client.post("/api/v1/nlp-lab/classify", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["intent"], "Leave Policy")

    def test_extract_entities_endpoint(self):
        payload = {"text": "Employees get 18 days of Earned Annual Leave per financial year at DSPAMC."}
        response = self.client.post("/api/v1/nlp-lab/extract-entities", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        labels = [e["label"] for e in data["data"]["entities"]]
        self.assertIn("DURATION", labels)
        self.assertIn("LEAVE_TYPE", labels)

    def test_retrieve_endpoint(self):
        payload = {"query": "How to apply for leave in PeoplePulse?", "mode": "hybrid", "alpha": 0.5, "limit": 3}
        response = self.client.post("/api/v1/nlp-lab/retrieve", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertGreater(len(data["data"]["results"]), 0)

    def test_benchmark_endpoint(self):
        response = self.client.get("/api/v1/nlp-lab/benchmark")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("retrieval", data["data"])
        self.assertIn("classification", data["data"])
        self.assertIn("ner", data["data"])

if __name__ == "__main__":
    unittest.main()
