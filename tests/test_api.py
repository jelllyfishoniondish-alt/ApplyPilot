import os
import unittest
from unittest.mock import patch

try:
    from fastapi.testclient import TestClient

    from applypilot.api import app, jobs_store
except ModuleNotFoundError:
    TestClient = None
    app = None
    jobs_store = None


@unittest.skipIf(TestClient is None, "FastAPI is not installed")
class ApplyPilotApiTest(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict(os.environ, {}, clear=True)
        self.env_patcher.start()
        jobs_store.clear()
        self.client = TestClient(app)

    def tearDown(self):
        self.env_patcher.stop()

    def test_analyze_job(self):
        response = self.client.post(
            "/analyze-job",
            json={
                "profile": {
                    "user_id": "user-1",
                    "headline": "Backend engineer",
                    "skills": ["Python"],
                    "evidence": ["Built APIs"],
                },
                "job": {
                    "company": "Acme",
                    "title": "Agent Engineer",
                    "source_url": "https://example.com/acme-agent",
                    "description": "Build agents",
                    "required_skills": ["Python", "MongoDB"],
                },
            },
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["fit"]["score"], 50)
        self.assertEqual(body["fit"]["missing_skills"], ["MongoDB"])
        self.assertEqual(body["analysis_source"], "local_fallback")
        self.assertEqual(body["job"]["description"], "Build agents")

    def test_analyze_job_can_fetch_url_description(self):
        with patch(
            "applypilot.api.fetch_job_description",
            return_value="Python MongoDB backend engineer role",
        ):
            response = self.client.post(
                "/analyze-job",
                json={
                    "profile": {
                        "user_id": "user-1",
                        "headline": "Backend engineer",
                        "skills": ["Python"],
                        "evidence": ["Built APIs"],
                    },
                    "job": {
                        "company": "Acme",
                        "title": "Agent Engineer",
                        "source_url": "https://example.com/job",
                        "required_skills": ["Python", "MongoDB"],
                    },
                },
            )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["analysis_source"], "local_fallback")
        self.assertEqual(body["job"]["description"], "Python MongoDB backend engineer role")
        self.assertEqual(body["fit"]["missing_skills"], ["MongoDB"])

    def test_create_and_list_jobs(self):
        create_response = self.client.post(
            "/jobs",
            json={
                "company": "Acme",
                "title": "Agent Engineer",
                "required_skills": ["Python"],
            },
        )
        list_response = self.client.get("/jobs")

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()["jobs"]), 1)
        self.assertEqual(list_response.json()["jobs"][0]["company"], "Acme")

    def test_serves_frontend_routes(self):
        home_response = self.client.get("/")
        dashboard_response = self.client.get("/dashboard")

        self.assertEqual(home_response.status_code, 200)
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertIn("ApplyPilot", home_response.text)
        self.assertIn("data-preset=\"targetRoles\"", home_response.text)
        self.assertIn("data-preset=\"degreeLevels\"", home_response.text)
        self.assertIn("data-preset=\"locations\"", home_response.text)
        self.assertIn("Saved jobs", dashboard_response.text)


if __name__ == "__main__":
    unittest.main()
