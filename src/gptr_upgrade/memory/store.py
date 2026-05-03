from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import MemoryEntry


class MemoryStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def memory_path(self) -> Path:
        return self.project_dir / "memory" / "entries.json"

    def save(self, entries: list[MemoryEntry]) -> Path:
        path = self.memory_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(entry) for entry in entries]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
