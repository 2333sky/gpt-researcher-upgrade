from __future__ import annotations

from pathlib import Path

from gptr_upgrade.queue.models import TopicBlock
from gptr_upgrade.queue.store import QueueStore
from gptr_upgrade.workspace.models import ResearchProject
from gptr_upgrade.workspace.store import WorkspaceStore


def main() -> None:
    root = Path("./workspace")
    store = WorkspaceStore(root)
    project = ResearchProject(
        project_id="proj_demo_ai_agents",
        title="AI Agent Infrastructure Trends",
    )
    project_dir = store.init_project(project)

    queue_store = QueueStore(project_dir)
    queue_store.save(
        [
            TopicBlock(block_id="topic_01", title="Agent orchestration patterns", priority=0.8),
            TopicBlock(block_id="topic_02", title="Memory architectures", priority=0.7),
        ]
    )

    print(f"Initialized demo workspace at: {project_dir}")


if __name__ == "__main__":
    main()
