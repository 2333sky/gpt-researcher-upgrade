from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import Checkpoint


class CheckpointStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def checkpoints_path(self) -> Path:
        return self.project_dir / "checkpoints.json"

    def save(self, checkpoints: list[Checkpoint]) -> Path:
        path = self.checkpoints_path()
        payload = [asdict(checkpoint) for checkpoint in checkpoints]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
