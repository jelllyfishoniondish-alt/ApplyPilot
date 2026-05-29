"""Gemini-backed job analysis for ApplyPilot."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

from .models import ApplicationPlan, ApplicationStatus, FitAssessment, JobPosting, UserProfile
from .tools import MongoMcpPlanner


load_dotenv()


class GeminiAnalyzerError(RuntimeError):
    """Raised when Gemini analysis cannot be completed."""


@dataclass(frozen=True)
class GeminiAnalysis:
    plan: ApplicationPlan
    model: str


class GeminiAnalyzer:
    """Analyze job fit with Gemini on Vertex AI."""

    def __init__(
        self,
        model: str | None = None,
        mcp_planner: MongoMcpPlanner | None = None,
    ) -> None:
        self.model = model or os.getenv("APPLYPILOT_GEMINI_MODEL", "gemini-2.5-flash")
        self._mcp_planner = mcp_planner or MongoMcpPlanner()

    def is_configured(self) -> bool:
        has_vertex_config = (
            bool(os.getenv("GOOGLE_CLOUD_PROJECT"))
            and bool(os.getenv("GOOGLE_CLOUD_LOCATION"))
            and _truthy(os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
        )
        return has_vertex_config or bool(_api_key())

    def analyze(self, profile: UserProfile, job: JobPosting) -> GeminiAnalysis:
        if not self.is_configured():
            raise GeminiAnalyzerError("Gemini is not configured for Vertex AI.")

        try:
            from google import genai
            from google.genai.types import HttpOptions
        except ImportError as exc:
            raise GeminiAnalyzerError("google-genai is not installed.") from exc

        try:
            client_kwargs = {"http_options": HttpOptions(api_version="v1")}
            if _api_key():
                client_kwargs["api_key"] = _api_key()

            client = genai.Client(**client_kwargs)
            response = client.models.generate_content(
                model=self.model,
                contents=_build_prompt(profile, job),
                config={
                    "response_mime_type": "application/json",
                    "response_schema": RESPONSE_SCHEMA,
                    # Disable chain-of-thought thinking — not needed for structured
                    # extraction and is the single biggest source of latency on flash.
                    "thinking_config": {"thinking_budget": 0},
                },
            )
            payload = json.loads(response.text or "{}")
            plan = _payload_to_plan(profile, job, payload, self._mcp_planner)
        except Exception as exc:
            raise GeminiAnalyzerError(str(exc)) from exc

        return GeminiAnalysis(plan=plan, model=self.model)


RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "OBJECT",
    "properties": {
        "company": {"type": "STRING"},
        "title": {"type": "STRING"},
        "fit_score": {"type": "INTEGER"},
        "matched_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
        "missing_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
        "risks": {"type": "ARRAY", "items": {"type": "STRING"}},
        "steps": {"type": "ARRAY", "items": {"type": "STRING"}},
    },
    "required": [
        "company",
        "title",
        "fit_score",
        "matched_skills",
        "missing_skills",
        "risks",
        "steps",
    ],
}


_PLACEHOLDER_COMPANY = "unknown company"
_PLACEHOLDER_TITLE = "job posting from url"


def _build_prompt(profile: UserProfile, job: JobPosting) -> str:
    # Only include non-empty profile fields to keep the prompt compact.
    profile_payload: dict = {}
    for key, val in [
        ("headline",        profile.headline),
        ("target_roles",    list(profile.target_roles)),
        ("skills",          list(profile.skills)),
        ("tools",           list(profile.tools)),
        ("evidence",        list(profile.evidence)),
        ("domain_interests",list(profile.domain_interests)),
        ("education",       list(profile.education)),
        ("certifications",  list(profile.certifications)),
        ("constraints",     list(profile.constraints)),
    ]:
        if val and val != []:
            profile_payload[key] = val

    # Truncate the description: the first ~2500 chars hold the key requirements.
    description = job.description[:2500].strip()
    if len(job.description) > 2500:
        description += "\n[truncated]"

    # Omit placeholder company/title so Gemini extracts the real values from description.
    job_payload: dict = {"description": description}
    if job.company.lower() != _PLACEHOLDER_COMPANY:
        job_payload["company"] = job.company
    if job.title.lower() != _PLACEHOLDER_TITLE:
        job_payload["title"] = job.title
    if job.required_skills:
        job_payload["required_skills"] = list(job.required_skills)
    if job.nice_to_have_skills:
        job_payload["nice_to_have_skills"] = list(job.nice_to_have_skills)

    return (
        "You are ApplyPilot. Extract the company name and job title from the description "
        "(return them in the company and title fields). Then score job fit, list "
        "matched/missing skills, flag risks, and give 3-5 concrete next steps. "
        "Use only facts from the profile — no invented skills, dates, or credentials. "
        "Treat competencies, tools, education, and evidence as potential skill matches.\n\n"
        f"PROFILE:{json.dumps(profile_payload, ensure_ascii=False)}\n\n"
        f"JOB:{json.dumps(job_payload, ensure_ascii=False)}"
    )


def _payload_to_plan(
    profile: UserProfile,
    original_job: JobPosting,
    payload: dict[str, Any],
    mcp_planner: MongoMcpPlanner,
) -> ApplicationPlan:
    company = _clean_text(payload.get("company")) or original_job.company
    title = _clean_text(payload.get("title")) or original_job.title
    fit = FitAssessment(
        score=_clamp_score(payload.get("fit_score")),
        matched_skills=tuple(_clean_list(payload.get("matched_skills"))),
        missing_skills=tuple(_clean_list(payload.get("missing_skills"))),
        risks=tuple(_clean_list(payload.get("risks"))),
    )
    steps = tuple(_clean_list(payload.get("steps"))) or (
        "Review the Gemini analysis and confirm application priorities.",
    )
    job = JobPosting(
        company=company,
        title=title,
        source_url=original_job.source_url,
        description=original_job.description,
        required_skills=original_job.required_skills,
        nice_to_have_skills=original_job.nice_to_have_skills,
    )
    mcp_operations = mcp_planner.plan_application_upsert(
        profile=profile,
        job=job,
        status=ApplicationStatus.PLANNED,
        fit_score=fit.score,
    )

    return ApplicationPlan(
        user_id=profile.user_id,
        company=company,
        title=title,
        status=ApplicationStatus.PLANNED,
        fit=fit,
        steps=steps,
        approval_required=(
            "Store this Gemini analysis and application plan in MongoDB",
            "Use approved profile facts to draft tailored materials",
            "Mark the application as submitted only after user confirmation",
        ),
        mcp_operations=mcp_operations,
    )


def _clean_text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _clean_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [text for text in (_clean_text(item) for item in value) if text]


def _clamp_score(value: Any) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError):
        score = 0
    return max(0, min(100, score))


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _api_key() -> str:
    return (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_GENAI_API_KEY")
        or ""
    ).strip()
