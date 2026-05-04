from pathlib import Path

from gpt_researcher.project import ProjectWorkspaceRuntime


def test_project_workspace_runtime_sync(tmp_path: Path) -> None:
    runtime = ProjectWorkspaceRuntime(
        root=tmp_path / "research_projects",
        title="AI Agents Market Map",
        project_id="ai-agents-market-map",
    )
    runtime.ensure_seed_topic("AI Agents Market Map")
    runtime.add_checkpoint("scope", "Confirm research scope", ["yes", "refine"])

    summary = runtime.sync_from_research(
        report="# Report\n\nHello world",
        research_sources=[
            {
                "title": "Example Source",
                "url": "https://example.com/source",
                "content": "Useful details",
            }
        ],
        context=["context block 1", "context block 2"],
        visited_urls=["https://example.com/source", "https://example.com/extra"],
    )

    project_dir = tmp_path / "research_projects" / "projects" / "ai-agents-market-map"
    assert project_dir.exists()
    assert (project_dir / "project.json").exists()
    assert (project_dir / "reports" / "latest_report.md").exists()
    assert (project_dir / "exports" / "ai-agents-market-map.md").exists()
    assert summary["project_id"] == "ai-agents-market-map"
    assert summary["added_sources"] >= 2
