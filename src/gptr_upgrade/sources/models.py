from __future__ import annotations

from dataclasses import dataclass


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
