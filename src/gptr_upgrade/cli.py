from __future__ import annotations

import argparse
import os
from pathlib import Path

from gptr_upgrade.artifacts import ArtifactRecord, ArtifactStore
from gptr_upgrade.capabilities import DEFAULT_CAPABILITIES
from gptr_upgrade.checkpoints import Checkpoint, CheckpointStore
from gptr_upgrade.common import generate_id, slugify, utc_now_iso
from gptr_upgrade.exporter import export_markdown
from gptr_upgrade.memory import MemoryEntry, MemoryStore
from gptr_upgrade.queue.models import TopicBlock
from gptr_upgrade.queue.store import QueueStore
from gptr_upgrade.sources import SourceRecord, SourceStore
from gptr_upgrade.workspace.models import ResearchProject
from gptr_upgrade.workspace.store import WorkspaceStore


VALID_TOPIC_STATUS = {"pending", "researching", "done", "blocked"}
VALID_CHECKPOINT_STATUS = {"pending", "approved", "rejected", "resolved"}


def workspace_root(args: argparse.Namespace) -> Path:
    root = args.root or os.getenv("GPTR_WORKSPACE_ROOT") or "./workspace"
    return Path(root)


def get_project_dir(root: Path, project_id: str) -> Path:
    return WorkspaceStore(root).project_dir(project_id)


def cmd_init(args: argparse.Namespace) -> None:
    root = workspace_root(args)
    project_id = args.project_id or slugify(args.title)
    project = ResearchProject(project_id=project_id, title=args.title, capability=args.capability, profile=args.profile)
    path = WorkspaceStore(root).init_project(project)
    print(f"Initialized project: {project.project_id}")
    print(path)


def cmd_projects(args: argparse.Namespace) -> None:
    projects = WorkspaceStore(workspace_root(args)).list_projects()
    for project in projects:
        print(f"{project.project_id}\t{project.title}\t{project.current_stage}\t{project.status}")
    if not projects:
        print("(no projects)")


def cmd_show(args: argparse.Namespace) -> None:
    project = WorkspaceStore(workspace_root(args)).load_project(args.project_id)
    print(f"project_id: {project.project_id}")
    print(f"title: {project.title}")
    print(f"status: {project.status}")
    print(f"capability: {project.capability}")
    print(f"profile: {project.profile}")
    print(f"current_stage: {project.current_stage}")
    print(f"created_at: {project.created_at}")
    print(f"updated_at: {project.updated_at}")


def cmd_set_stage(args: argparse.Namespace) -> None:
    store = WorkspaceStore(workspace_root(args))
    project = store.load_project(args.project_id)
    project.current_stage = args.stage
    store.save_project(project)
    print(f"Updated stage for {args.project_id} -> {args.stage}")


def cmd_add_topic(args: argparse.Namespace) -> None:
    block = TopicBlock(
        block_id=generate_id("topic"),
        title=args.title,
        priority=args.priority,
        source_reason=args.source_reason,
    )
    QueueStore(get_project_dir(workspace_root(args), args.project_id)).append(block)
    print(f"Added topic: {block.block_id}")


def cmd_list_topics(args: argparse.Namespace) -> None:
    topics = QueueStore(get_project_dir(workspace_root(args), args.project_id)).list()
    for topic in topics:
        print(f"{topic.block_id}\t{topic.status}\t{topic.priority}\t{topic.title}")
    if not topics:
        print("(no topics)")


def cmd_move_topic(args: argparse.Namespace) -> None:
    if args.status not in VALID_TOPIC_STATUS:
        raise SystemExit(f"Invalid topic status: {args.status}")
    store = QueueStore(get_project_dir(workspace_root(args), args.project_id))
    topics = store.list()
    found = False
    for topic in topics:
        if topic.block_id == args.topic_id:
            topic.status = args.status
            found = True
            break
    if not found:
        raise SystemExit(f"Topic not found: {args.topic_id}")
    store.save(topics)
    print(f"Updated topic {args.topic_id} -> {args.status}")


def cmd_add_source(args: argparse.Namespace) -> None:
    source = SourceRecord(
        source_id=generate_id("source"),
        url=args.url,
        title=args.title,
        publisher=args.publisher,
        source_type=args.source_type,
        credibility=args.credibility,
        summary=args.summary,
        retrieved_at=utc_now_iso(),
    )
    SourceStore(get_project_dir(workspace_root(args), args.project_id)).append(source)
    print(f"Added source: {source.source_id}")


