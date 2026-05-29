import os
import unittest
from unittest.mock import patch

from applypilot.gemini import GeminiAnalyzer, GeminiAnalyzerError
from applypilot.models import JobPosting, UserProfile


class GeminiAnalyzerTest(unittest.TestCase):
    def test_requires_vertex_configuration(self):
        analyzer = GeminiAnalyzer()
        profile = UserProfile(
            user_id="user-1",
            headline="Engineer",
            skills=("Python",),
            evidence=(),
        )
        job = JobPosting(
            company="Acme",
            title="Engineer",
            source_url="",
            description="Python",
            required_skills=("Python",),
        )

        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(GeminiAnalyzerError):
                analyzer.analyze(profile, job)

    def test_reports_configuration_when_env_is_present(self):
        with patch.dict(
            os.environ,
            {
                "GOOGLE_CLOUD_PROJECT": "project-1",
                "GOOGLE_CLOUD_LOCATION": "global",
                "GOOGLE_GENAI_USE_VERTEXAI": "True",
            },
            clear=True,
        ):
            self.assertTrue(GeminiAnalyzer().is_configured())

    def test_supports_api_key_configuration(self):
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"}, clear=True):
            self.assertTrue(GeminiAnalyzer().is_configured())


if __name__ == "__main__":
    unittest.main()
