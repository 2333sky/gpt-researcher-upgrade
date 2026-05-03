from __future__ import annotations

import re
from pathlib import Path

from gptr_upgrade.artifacts import ArtifactRecord, ArtifactStore
from gptr_upgrade.checkpoints import Checkpoint, CheckpointStore
from gptr_upgrade.common import generate_id, slugify
from gptr_upgrade.memory import MemoryEntry, MemoryStore
from gptr_upgrade.queue.models import TopicBlock
from gptr_upgrade.queue.store import QueueStore
from gptr_upgrade.workspace.models import ResearchProject
from gptr_upgrade.workspace.store import WorkspaceStore


STOPWORDS = {
    "a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "with", "how", "what", "why", "is", "are",
}


def infer_topics_from_query(query: str, limit: int = 5) -> list[str]:
    parts = [chunk.strip(" ,.;:!?-") for chunk in re.split(r"[,;]|\band\b|\bvs\b|\bwith\b", query, flags=re.IGNORECASE)]
    topics: list[str] = []
    for part in parts:
        normalized = part.strip()
        if len(normalized) >= 4 and normalized.lower() not in STOPWORDS:
            topics.append(normalized)
    if not topics:
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", query) if w.lower() not in STOPWORDS]
        topics = [" ".join(words[:3])] if words else [query.strip()]

    deduped: list[str] = []
    seen: set[str] = set()
    for topic in topics:
        key = topic.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(topic)
    return deduped[:limit]


def scaffold_project(root: str | Path, title: str, project_id: str | None = None, capability: str = "deep_research", profile: str = "balanced") -> tuple[str, Path]:
    workspace = WorkspaceStore(root)
    resolved_id = project_id or slugify(title)
    project = ResearchProject(project_id=resolved_id, title=title, capability=capability, profile=profile)
    project_dir = workspace.init_project(project)

    topics = [
        TopicBlock(block_id=generate_id("topic"), title=topic, priority=max(0.5, 0.95 - idx * 0.1), source_reason="query_scaffold")
        for idx, topic in enumerate(infer_topics_from_query(title))
    ]
    QueueStore(project_dir).save(topics)

    CheckpointStore(project_dir).save([
        Checkpoint(
            checkpoint_id=generate_id("checkpoint"),
            kind="clarify_scope",
            prompt="Confirm scope, depth, geography, and date range before full research.",
            options=["approve", "narrow", "expand"],
        ),
        Checkpoint(
            checkpoint_id=generate_id("checkpoint"),
            kind="outline_approval",
            prompt="Review the initial topic scaffold before detailed research.",
            options=["approve", "revise"],
        ),
    ])

    MemoryStore(project_dir).save([
        MemoryEntry(
            memory_id=generate_id("memory"),
            level="project",
            summary=f"Project scaffold created from query: {title}",
            confidence="high",
        )
    ])

    ArtifactStore(project_dir).save([
        ArtifactRecord(
            artifact_id=generate_id("artifact"),
            artifact_type="scaffold",
            path="notes.md",
            summary="Initial project scaffold created from query.",
            tags=["scaffold"],
        )
    ])

    notes_path = project_dir / "notes.md"
    notes_lines = [
        f"# {title}",
        "",
        "## Initial scaffold",
        "",
        f"- Project ID: `{resolved_id}`",
        f"- Capability: `{capability}`",
        f"- Profile: `{profile}`",
        "",
        "## Seed topics",
        "",
    ]
    notes_lines.extend([f"- {topic.title}" for topic in topics] or ["- (none)"])
    notes_lines.append("")
    notes_lines.append("## Next actions")
    notes_lines.append("")
    notes_lines.extend([
        "- review the generated topics",
        "- add sources",
        "- resolve checkpoints",
        "- export a markdown snapshot",
    ])
    notes_path.write_text("\n".join(notes_lines), encoding="utf-8")
    return resolved_id, project_dir
