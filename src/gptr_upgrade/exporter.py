from __future__ import annotations

from pathlib import Path

from gptr_upgrade.artifacts import ArtifactStore
from gptr_upgrade.checkpoints import CheckpointStore
from gptr_upgrade.memory import MemoryStore
from gptr_upgrade.queue.store import QueueStore
from gptr_upgrade.sources import SourceStore
from gptr_upgrade.workspace.store import WorkspaceStore


def export_markdown(root: str | Path, project_id: str, output: str | Path | None = None) -> Path:
    workspace = WorkspaceStore(root)
    project = workspace.load_project(project_id)
    project_dir = workspace.project_dir(project_id)

    topics = QueueStore(project_dir).list()
    sources = SourceStore(project_dir).list()
    checkpoints = CheckpointStore(project_dir).list()
    artifacts = ArtifactStore(project_dir).list()
    memory_entries = MemoryStore(project_dir).list()

    lines: list[str] = []
    lines.append(f"# {project.title}")
    lines.append("")
    lines.append(f"- Project ID: `{project.project_id}`")
    lines.append(f"- Status: `{project.status}`")
    lines.append(f"- Capability: `{project.capability}`")
    lines.append(f"- Profile: `{project.profile}`")
    lines.append(f"- Current stage: `{project.current_stage}`")
    lines.append("")

    lines.append("## Topics")
    lines.append("")
    for topic in topics:
        lines.append(f"- `{topic.block_id}` | {topic.title} | status={topic.status} | priority={topic.priority}")
    if not topics:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Sources")
    lines.append("")
    for source in sources:
        lines.append(f"- `{source.source_id}` | [{source.title}]({source.url}) | {source.publisher} | {source.source_type} | credibility={source.credibility}")
    if not sources:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Checkpoints")
    lines.append("")
    for checkpoint in checkpoints:
        lines.append(f"- `{checkpoint.checkpoint_id}` | {checkpoint.kind} | status={checkpoint.status} | {checkpoint.prompt}")
    if not checkpoints:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Artifacts")
    lines.append("")
    for artifact in artifacts:
        lines.append(f"- `{artifact.artifact_id}` | {artifact.artifact_type} | {artifact.path} | {artifact.summary}")
    if not artifacts:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Memory")
    lines.append("")
    for entry in memory_entries:
        lines.append(f"- `{entry.memory_id}` | {entry.level} | confidence={entry.confidence} | {entry.summary}")
    if not memory_entries:
        lines.append("- (none)")
    lines.append("")

    out_path = Path(output) if output else project_dir / "exports" / f"{project_id}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
