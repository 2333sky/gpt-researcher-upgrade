from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from gptr_upgrade.common import load_json, save_json

from .models import MemoryEntry


class MemoryStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def memory_path(self) -> Path:
        return self.project_dir / "memory" / "entries.json"

    def list(self) -> list[MemoryEntry]:
        payload = load_json(self.memory_path(), [])
        return [MemoryEntry(**item) for item in payload]

    def save(self, entries: list[MemoryEntry]) -> Path:
        return save_json(self.memory_path(), [asdict(entry) for entry in entries])

    def append(self, entry: MemoryEntry) -> Path:
        entries = self.list()
        entries.append(entry)
        return self.save(entries)