def cmd_list_sources(args: argparse.Namespace) -> None:
    sources = SourceStore(get_project_dir(workspace_root(args), args.project_id)).list()
    for source in sources:
        print(f"{source.source_id}\t{source.source_type}\t{source.credibility}\t{source.title}\t{source.url}")
    if not sources:
        print("(no sources)")


def cmd_add_checkpoint(args: argparse.Namespace) -> None:
    checkpoint = Checkpoint(
        checkpoint_id=generate_id("checkpoint"),
        kind=args.kind,
        prompt=args.prompt,
        options=args.option or [],
    )
    CheckpointStore(get_project_dir(workspace_root(args), args.project_id)).append(checkpoint)
    print(f"Added checkpoint: {checkpoint.checkpoint_id}")


def cmd_list_checkpoints(args: argparse.Namespace) -> None:
    checkpoints = CheckpointStore(get_project_dir(workspace_root(args), args.project_id)).list()
    for checkpoint in checkpoints:
        print(f"{checkpoint.checkpoint_id}\t{checkpoint.kind}\t{checkpoint.status}\t{checkpoint.prompt}")
    if not checkpoints:
        print("(no checkpoints)")


def cmd_resolve_checkpoint(args: argparse.Namespace) -> None:
    if args.status not in VALID_CHECKPOINT_STATUS:
        raise SystemExit(f"Invalid checkpoint status: {args.status}")
    store = CheckpointStore(get_project_dir(workspace_root(args), args.project_id))
    checkpoints = store.list()
    found = False
    for checkpoint in checkpoints:
        if checkpoint.checkpoint_id == args.checkpoint_id:
            checkpoint.status = args.status
            if args.response:
                checkpoint.prompt = f"{checkpoint.prompt} | response: {args.response}"
            found = True
            break
    if not found:
        raise SystemExit(f"Checkpoint not found: {args.checkpoint_id}")
    store.save(checkpoints)
    print(f"Resolved checkpoint {args.checkpoint_id} -> {args.status}")


def cmd_add_artifact(args: argparse.Namespace) -> None:
    artifact = ArtifactRecord(
        artifact_id=generate_id("artifact"),
        artifact_type=args.type,
        path=args.path,
        summary=args.summary,
        tags=args.tag or [],
    )
    ArtifactStore(get_project_dir(workspace_root(args), args.project_id)).append(artifact)
    print(f"Added artifact: {artifact.artifact_id}")


def cmd_list_artifacts(args: argparse.Namespace) -> None:
    artifacts = ArtifactStore(get_project_dir(workspace_root(args), args.project_id)).list()
    for artifact in artifacts:
        print(f"{artifact.artifact_id}\t{artifact.artifact_type}\t{artifact.path}\t{artifact.summary}")
    if not artifacts:
        print("(no artifacts)")


def cmd_add_memory(args: argparse.Namespace) -> None:
    entry = MemoryEntry(
        memory_id=generate_id("memory"),
        level=args.level,
        summary=args.summary,
        confidence=args.confidence,
    )
    MemoryStore(get_project_dir(workspace_root(args), args.project_id)).append(entry)
    print(f"Added memory: {entry.memory_id}")


def cmd_list_memory(args: argparse.Namespace) -> None:
    entries = MemoryStore(get_project_dir(workspace_root(args), args.project_id)).list()
    for entry in entries:
        print(f"{entry.memory_id}\t{entry.level}\t{entry.confidence}\t{entry.summary}")
    if not entries:
        print("(no memory entries)")


def cmd_capabilities(args: argparse.Namespace) -> None:
    for capability in DEFAULT_CAPABILITIES.values():
        print(f"{capability.name}\tprofile={capability.tool_profile}\treview={capability.review_policy}\tstages={','.join(capability.stages)}")


def cmd_export(args: argparse.Namespace) -> None:
    output = export_markdown(workspace_root(args), args.project_id, args.output)
    print(output)


