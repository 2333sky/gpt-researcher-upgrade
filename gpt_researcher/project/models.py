from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .common import utc_now_iso


@dataclass
class ResearchProject:
    project_id: str
    title: str
    status: str = "active"
    capability: str = "deep_research"
    profile: str = "balanced"
    current_stage: str = "clarify"
    latest_report_path: Optional[str] = None
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)

    def touch(self) -> None:
        self.updated_at = utc_now_iso()


@dataclass
class TopicBlock:
    block_id: str
    title: str
    status: str = "pending"
    priority: float = 0.5
    parent: Optional[str] = None
    source_reason: str = "initial_plan"
    assigned_worker: Optional[str] = None
    evidence_count: int = 0
    notes_ref: list[str] = field(default_factory=list)


@dataclass
class Checkpoint:
    checkpoint_id: str
    kind: str
    status: str = "pending"
    prompt: str = ""
    options: list[str] = field(default_factory=list)


@dataclass
class ArtifactRecord:
    artifact_id: str
    artifact_type: str
    path: str
    summary: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class MemoryEntry:
    memory_id: str
    level: str
    summary: str
    confidence: str = "medium"


@dataclass
class SourceRecord:
    source_id: str
    url: str
    title: str
    publisher: str = ""
    source_type: str = "web"
    credibility: str = "medium"
    summary: str = ""
    retrieved_at: str = ""
