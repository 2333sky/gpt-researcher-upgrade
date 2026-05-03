from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from gptr_upgrade.common import load_json, save_json

from .models import ArtifactRecord


class ArtifactStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def artifacts_path(self) -> Path:
        return self.project_dir / "artifacts.json"

    def list(self) -> list[ArtifactRecord]:
        payload = load_json(self.artifacts_path(), [])
        return [ArtifactRecord(**item) for item in payload]

    def save(self, artifacts: list[ArtifactRecord]) -> Path:
        return save_json(self.artifacts_path(), [asdict(artifact) for artifact in artifacts])

    def append(self, artifact: ArtifactRecord) -> Path:
        artifacts = self.list()
        artifacts.append(artifact)
        return self.save(artifacts)
