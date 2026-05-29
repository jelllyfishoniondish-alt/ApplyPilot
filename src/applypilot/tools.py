"""Tool planning helpers for ApplyPilot."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .models import ApplicationStatus, JobPosting, UserProfile


class MongoMcpPlanner:
    """Builds MongoDB MCP operations without executing them locally."""

    def plan_application_upsert(
        self,
        profile: UserProfile,
        job: JobPosting,
        status: ApplicationStatus,
        fit_score: int,
    ) -> tuple[dict[str, Any], ...]:
        now = datetime.now(timezone.utc).isoformat()
        job_key = self._job_key(job)
        application_key = f"{profile.user_id}:{job_key}"

        return (
            {
                "tool": "mongodb_mcp.update_one",
                "collection": "jobs",
                "filter": {"job_key": job_key},
                "update": {
                    "$set": {
                        "job_key": job_key,
                        "company": job.company,
                        "title": job.title,
                        "source_url": job.source_url,
                        "description": job.description,
                        "required_skills": list(job.required_skills),
                        "nice_to_have_skills": list(job.nice_to_have_skills),
                        "updated_at": now,
                    },
                    "$setOnInsert": {"created_at": now},
                },
                "upsert": True,
            },
            {
                "tool": "mongodb_mcp.update_one",
                "collection": "applications",
                "filter": {"application_key": application_key},
                "update": {
                    "$set": {
                        "application_key": application_key,
                        "user_id": profile.user_id,
                        "job_key": job_key,
                        "status": status.value,
                        "fit_score": fit_score,
                        "updated_at": now,
                    },
                    "$setOnInsert": {"created_at": now},
                },
                "upsert": True,
            },
            {
                "tool": "mongodb_mcp.insert_one",
                "collection": "events",
                "document": {
                    "application_key": application_key,
                    "event_type": "application_plan_created",
                    "created_at": now,
                    "details": {
                        "company": job.company,
                        "title": job.title,
                        "status": status.value,
                    },
                },
            },
        )

    @staticmethod
    def _job_key(job: JobPosting) -> str:
        safe_company = job.company.lower().strip().replace(" ", "-")
        safe_title = job.title.lower().strip().replace(" ", "-")
        return f"{safe_company}:{safe_title}"
