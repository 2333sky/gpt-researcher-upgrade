from __future__ import annotations

from pathlib import Path

from .common import generate_id, slugify, utc_now_iso
from .exporter import export_project_markdown
from .models import ArtifactRecord, Checkpoint, MemoryEntry, ResearchProject, SourceRecord, TopicBlock
from .store import ArtifactStore, CheckpointStore, MemoryStore, QueueStore, SourceStore, WorkspaceStore


class ProjectWorkspaceRuntime:
    def __init__(
        self,
        root: str | Path,
        title: str,
        project_id: str | None = None,
        capability: str = "deep_research",
        profile: str = "balanced",
    ):
        self.root = Path(root)
        self.project_id = project_id or slugify(title)
        self.workspace = WorkspaceStore(self.root)
        self.project = self._load_or_init_project(title=title, capability=capability, profile=profile)
        self.project_dir = self.workspace.project_dir(self.project_id)
        self.queue = QueueStore(self.project_dir)
        self.sources = SourceStore(self.project_dir)
        self.checkpoints = CheckpointStore(self.project_dir)
        self.artifacts = ArtifactStore(self.project_dir)
        self.memory = MemoryStore(self.project_dir)

    def _load_or_init_project(self, title: str, capability: str, profile: str) -> ResearchProject:
        try:
            project = self.workspace.load_project(self.project_id)
            if title and project.title != title:
                project.title = title
                self.workspace.save_project(project)
            return project
        except FileNotFoundError:
            project = ResearchProject(
                project_id=self.project_id,
                title=title,
                capability=capability,
                profile=profile,
            )
            self.workspace.init_project(project)
            return project

    def ensure_seed_topic(self, title: str, source_reason: str = "initial_query") -> None:
        topics = self.queue.list()
        if topics:
            return
        self.queue.append(
            TopicBlock(
                block_id=generate_id("topic"),
                title=title,
                priority=1.0,
                source_reason=source_reason,
            )
        )

    def add_checkpoint(self, kind: str, prompt: str, options: list[str] | None = None) -> str:
        checkpoint = Checkpoint(
            checkpoint_id=generate_id("checkpoint"),
            kind=kind,
            prompt=prompt,
            options=options or [],
        )
        self.checkpoints.append(checkpoint)
        return checkpoint.checkpoint_id

    def add_sources_from_research(self, research_sources: list[dict]) -> int:
        existing = {source.url for source in self.sources.list() if source.url}
        added = 0
        for item in research_sources or []:
            url = item.get("url") or item.get("href") or ""
            if not url or url in existing:
                continue
            title = item.get("title") or item.get("name") or url
            publisher = item.get("publisher") or item.get("source") or ""
            summary = item.get("content") or item.get("body") or item.get("summary") or ""
            self.sources.append(
                SourceRecord(
                    source_id=generate_id("source"),
                    url=url,
                    title=title,
                    publisher=publisher,
                    source_type=item.get("source_type") or "web",
                    credibility=item.get("credibility") or "medium",
                    summary=summary[:500],
                    retrieved_at=utc_now_iso(),
                )
            )
            existing.add(url)
            added += 1
        return added

    def add_memory_entry(self, level: str, summary: str, confidence: str = "medium") -> str:
        entry = MemoryEntry(
            memory_id=generate_id("memory"),
            level=level,
            summary=summary,
            confidence=confidence,
        )
        self.memory.append(entry)
        return entry.memory_id

    def persist_report(self, report: str) -> Path:
        report_path = self.project_dir / "reports" / "latest_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")

        self.artifacts.append(
            ArtifactRecord(
                artifact_id=generate_id("artifact"),
                artifact_type="report",
                path=str(report_path.relative_to(self.project_dir)),
                summary="Latest generated report",
                tags=["report", "latest"],
            )
        )

        self.project.latest_report_path = str(report_path.relative_to(self.project_dir))
        self.project.current_stage = "report_generated"
        self.workspace.save_project(self.project)
        return report_path

    def sync_from_research(self, report: str, research_sources: list[dict], context: list[str], visited_urls: list[str] | None = None) -> dict:
        self.ensure_seed_topic(self.project.title)
        added_sources = self.add_sources_from_research(research_sources)

        if visited_urls:
            existing_urls = {source.url for source in self.sources.list() if source.url}
            for url in visited_urls:
                if url in existing_urls:
                    continue
                self.sources.append(
                    SourceRecord(
                        source_id=generate_id("source"),
                        url=url,
                        title=url,
                        source_type="web",
                        credibility="medium",
                        retrieved_at=utc_now_iso(),
                    )
                )
                existing_urls.add(url)
                added_sources += 1

        report_path = self.persist_report(report)
        context_size = len(context) if isinstance(context, list) else 0
        self.add_memory_entry("project", f"Research run captured {context_size} context blocks and {added_sources} sources.")
        export_path = export_project_markdown(self.root, self.project_id)
        return {
            "project_id": self.project_id,
            "project_dir": str(self.project_dir),
            "report_path": str(report_path),
            "export_path": str(export_path),
            "added_sources": added_sources,
        }
