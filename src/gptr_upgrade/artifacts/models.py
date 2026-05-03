from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ArtifactRecord:
    artifact_id: str
    artifact_type: str
    path: str
    summary: str = ""
    tags: list[str] = field(default_factory=list)
