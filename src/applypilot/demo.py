"""Run a small ApplyPilot planning demo."""

from __future__ import annotations

import json

from .agent import ApplyPilotAgent
from .models import JobPosting, UserProfile


def main() -> None:
    profile = UserProfile(
        user_id="demo-user",
        headline="Data and AI engineering graduate student",
        skills=("Python", "MongoDB", "Machine Learning", "FastAPI", "Google Cloud"),
        evidence=(
            "Built ML prediction pipelines",
            "Created data-backed dashboards",
            "Deployed Python services",
        ),
        constraints=("Requires visa-aware application tracking",),
    )
    job = JobPosting(
        company="Northstar AI",
        title="AI Platform Intern",
        source_url="https://example.com/jobs/ai-platform-intern",
        description="Build agentic AI workflows backed by operational data stores.",
        required_skills=("Python", "MongoDB", "Google Cloud", "Agentic AI"),
        nice_to_have_skills=("MCP", "Vertex AI"),
    )

    plan = ApplyPilotAgent().create_application_plan(profile, job)
    print(json.dumps(_to_json(plan), indent=2))


def _to_json(value):
    if hasattr(value, "__dataclass_fields__"):
        return {key: _to_json(getattr(value, key)) for key in value.__dataclass_fields__}
    if isinstance(value, tuple):
        return [_to_json(item) for item in value]
    if hasattr(value, "value"):
        return value.value
    return value


if __name__ == "__main__":
    main()
