from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .common import load_json, save_json
from .models import ArtifactRecord, Checkpoint, MemoryEntry, ResearchProject, SourceRecord, TopicBlock


class WorkspaceStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def project_dir(self, project_id: str) -> Path:
        return self.root / "projects" / project_id

    def project_path(self, project_id: str) -> Path:
        return self.project_dir(project_id) / "project.json"

    def init_project(self, project: ResearchProject) -> Path:
        project_dir = self.project_dir(project.project_id)
        for rel in ["reports", "drafts", "traces", "memory", "exports"]:
            (project_dir / rel).mkdir(parents=True, exist_ok=True)
        (project_dir / "notes.md").touch(exist_ok=True)
        self.save_project(project)
        return project_dir

    def save_project(self, project: ResearchProject) -> Path:
        project.touch()
        return save_json(self.project_path(project.project_id), asdict(project))

    def load_project(self, project_id: str) -> ResearchProject:
        payload = load_json(self.project_path(project_id), None)
        if not payload:
            raise FileNotFoundError(f"Project not found: {project_id}")
        return ResearchProject(**payload)

    def list_projects(self) -> list[ResearchProject]:
        projects_dir = self.root / "projects"
        if not projects_dir.exists():
            return []
        results: list[ResearchProject] = []
        for path in sorted(projects_dir.glob("*/project.json")):
            payload = load_json(path, None)
            if payload:
                results.append(ResearchProject(**payload))
        return results


class QueueStore:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)

    def queue_path(self) -> Path:
        return self.project_dir / "queue.json"

    def list(self) -> list[TopicBlock]:
        payload = load_json(self.queue_path(), [])
        return [TopicBlock(**item) for item in payload]

    def save(self, blocks: list[TopicBlock]) -> Path:
        return save_json(self.queue_path(), [asdict(block) for block in blocks])

    def append(self, block: TopicBlock) -> Path:
        blocks = self.list()
        blocks.append(block)
        return self.save(blocks)


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
