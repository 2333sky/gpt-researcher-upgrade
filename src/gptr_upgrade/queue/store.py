from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import TopicBlock


class QueueStore:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)

    def queue_path(self) -> Path:
        return self.base_dir / "queue.json"

    def save(self, blocks: list[TopicBlock]) -> Path:
        path = self.queue_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(block) for block in blocks]
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
