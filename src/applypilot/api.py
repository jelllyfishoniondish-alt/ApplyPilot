"""Minimal FastAPI backend for ApplyPilot."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .agent import ApplyPilotAgent
from .auth import create_token, decode_token, hash_password, verify_password
from .db import create_user as db_create_user
from .db import delete_job as db_delete_job
from .db import get_user_by_email as db_get_user_by_email
from .db import get_user_by_id as db_get_user_by_id
from .db import list_jobs as db_list_jobs
from .db import save_job as db_save_job
from .db import storage_mode
from .db import update_job as db_update_job
from .db_mcp import MongoMCPClient
from .gemini import GeminiAnalyzer, GeminiAnalyzerError
from .job_fetcher import JobFetchError, fetch_job_description
from .models import ApplicationPlan, JobPosting, UserProfile


STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    mcp = MongoMCPClient()
    app.state.mcp = mcp
    # Start MCP in background so the server responds immediately.
    # Requests arriving before MCP is ready fall back to the file store.
    asyncio.create_task(mcp.start())
    yield
    await mcp.stop()


app = FastAPI(title="ApplyPilot API", version="0.1.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
agent = ApplyPilotAgent()
gemini_analyzer = GeminiAnalyzer()
analysis_cache: dict[str, dict] = {}


class UserProfileRequest(BaseModel):
    user_id: str = "default-user"
    headline: str = "Job seeker"
    target_roles: list[str] = Field(default_factory=list)
    core_skills: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    domain_interests: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    degree_levels: list[str] = Field(default_factory=list)
    study_fields: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class JobRequest(BaseModel):
    company: str
    title: str
    source_url: str = ""
    description: str = ""
    required_skills: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)


class SaveJobRequest(JobRequest):
    """Extended JobRequest that also carries the analysis result for persistence."""
    analysis: dict = Field(default_factory=dict)


class UpdateJobRequest(BaseModel):
    status: str | None = None
    applied_date: str | None = None
    interview_1_date: str | None = None
    interview_2_date: str | None = None
    offer_date: str | None = None
    rejected_date: str | None = None
    notes: str | None = None


class AnalyzeJobRequest(BaseModel):
    profile: UserProfileRequest
    job: JobRequest


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/dashboard", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


# ── Auth ──────────────────────────────────────────────────────────────────────

async def get_current_user(request: Request) -> dict:
    auth_header = request.headers.get("Authorization", "")
    token = auth_header[7:] if auth_header.startswith("Bearer ") else ""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db_get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/auth/register", status_code=201)
async def register(body: RegisterRequest) -> dict:
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    if not body.email or "@" not in body.email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    if db_get_user_by_email(body.email.lower()):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = db_create_user(body.email.lower(), hash_password(body.password))
    return {"token": create_token(user["id"]), "email": user["email"]}


@app.post("/auth/login")
async def login(body: LoginRequest) -> dict:
    user = db_get_user_by_email(body.email.lower())
    if not user or not verify_password(body.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"token": create_token(user["id"]), "email": user["email"]}


@app.get("/auth/me")
async def me(current_user: dict = Depends(get_current_user)) -> dict:
    return {"id": current_user["id"], "email": current_user["email"]}


@app.post("/analyze-job")
async def analyze_job(request: AnalyzeJobRequest, _: dict = Depends(get_current_user)) -> StreamingResponse:
    """Analyze one job against one user profile. Returns SSE stream with status events."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    async def _generate():
        loop = asyncio.get_event_loop()

        try:
            profile = _to_profile(request.profile)

            # ── Step 1: fetch URL (if needed) ───────────────────────────────
            needs_fetch = bool(request.job.source_url and not request.job.description.strip())
            if needs_fetch:
                yield _sse({"status": "fetching"})

            try:
                job = await loop.run_in_executor(
                    None, lambda: _to_job(request.job)
                )
            except JobFetchError as exc:
                plan = agent.create_application_plan(
                    profile=profile,
                    job=JobPosting(
                        company=request.job.company,
                        title=request.job.title,
                        source_url=request.job.source_url,
                        description=request.job.description,
                        required_skills=tuple(request.job.required_skills),
                        nice_to_have_skills=tuple(request.job.nice_to_have_skills),
                    ),
                )
                result = _plan_to_dict(plan)
                result["analysis_source"] = "local_fallback"
                result["fallback_reason"] = str(exc)
                result["cache_hit"] = False
                result.update(_derive_extras(result))
                yield _sse({"status": "done", "result": result})
                return

            # ── Step 2: cache check ──────────────────────────────────────────
            cache_key = _analysis_cache_key(profile, job, gemini_analyzer.model)
            if cache_key in analysis_cache:
                result = json.loads(json.dumps(analysis_cache[cache_key]))
                result["cache_hit"] = True
                yield _sse({"status": "done", "result": result})
                return

            # ── Step 3: Gemini analysis ──────────────────────────────────────
            yield _sse({"status": "analyzing"})

            try:
                analysis = await loop.run_in_executor(
                    None, lambda: gemini_analyzer.analyze(profile=profile, job=job)
                )
                result = _plan_to_dict(analysis.plan)
                result["job"] = _job_to_dict(job)
                result["analysis_source"] = "gemini"
                result["model"] = analysis.model
                result.update(analysis.extras)
            except GeminiAnalyzerError as exc:
                plan = agent.create_application_plan(profile=profile, job=job)
                result = _plan_to_dict(plan)
                result["job"] = _job_to_dict(job)
                result["analysis_source"] = "local_fallback"
                result["fallback_reason"] = str(exc)
                result.update(_derive_extras(result))

            result["cache_hit"] = False
            analysis_cache[cache_key] = json.loads(json.dumps(result))
            yield _sse({"status": "done", "result": result})

        except Exception as exc:
            # Last-resort: always send a done event so the browser never hangs.
            print(f"[ApplyPilot] Unhandled error in analyze stream: {exc}")
            yield _sse({"status": "error", "message": str(exc)})

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


