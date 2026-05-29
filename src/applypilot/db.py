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


def list_jobs() -> list[dict]:
    """Return all saved jobs, newest first."""
    db = _get_db()
    if db is not None:
        try:
            cursor = db["jobs"].find({}, {"_id": 0}).sort("saved_at", -1)
            return list(cursor)
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB find failed ({exc}); using file store.")

    jobs = _load_json_store()
    return list(reversed(jobs))


def delete_job(job_id: str) -> bool:
    """Delete a job by id. Returns True if deleted, False if not found."""
    db = _get_db()
    if db is not None:
        try:
            result = db["jobs"].delete_one({"id": job_id})
            return result.deleted_count > 0
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB delete failed ({exc}); using file store.")

    jobs = _load_json_store()
    new_jobs = [j for j in jobs if j.get("id") != job_id]
    if len(new_jobs) == len(jobs):
        return False
    _save_json_store(new_jobs)
    return True


def update_job(job_id: str, updates: dict) -> dict | None:
    """Update fields on a job record. Returns updated record or None if not found."""
    db = _get_db()
    if db is not None:
        try:
            from pymongo import ReturnDocument
            result = db["jobs"].find_one_and_update(
                {"id": job_id},
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
        if job.get("id") == job_id:
            jobs[i] = {**job, **updates}
            _save_json_store(jobs)
            return jobs[i]
    return None
