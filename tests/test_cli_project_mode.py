from argparse import Namespace
from pathlib import Path
from unittest.mock import AsyncMock, patch

from gpt_researcher.cli import async_main
from gpt_researcher.utils.enum import ReportType


@patch("gpt_researcher.cli.write_md_to_word", new_callable=AsyncMock)
@patch("gpt_researcher.cli.write_md_to_pdf", new_callable=AsyncMock)
@patch("gpt_researcher.cli.GPTResearcher")
def test_cli_project_mode(mock_researcher_cls, mock_pdf, mock_docx, tmp_path: Path):
    mock_pdf.return_value = None
    mock_docx.return_value = None

    researcher = mock_researcher_cls.return_value
    researcher.conduct_research = AsyncMock()
    researcher.write_report = AsyncMock(return_value="# CLI Report")
    researcher.get_project_workspace_summary.return_value = {
        "project_id": "cli-project",
        "project_dir": str(tmp_path / "project_dir"),
        "report_path": str(tmp_path / "project_dir" / "reports" / "latest_report.md"),
        "export_path": str(tmp_path / "project_dir" / "exports" / "cli-project.md"),
        "added_sources": 3,
    }

    args = Namespace(
        query="Study agent memory systems",
        report_type=ReportType.ResearchReport.value,
        tone="objective",
        encoding="utf-8",
        query_domains="",
        report_source="web",
        no_pdf=True,
        no_docx=True,
        project_root=str(tmp_path / "workspace_root"),
        project_id="cli-project",
        project_title="CLI Project",
        project_capability="deep_research",
        project_profile="balanced",
    )

    import asyncio

    result = asyncio.run(async_main(args))
    assert Path(result["artifact_filepath"]).exists()
    assert result["project_summary"]["project_id"] == "cli-project"
    mock_researcher_cls.assert_called_once()
