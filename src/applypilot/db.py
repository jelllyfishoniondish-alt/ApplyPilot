"""Persistence layer for ApplyPilot.

Priority order:
  1. MongoDB  — when MONGODB_URI is set and reachable
  2. Local JSON file  — jobs.json next to pyproject.toml (default)
  3. In-process list  — last resort fallback

This means local development works out of the box with no extra setup:
data survives server restarts via the JSON file.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# MongoDB singletons — connected lazily on first use.
# ---------------------------------------------------------------------------
_client: Any = None
_db: Any = None
_mongo_connected: bool | None = None  # None = not yet attempted

# ---------------------------------------------------------------------------
# Local JSON file path — sits in the project root (parent of src/).
# ---------------------------------------------------------------------------
def _json_path() -> Path:
    here = Path(__file__).resolve()          # …/src/applypilot/db.py
    project_root = here.parent.parent.parent  # …/ (project root)
    return project_root / "jobs.json"


def _load_json_store() -> list[dict]:
    p = _json_path()
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_json_store(jobs: list[dict]) -> None:
    try:
        _json_path().write_text(
            json.dumps(jobs, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"[ApplyPilot] JSON file write failed: {exc}")


# ---------------------------------------------------------------------------
# MongoDB helpers
# ---------------------------------------------------------------------------
def _get_db() -> Any:
    """Return a live pymongo Database or None (triggers file/memory fallback)."""
    global _client, _db, _mongo_connected
    if _mongo_connected is not None:
        return _db  # already resolved

    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        _mongo_connected = False
        return None

    try:
        from pymongo import MongoClient
        _client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        _client.admin.command("ping")
        _db = _client["applypilot"]
        _mongo_connected = True
        print("[ApplyPilot] Connected to MongoDB.")
    except Exception as exc:
        print(f"[ApplyPilot] MongoDB unavailable ({exc}); using local JSON store.")
        _client = None
        _db = None
        _mongo_connected = False

    return _db


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def storage_mode() -> str:
    """'mongodb', 'file', or 'memory'."""
    if _get_db() is not None:
        return "mongodb"
    return "file"


def save_job(record: dict) -> dict:
    """Persist a job record. Adds *saved_at* and returns the saved dict."""
    record = {**record, "saved_at": datetime.now(timezone.utc).isoformat()}

    db = _get_db()
    if db is not None:
        try:
            db["jobs"].insert_one(record)
            record.pop("_id", None)
            return record
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB insert failed ({exc}); falling back to file.")

    # JSON file persistence
    jobs = _load_json_store()
    jobs.append(record)
    _save_json_store(jobs)
    return record


def list_jobs(user_id: str | None = None) -> list[dict]:
    """Return saved jobs for user_id (all jobs if None), newest first."""
    db = _get_db()
    if db is not None:
        try:
            query = {"user_id": user_id} if user_id else {}
            cursor = db["jobs"].find(query, {"_id": 0}).sort("saved_at", -1)
            return list(cursor)
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB find failed ({exc}); using file store.")

    jobs = _load_json_store()
    if user_id:
        jobs = [j for j in jobs if j.get("user_id") == user_id]
    return list(reversed(jobs))


def delete_job(job_id: str, user_id: str | None = None) -> bool:
    """Delete a job by id (scoped to user_id when provided)."""
    db = _get_db()
    if db is not None:
        try:
            query: dict = {"id": job_id}
            if user_id:
                query["user_id"] = user_id
            result = db["jobs"].delete_one(query)
            return result.deleted_count > 0
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB delete failed ({exc}); using file store.")

    jobs = _load_json_store()
    new_jobs = [
        j for j in jobs
        if not (j.get("id") == job_id and (not user_id or j.get("user_id") == user_id))
    ]
    if len(new_jobs) == len(jobs):
        return False
    _save_json_store(new_jobs)
    return True


def update_job(job_id: str, updates: dict, user_id: str | None = None) -> dict | None:
    """Update fields on a job record (scoped to user_id when provided)."""
    db = _get_db()
    if db is not None:
        try:
            from pymongo import ReturnDocument
            query: dict = {"id": job_id}
            if user_id:
                query["user_id"] = user_id
            result = db["jobs"].find_one_and_update(
                query,
                {"$set": updates},
                return_document=ReturnDocument.AFTER,
            )
            if result:
                result.pop("_id", None)
            return result
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB update failed ({exc}); using file store.")

    jobs = _load_json_store()
    for i, job in enumerate(jobs):
        if job.get("id") == job_id and (not user_id or job.get("user_id") == user_id):
            jobs[i] = {**job, **updates}
            _save_json_store(jobs)
            return jobs[i]
    return None


# ---------------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------------

def _users_json_path() -> Path:
    here = Path(__file__).resolve()
    project_root = here.parent.parent.parent
    return project_root / "users.json"


def _load_users_store() -> list[dict]:
    p = _users_json_path()
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_users_store(users: list[dict]) -> None:
    try:
        _users_json_path().write_text(
            json.dumps(users, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"[ApplyPilot] users.json write failed: {exc}")


def create_user(email: str, hashed_password: str) -> dict:
    """Persist a new user. Returns the saved dict."""
    from uuid import uuid4
    user: dict = {
        "id": str(uuid4()),
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    db = _get_db()
    if db is not None:
        try:
            db["users"].insert_one({**user})
            user.pop("_id", None)
            return user
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB user insert failed ({exc}); using file store.")
    users = _load_users_store()
    users.append(user)
    _save_users_store(users)
    return user


def get_user_by_email(email: str) -> dict | None:
    db = _get_db()
    if db is not None:
        try:
            return db["users"].find_one({"email": email}, {"_id": 0}) or None
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB user lookup failed ({exc}); using file store.")
    return next((u for u in _load_users_store() if u.get("email") == email), None)


def get_user_by_id(user_id: str) -> dict | None:
    db = _get_db()
    if db is not None:
        try:
            return db["users"].find_one({"id": user_id}, {"_id": 0}) or None
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB user lookup failed ({exc}); using file store.")
    return next((u for u in _load_users_store() if u.get("id") == user_id), None)
