import unittest

from applypilot import ApplyPilotAgent, JobPosting, UserProfile


class ApplyPilotAgentTest(unittest.TestCase):
    def test_creates_plan_with_mongodb_mcp_operations(self):
        profile = UserProfile(
            user_id="user-1",
            headline="Backend engineer",
            skills=("Python", "MongoDB"),
            evidence=("Built APIs",),
        )
        job = JobPosting(
            company="Acme",
            title="Agent Engineer",
            source_url="https://example.com/acme-agent",
            description="Build agents",
            required_skills=("Python", "MongoDB", "Google Cloud"),
        )

        plan = ApplyPilotAgent().create_application_plan(profile, job)

        self.assertEqual(plan.company, "Acme")
        self.assertEqual(plan.fit.score, 67)
        self.assertEqual(plan.fit.missing_skills, ("Google Cloud",))
        self.assertEqual(len(plan.mcp_operations), 3)
        self.assertEqual(plan.mcp_operations[0]["collection"], "jobs")
        self.assertEqual(plan.mcp_operations[1]["collection"], "applications")
        self.assertEqual(plan.mcp_operations[2]["collection"], "events")

    def test_full_match_has_no_missing_skill_risk(self):
        profile = UserProfile(
            user_id="user-2",
            headline="AI engineer",
            skills=("Python", "MongoDB", "Google Cloud"),
            evidence=("Shipped cloud services",),
        )
        job = JobPosting(
            company="Example",
            title="Cloud Agent Builder",
            source_url="https://example.com/cloud-agent-builder",
            description="Build cloud agents",
            required_skills=("Python", "MongoDB", "Google Cloud"),
        )

        plan = ApplyPilotAgent().create_application_plan(profile, job)

        self.assertEqual(plan.fit.score, 100)
        self.assertEqual(plan.fit.missing_skills, ())
        self.assertNotIn(
            "Some required skills are not present in the approved profile.",
            plan.fit.risks,
        )


if __name__ == "__main__":
    unittest.main()
