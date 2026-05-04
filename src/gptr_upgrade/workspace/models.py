from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from gptr_upgrade.common import utc_now_iso


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
