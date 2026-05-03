from __future__ import annotations

from pathlib import Path

from gptr_upgrade.artifacts import ArtifactRecord, ArtifactStore
from gptr_upgrade.checkpoints import Checkpoint, CheckpointStore
from gptr_upgrade.memory import MemoryEntry, MemoryStore
from gptr_upgrade.queue.models import TopicBlock
from gptr_upgrade.queue.store import QueueStore
from gptr_upgrade.workspace.models import ResearchProject
from gptr_upgrade.workspace.store import WorkspaceStore


def main() -> None:
    root = Path("./workspace")
    workspace_store = WorkspaceStore(root)
    project = ResearchProject(
        project_id="proj_demo_ai_agents",
        title="AI Agent Infrastructure Trends",
    )
    project_dir = workspace_store.init_project(project)

    QueueStore(project_dir).save(
        [
            TopicBlock(block_id="topic_01", title="Agent orchestration patterns", priority=0.8),
            TopicBlock(block_id="topic_02", title="Memory architectures", priority=0.7),
        ]
    )
    ArtifactStore(project_dir).save(
        [
            ArtifactRecord(
                artifact_id="artifact_01",
                artifact_type="report",
                path="reports/v1.md",
                summary="First draft report placeholder",
            )
        ]
    )
    CheckpointStore(project_dir).save(
        [
            Checkpoint(
                checkpoint_id="cp_01",
                kind="outline_approval",
                prompt="Approve the initial outline before deeper research?",
                options=["approve", "revise"],
            )
        ]
    )
    MemoryStore(project_dir).save(
        [
            MemoryEntry(
                memory_id="mem_01",
                level="project",
                summary="Prefer stronger source review before publishing.",
            )
        ]
    )

    print(f"Initialized demo workspace at: {project_dir}")


if __name__ == "__main__":
    main()
