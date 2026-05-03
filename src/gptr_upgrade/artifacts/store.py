from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import ArtifactRecord


class ArtifactStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def artifacts_path(self) -> Path:
        return self.project_dir / "artifacts.json"

    def save(self, artifacts: list[ArtifactRecord]) -> Path:
        path = self.artifacts_path()
        payload = [asdict(artifact) for artifact in artifacts]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
