"""Package CLI for GPT Researcher.

Supports the traditional one-shot report flow plus an optional project workspace
mode that persists research state under a local project directory.
"""

from __future__ import annotations

import argparse
import asyncio
import os
from argparse import RawTextHelpFormatter
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from gpt_researcher import GPTResearcher
from gpt_researcher.project import ProjectWorkspaceRuntime
from gpt_researcher.utils.enum import ReportType, Tone
from backend.report_type import DetailedReport
from backend.utils import write_md_to_pdf, write_md_to_word

TONE_MAP = {
    "objective": Tone.Objective,
    "formal": Tone.Formal,
    "analytical": Tone.Analytical,
    "persuasive": Tone.Persuasive,
    "informative": Tone.Informative,
    "explanatory": Tone.Explanatory,
    "descriptive": Tone.Descriptive,
    "critical": Tone.Critical,
    "comparative": Tone.Comparative,
    "speculative": Tone.Speculative,
    "reflective": Tone.Reflective,
    "narrative": Tone.Narrative,
    "humorous": Tone.Humorous,
    "optimistic": Tone.Optimistic,
    "pessimistic": Tone.Pessimistic,
}


def build_parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Generate a research report.",
        formatter_class=RawTextHelpFormatter,
    )

    cli.add_argument("query", type=str, help="The query to conduct research on.")

    choices = [report_type.value for report_type in ReportType]
    report_type_descriptions = {
        ReportType.ResearchReport.value: "Summary - Short and fast (~2 min)",
        ReportType.DetailedReport.value: "Detailed - In depth and longer (~5 min)",
        ReportType.ResourceReport.value: "",
        ReportType.OutlineReport.value: "",
        ReportType.CustomReport.value: "",
        ReportType.SubtopicReport.value: "",
        ReportType.DeepResearch.value: "Deep Research",
    }

    cli.add_argument(
        "--report_type",
        type=str,
        help="The type of report to generate. Options:\n" + "\n".join(
            f"  {choice}: {report_type_descriptions[choice]}" for choice in choices
        ),
        choices=choices,
        required=True,
    )

    cli.add_argument(
        "--tone",
        type=str,
        help="The tone of the report (optional).",
        choices=list(TONE_MAP.keys()),
        default="objective",
    )

    cli.add_argument(
        "--encoding",
        type=str,
        help="The encoding to use for the output file (default: utf-8).",
        default="utf-8",
    )

    cli.add_argument(
        "--query_domains",
        type=str,
        help="A comma-separated list of domains to search for the query.",
        default="",
    )

    cli.add_argument(
        "--report_source",
        type=str,
        help="The source of information for the report.",
        choices=[
            "web",
            "local",
            "hybrid",
            "azure",
            "langchain_documents",
            "langchain_vectorstore",
            "static",
        ],
        default="web",
    )

    cli.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF generation (generate markdown and DOCX only).",
    )

    cli.add_argument(
        "--no-docx",
        action="store_true",
        help="Skip DOCX generation (generate markdown and PDF only).",
    )

    cli.add_argument(
        "--project-root",
        type=str,
        default=os.getenv("GPT_RESEARCHER_PROJECT_ROOT", ""),
        help=(
            "Persist research outputs under a local project workspace root. "
            "Also enables project mode. Can also be set via GPT_RESEARCHER_PROJECT_ROOT."
        ),
    )
    cli.add_argument("--project-id", type=str, help="Stable project id for project mode.")
    cli.add_argument(
        "--project-title",
        type=str,
        help="Human-friendly project title. Defaults to the query text.",
    )
    cli.add_argument(
        "--project-capability",
        type=str,
        default="deep_research",
        help="Capability label stored in the project workspace.",
    )
    cli.add_argument(
        "--project-profile",
        type=str,
        default="balanced",
        help="Profile label stored in the project workspace.",
    )

    return cli


def _project_mode_enabled(args: argparse.Namespace) -> bool:
    return bool(args.project_root or args.project_id or args.project_title)


async def _sync_detailed_report_project_mode(args: argparse.Namespace, report: str) -> dict | None:
    if not _project_mode_enabled(args):
        return None
    runtime = ProjectWorkspaceRuntime(
        root=args.project_root or "./research_projects",
        title=args.project_title or args.query,
        project_id=args.project_id,
        capability=args.project_capability,
        profile=args.project_profile,
    )
    runtime.ensure_seed_topic(args.query)
    runtime.add_checkpoint(
        "report_review",
        f"Review the detailed report for: {args.query}",
        options=["approve", "revise"],
    )
    return runtime.sync_from_research(report, research_sources=[], context=[], visited_urls=[])


async def async_main(args: argparse.Namespace) -> dict:
    query_domains = args.query_domains.split(",") if args.query_domains else []
    project_summary = None

    if args.report_type == ReportType.DetailedReport.value:
        detailed_report = DetailedReport(
            query=args.query,
            query_domains=query_domains,
            report_type="research_report",
            report_source="web_search",
        )
        report = await detailed_report.run()
        project_summary = await _sync_detailed_report_project_mode(args, report)
    else:
        researcher = GPTResearcher(
            query=args.query,
            query_domains=query_domains,
            report_type=args.report_type,
            report_source=args.report_source,
            tone=TONE_MAP[args.tone],
            encoding=args.encoding,
            project_root=args.project_root or None,
            project_id=args.project_id,
            project_title=args.project_title,
            project_capability=args.project_capability,
            project_profile=args.project_profile,
        )
        await researcher.conduct_research()
        report = await researcher.write_report()
        project_summary = researcher.get_project_workspace_summary()

    task_id = str(uuid4())
    artifact_filepath = Path("outputs") / f"{task_id}.md"
    artifact_filepath.parent.mkdir(parents=True, exist_ok=True)
    artifact_filepath.write_text(report, encoding="utf-8")

    pdf_path = None
    docx_path = None
    if not args.no_pdf:
        try:
            pdf_path = await write_md_to_pdf(report, task_id)
        except Exception as e:  # pragma: no cover - non-deterministic external dependency
            print(f"Warning: PDF generation failed: {e}")

    if not args.no_docx:
        try:
            docx_path = await write_md_to_word(report, task_id)
        except Exception as e:  # pragma: no cover - non-deterministic external dependency
            print(f"Warning: DOCX generation failed: {e}")

    return {
        "report": report,
        "artifact_filepath": str(artifact_filepath),
        "pdf_path": pdf_path,
        "docx_path": docx_path,
        "project_summary": project_summary,
    }


def render_cli_result(result: dict) -> None:
    print(f"Report written to '{result['artifact_filepath']}'")
    if result.get("pdf_path"):
        print(f"PDF written to '{result['pdf_path']}'")
    if result.get("docx_path"):
        print(f"DOCX written to '{result['docx_path']}'")

    project_summary = result.get("project_summary")
    if project_summary:
        print("Project workspace synchronized:")
        print(f"- Project ID: {project_summary['project_id']}")
        print(f"- Project dir: {project_summary['project_dir']}")
        print(f"- Report path: {project_summary['report_path']}")
        print(f"- Export path: {project_summary['export_path']}")
        print(f"- Added sources: {project_summary['added_sources']}")


def main_sync(argv: list[str] | None = None) -> dict:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)
    result = asyncio.run(async_main(args))
    render_cli_result(result)
    return result


if __name__ == "__main__":
    main_sync()
