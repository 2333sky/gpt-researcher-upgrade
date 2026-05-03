from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from gptr_upgrade.common import load_json, save_json

from .models import SourceRecord


class SourceStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def sources_path(self) -> Path:
        return self.project_dir / "sources.json"

    def list(self) -> list[SourceRecord]:
        payload = load_json(self.sources_path(), [])
        return [SourceRecord(**item) for item in payload]

    def save(self, sources: list[SourceRecord]) -> Path:
        return save_json(self.sources_path(), [asdict(source) for source in sources])

    def append(self, source: SourceRecord) -> Path:
        sources = self.list()
        sources.append(source)
        return self.save(sources)