def _sse(data: dict) -> str:
    """Format a dict as a Server-Sent Events data line.

    Padded to at least 1 KB so TCP/proxy buffers flush immediately on
    intermediate status events (e.g. 'fetching', 'analyzing').
    """
    payload = f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    if len(payload) < 1024:
        # SSE comment lines (start with ':') are ignored by clients but
        # force the chunk to be large enough to bypass output buffering.
        pad = ":" + " " * (1024 - len(payload) - 3) + "\n\n"
        return pad + payload
    return payload


@app.get("/jobs")
async def list_jobs(request: Request, current_user: dict = Depends(get_current_user)) -> dict:
    """Return all persisted job records for the current user, newest first."""
    user_id = current_user["id"]
    mcp = request.app.state.mcp
    if mcp.is_connected:
        try:
            jobs = await mcp.find("jobs", filter={"user_id": user_id}, sort={"saved_at": -1})
            return {"jobs": jobs, "storage": "mcp"}
        except Exception as exc:
            print(f"[ApplyPilot] MCP find failed ({exc}); falling back.")
    return {"jobs": db_list_jobs(user_id), "storage": storage_mode()}


@app.post("/jobs", status_code=201)
async def create_job(job: SaveJobRequest, request: Request, current_user: dict = Depends(get_current_user)) -> dict:
    """Persist a job posting (with its analysis) via MongoDB MCP or file fallback."""
    record = {
        "id": str(uuid4()),
        "user_id": current_user["id"],
        "company": job.company,
        "title": job.title,
        "source_url": job.source_url,
        "description": job.description,
        "required_skills": job.required_skills,
        "nice_to_have_skills": job.nice_to_have_skills,
        "analysis": job.analysis,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    mcp = request.app.state.mcp
    if mcp.is_connected:
        try:
            saved = await mcp.insert_one("jobs", record)
            return {**saved, "storage": "mcp"}
        except Exception as exc:
            print(f"[ApplyPilot] MCP insert failed ({exc}); falling back.")
    saved = db_save_job({k: v for k, v in record.items() if k != "saved_at"})
    return {**saved, "storage": storage_mode()}


@app.delete("/jobs/{job_id}", status_code=204)
async def delete_job(job_id: str, request: Request, current_user: dict = Depends(get_current_user)) -> None:
    user_id = current_user["id"]
    mcp = request.app.state.mcp
    if mcp.is_connected:
        try:
            deleted = await mcp.delete_one("jobs", {"id": job_id, "user_id": user_id})
            if not deleted:
                raise HTTPException(status_code=404, detail="Job not found")
            return
        except HTTPException:
            raise
        except Exception as exc:
            print(f"[ApplyPilot] MCP delete failed ({exc}); falling back.")
    if not db_delete_job(job_id, user_id):
        raise HTTPException(status_code=404, detail="Job not found")


@app.patch("/jobs/{job_id}")
async def update_job(job_id: str, body: UpdateJobRequest, request: Request, current_user: dict = Depends(get_current_user)) -> dict:
    user_id = current_user["id"]
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    mcp = request.app.state.mcp
    if mcp.is_connected:
        try:
            updated = await mcp.update_one("jobs", {"id": job_id, "user_id": user_id}, {"$set": updates})
            if updated is None:
                raise HTTPException(status_code=404, detail="Job not found")
            return updated
        except HTTPException:
            raise
        except Exception as exc:
            print(f"[ApplyPilot] MCP update failed ({exc}); falling back.")
    updated = db_update_job(job_id, updates, user_id)
    if updated is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated


def _to_profile(request: UserProfileRequest) -> UserProfile:
    education = _unique_items([*request.education, *request.degree_levels, *request.study_fields])
    skills = _unique_items([
        *request.core_skills,
        *request.skills,
        *request.tools,
        *request.domain_interests,
        *request.study_fields,
        *request.certifications,
    ])
    evidence = _unique_items([*request.evidence, *education, *request.certifications])
    constraints = _unique_items([*request.constraints, *request.locations])
    headline = request.headline
    if request.target_roles:
        headline = f"{headline} targeting {', '.join(request.target_roles)}"

    return UserProfile(
        user_id=request.user_id,
        headline=headline,
        skills=tuple(skills),
        evidence=tuple(evidence),
        constraints=tuple(constraints),
        target_roles=tuple(request.target_roles),
        tools=tuple(request.tools),
        domain_interests=tuple(request.domain_interests),
        education=tuple(education),
        certifications=tuple(request.certifications),
        locations=tuple(request.locations),
    )


def _to_job(request: JobRequest) -> JobPosting:
    description = request.description
    if request.source_url and not description.strip():
        description = fetch_job_description(request.source_url)

    return JobPosting(
        company=request.company,
        title=request.title,
        source_url=request.source_url,
        description=description,
        required_skills=tuple(request.required_skills),
        nice_to_have_skills=tuple(request.nice_to_have_skills),
    )


def _plan_to_dict(plan: ApplicationPlan) -> dict:
    return {
        "user_id": plan.user_id,
        "company": plan.company,
        "title": plan.title,
        "status": plan.status.value,
        "fit": {
            "score": plan.fit.score,
            "matched_skills": list(plan.fit.matched_skills),
            "missing_skills": list(plan.fit.missing_skills),
            "risks": list(plan.fit.risks),
        },
        "steps": list(plan.steps),
        "approval_required": list(plan.approval_required),
        "mcp_operations": list(plan.mcp_operations),
    }


def _job_to_dict(job: JobPosting) -> dict:
    return {
        "company": job.company,
        "title": job.title,
        "source_url": job.source_url,
        "description": job.description,
        "required_skills": list(job.required_skills),
        "nice_to_have_skills": list(job.nice_to_have_skills),
    }


def _unique_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = item.strip()
        key = cleaned.lower()
        if cleaned and key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def _derive_extras(result: dict) -> dict:
    """Derive agent-loop extras from a local-fallback result when Gemini is unavailable."""
    score = result.get("fit", {}).get("score", 0)
    action = "apply" if score >= 70 else "maybe" if score >= 45 else "skip"
    matched = result.get("fit", {}).get("matched_skills", [])
    return {
        "recommended_action": action,
        "application_angle": "",
        "cv_keywords": matched[:6],
        "cover_letter_bullets": [],
    }


def _analysis_cache_key(profile: UserProfile, job: JobPosting, model: str) -> str:
    payload = {
        "model": model,
        "profile": asdict(profile),
        "job": asdict(job),
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)
