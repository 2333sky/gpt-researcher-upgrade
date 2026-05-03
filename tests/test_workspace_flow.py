from pathlib import Path

from gptr_upgrade.artifacts import ArtifactRecord, ArtifactStore
from gptr_upgrade.checkpoints import Checkpoint, CheckpointStore
from gptr_upgrade.memory import MemoryEntry, MemoryStore
from gptr_upgrade.queue.models import TopicBlock
from gptr_upgrade.queue.store import QueueStore
from gptr_upgrade.workspace.models import ResearchProject
from gptr_upgrade.workspace.store import WorkspaceStore


def test_workspace_flow(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    workspace_store = WorkspaceStore(root)

    project = ResearchProject(
        project_id="proj_test",
        title="Test Project",
    )
    project_dir = workspace_store.init_project(project)

    queue_path = QueueStore(project_dir).save([
        TopicBlock(block_id="topic_01", title="Queues"),
    ])
    artifact_path = ArtifactStore(project_dir).save([
        ArtifactRecord(artifact_id="artifact_01", artifact_type="report", path="reports/v1.md"),
    ])
    checkpoint_path = CheckpointStore(project_dir).save([
        Checkpoint(checkpoint_id="cp_01", kind="outline_approval", prompt="Approve outline?"),
    ])
    memory_path = MemoryStore(project_dir).save([
        MemoryEntry(memory_id="mem_01", level="project", summary="User prefers deeper source review."),
    ])

    assert (project_dir / "project.json").exists()
    assert queue_path.exists()
    assert artifact_path.exists()
    assert checkpoint_path.exists()
    assert memory_path.exists()
