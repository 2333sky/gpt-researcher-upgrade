from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from gptr_upgrade.common import load_json, save_json

from .models import Checkpoint


class CheckpointStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def checkpoints_path(self) -> Path:
        return self.project_dir / "checkpoints.json"

    def list(self) -> list[Checkpoint]:
        payload = load_json(self.checkpoints_path(), [])
        return [Checkpoint(**item) for item in payload]

    def save(self, checkpoints: list[Checkpoint]) -> Path:
        return save_json(self.checkpoints_path(), [asdict(checkpoint) for checkpoint in checkpoints])

    def append(self, checkpoint: Checkpoint) -> Path:
        checkpoints = self.list()
        checkpoints.append(checkpoint)
        return self.save(checkpoints)
