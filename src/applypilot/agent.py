"""Core ApplyPilot workflow."""

from __future__ import annotations

from .models import (
    ApplicationPlan,
    ApplicationStatus,
    FitAssessment,
    JobPosting,
    UserProfile,
)
from .tools import MongoMcpPlanner


class ApplyPilotAgent:
    """Reference implementation of the ApplyPilot planning workflow."""

    def __init__(self, mcp_planner: MongoMcpPlanner | None = None) -> None:
        self._mcp_planner = mcp_planner or MongoMcpPlanner()

    def create_application_plan(
        self,
        profile: UserProfile,
        job: JobPosting,
    ) -> ApplicationPlan:
        fit = self._assess_fit(profile, job)
        status = ApplicationStatus.PLANNED
        steps = self._build_steps(fit)
        approvals = (
            "Store this job and application plan in MongoDB",
            "Use approved profile facts to draft tailored materials",
            "Mark the application as submitted only after user confirmation",
        )
        mcp_operations = self._mcp_planner.plan_application_upsert(
            profile=profile,
            job=job,
            status=status,
            fit_score=fit.score,
        )

        return ApplicationPlan(
            user_id=profile.user_id,
            company=job.company,
            title=job.title,
            status=status,
            fit=fit,
            steps=steps,
            approval_required=approvals,
            mcp_operations=mcp_operations,
        )

    def _assess_fit(self, profile: UserProfile, job: JobPosting) -> FitAssessment:
        profile_skills = {skill.lower() for skill in profile.skills}
        required = {skill.lower(): skill for skill in job.required_skills}

        matched = tuple(
            original for normalized, original in required.items() if normalized in profile_skills
        )
        missing = tuple(
            original for normalized, original in required.items() if normalized not in profile_skills
        )
        score = round((len(matched) / max(len(required), 1)) * 100)

        risks: list[str] = []
        if missing:
            risks.append("Some required skills are not present in the approved profile.")
        if profile.constraints:
            risks.append("User constraints must be checked before submission.")

        return FitAssessment(
            score=score,
            matched_skills=matched,
            missing_skills=missing,
            risks=tuple(risks),
        )

    @staticmethod
    def _build_steps(fit: FitAssessment) -> tuple[str, ...]:
        steps = [
            "Confirm role, company, deadline, and source URL.",
            "Map approved profile evidence to the role requirements.",
            "Draft resume changes using only confirmed facts.",
            "Draft a concise cover-letter outline.",
            "Create a follow-up reminder after submission.",
        ]

        if fit.missing_skills:
            steps.insert(
                2,
                "Ask the user for evidence or alternatives for missing required skills.",
            )

        return tuple(steps)
