from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Checkpoint:
    checkpoint_id: str
    kind: str
    status: str = "pending"
    prompt: str = ""
    options: list[str] = field(default_factory=list)