def cmd_demo(args: argparse.Namespace) -> None:
    root = workspace_root(args)
    demo_args = argparse.Namespace(
        root=str(root),
        project_id="demo-ai-agents",
        title="AI Agent Infrastructure Trends",
        capability="deep_research",
        profile="balanced",
    )
    cmd_init(demo_args)
    cmd_add_topic(argparse.Namespace(root=str(root), project_id="demo-ai-agents", title="Agent orchestration patterns", priority=0.8, source_reason="initial_plan"))
    cmd_add_topic(argparse.Namespace(root=str(root), project_id="demo-ai-agents", title="Memory architectures", priority=0.7, source_reason="initial_plan"))
    cmd_add_source(argparse.Namespace(root=str(root), project_id="demo-ai-agents", url="https://example.com/agents", title="Example Agents Post", publisher="Example", source_type="web", credibility="medium", summary="Seed source"))
    cmd_add_checkpoint(argparse.Namespace(root=str(root), project_id="demo-ai-agents", kind="outline_approval", prompt="Approve the initial outline before deeper research?", option=["approve", "revise"]))
    cmd_add_artifact(argparse.Namespace(root=str(root), project_id="demo-ai-agents", type="report", path="reports/v1.md", summary="Initial draft report", tag=["draft"]))
    cmd_add_memory(argparse.Namespace(root=str(root), project_id="demo-ai-agents", level="project", summary="Prefer stronger source review before publishing.", confidence="medium"))
    export_path = export_markdown(root, "demo-ai-agents", None)
    print(f"Demo export: {export_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gptr", description="Local-first research workspace CLI")
    parser.add_argument("--root", help="Workspace root directory")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--title", required=True)
    p.add_argument("--project-id")
    p.add_argument("--capability", default="deep_research")
    p.add_argument("--profile", default="balanced")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("projects")
    p.set_defaults(func=cmd_projects)

    p = sub.add_parser("show")
    p.add_argument("project_id")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("set-stage")
    p.add_argument("project_id")
    p.add_argument("--stage", required=True)
    p.set_defaults(func=cmd_set_stage)

    p = sub.add_parser("add-topic")
    p.add_argument("project_id")
    p.add_argument("--title", required=True)
    p.add_argument("--priority", type=float, default=0.5)
    p.add_argument("--source-reason", default="initial_plan")
    p.set_defaults(func=cmd_add_topic)

    p = sub.add_parser("list-topics")
    p.add_argument("project_id")
    p.set_defaults(func=cmd_list_topics)

    p = sub.add_parser("move-topic")
    p.add_argument("project_id")
    p.add_argument("topic_id")
    p.add_argument("--status", required=True)
    p.set_defaults(func=cmd_move_topic)

    p = sub.add_parser("add-source")
    p.add_argument("project_id")
    p.add_argument("--url", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--publisher", default="")
    p.add_argument("--source-type", default="web")
    p.add_argument("--credibility", default="medium")
    p.add_argument("--summary", default="")
    p.set_defaults(func=cmd_add_source)

    p = sub.add_parser("list-sources")
    p.add_argument("project_id")
    p.set_defaults(func=cmd_list_sources)

    p = sub.add_parser("add-checkpoint")
    p.add_argument("project_id")
    p.add_argument("--kind", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--option", action="append")
    p.set_defaults(func=cmd_add_checkpoint)

    p = sub.add_parser("list-checkpoints")
    p.add_argument("project_id")
    p.set_defaults(func=cmd_list_checkpoints)

    p = sub.add_parser("resolve-checkpoint")
    p.add_argument("project_id")
    p.add_argument("checkpoint_id")
    p.add_argument("--status", required=True)
    p.add_argument("--response")
    p.set_defaults(func=cmd_resolve_checkpoint)

    p = sub.add_parser("add-artifact")
    p.add_argument("project_id")
    p.add_argument("--type", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--summary", default="")
    p.add_argument("--tag", action="append")
    p.set_defaults(func=cmd_add_artifact)

    p = sub.add_parser("list-artifacts")
    p.add_argument("project_id")
    p.set_defaults(func=cmd_list_artifacts)

    p = sub.add_parser("add-memory")
    p.add_argument("project_id")
    p.add_argument("--level", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--confidence", default="medium")
    p.set_defaults(func=cmd_add_memory)

    p = sub.add_parser("list-memory")
    p.add_argument("project_id")
    p.set_defaults(func=cmd_list_memory)

    p = sub.add_parser("capabilities")
    p.set_defaults(func=cmd_capabilities)

    p = sub.add_parser("export")
    p.add_argument("project_id")
    p.add_argument("--output")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("demo")
    p.set_defaults(func=cmd_demo)

    return parser


def run() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
