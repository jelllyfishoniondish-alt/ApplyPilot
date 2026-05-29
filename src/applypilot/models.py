"""Domain models for ApplyPilot."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ApplicationStatus(str, Enum):
    DISCOVERED = "discovered"
    PLANNED = "planned"
    DRAFTING = "drafting"
    READY_FOR_REVIEW = "ready_for_review"
    SUBMITTED = "submitted"
    FOLLOW_UP = "follow_up"


@dataclass(frozen=True)
class UserProfile:
    user_id: str
    headline: str
    skills: tuple[str, ...]
    evidence: tuple[str, ...]
    constraints: tuple[str, ...] = ()
    target_roles: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    domain_interests: tuple[str, ...] = ()
    education: tuple[str, ...] = ()
    certifications: tuple[str, ...] = ()
    locations: tuple[str, ...] = ()


@dataclass(frozen=True)
class JobPosting:
    company: str
    title: str
    source_url: str
    description: str
    required_skills: tuple[str, ...]
    nice_to_have_skills: tuple[str, ...] = ()


@dataclass(frozen=True)
class FitAssessment:
    score: int
    matched_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]
    risks: tuple[str, ...]


@dataclass(frozen=True)
class ApplicationPlan:
    user_id: str
    company: str
    title: str
    status: ApplicationStatus
    fit: FitAssessment
    steps: tuple[str, ...]
    approval_required: tuple[str, ...]
    mcp_operations: tuple[dict, ...] = field(default_factory=tuple)
