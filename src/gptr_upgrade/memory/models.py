from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MemoryEntry:
    memory_id: str
    level: str
    summary: str
    confidence: str = "medium"
