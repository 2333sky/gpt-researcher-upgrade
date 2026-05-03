from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


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
