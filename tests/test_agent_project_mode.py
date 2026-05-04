from unittest.mock import AsyncMock, patch

from gpt_researcher.agent import GPTResearcher


@patch("langchain_openai.OpenAIEmbeddings")
@patch("gpt_researcher.agent.choose_agent", new_callable=AsyncMock)
@patch("gpt_researcher.skills.researcher.ResearchConductor.conduct_research", new_callable=AsyncMock)
@patch("gpt_researcher.skills.writer.ReportGenerator.write_report", new_callable=AsyncMock)
def test_agent_project_mode_sync(
    mock_write_report,
    mock_conduct_research,
    mock_choose_agent,
    mock_embeddings,
    tmp_path,
):
    mock_choose_agent.return_value = ("researcher", "Research specialist")
    mock_conduct_research.return_value = ["Context block"]
    mock_write_report.return_value = "# Final report\n\nDone"

    researcher = GPTResearcher(
        query="Map the AI agent tooling landscape",
        project_root=str(tmp_path / "projects_root"),
        project_id="agent-tooling-landscape",
    )
    researcher.add_research_sources([
        {"title": "Example", "url": "https://example.com", "content": "hello"}
    ])
    researcher.visited_urls.add("https://example.com/visited")

    import asyncio

    asyncio.run(researcher.conduct_research())
    report = asyncio.run(researcher.write_report())

    assert report.startswith("# Final report")
    summary = researcher.get_project_workspace_summary()
    assert summary is not None
    assert summary["project_id"] == "agent-tooling-landscape"
    assert (tmp_path / "projects_root" / "projects" / "agent-tooling-landscape" / "reports" / "latest_report.md").exists()
