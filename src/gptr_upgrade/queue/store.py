from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from gptr_upgrade.common import load_json, save_json

from .models import TopicBlock


class QueueStore:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)

    def queue_path(self) -> Path:
        return self.base_dir / "queue.json"

    def list(self) -> list[TopicBlock]:
        payload = load_json(self.queue_path(), [])
        return [TopicBlock(**item) for item in payload]

    def save(self, blocks: list[TopicBlock]) -> Path:
        return save_json(self.queue_path(), [asdict(block) for block in blocks])

    def append(self, block: TopicBlock) -> Path:
        blocks = self.list()
        blocks.append(block)
        return self.save(blocks)
