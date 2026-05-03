# GPT Researcher Upgrade

> A local-first CLI research workspace for structured, project-based research workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## What this is

This repository now ships a **usable MVP product**:

- installable Python package
- CLI entrypoint: `gptr`
- local project workspace management
- topic queue tracking
- checkpoint management
- source tracking
- artifact tracking
- project memory tracking
- Markdown workspace export

It is designed for people who want to organize research as a durable project instead of a one-shot chat.

## Product status

This repository now provides a **working local-first MVP**.

Right now, it is a real product for organizing and operating a research workspace:
- create projects
- track research topics
- manage checkpoints
- store sources and artifacts
- record durable memory
- export project snapshots to Markdown

What it does **not yet** include is automatic integration with GPT Researcher's existing retriever / writer execution pipeline. That is a next-stage integration target, not a blocker for the current MVP.

## Install

```bash
git clone https://github.com/2333sky/gpt-researcher-upgrade.git
cd gpt-researcher-upgrade
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Quick start

### 1. Create a project

```bash
gptr init --title "AI Agent Infrastructure Trends" --project-id ai-agent-infra
```

### 2. Add topics

```bash
gptr add-topic ai-agent-infra --title "Memory architectures" --priority 0.9
gptr add-topic ai-agent-infra --title "Agent orchestration patterns" --priority 0.8
```

### 3. Add sources

```bash
gptr add-source ai-agent-infra \
  --url "https://example.com/post" \
  --title "Example Post" \
  --publisher "Example" \
  --source-type web \
  --credibility medium
```

### 4. Add a checkpoint

```bash
gptr add-checkpoint ai-agent-infra \
  --kind outline_approval \
  --prompt "Approve the initial outline before deep research?" \
  --option approve \
  --option revise
```

### 5. Export a Markdown snapshot

```bash
gptr export ai-agent-infra
```

## Commands

### Project commands

```bash
gptr init --title "Project Title" --project-id my-project
gptr projects
gptr show my-project
gptr set-stage my-project --stage research
```

### Topic queue commands

```bash
gptr add-topic my-project --title "Topic" --priority 0.8
gptr list-topics my-project
gptr move-topic my-project topic_xxxxxxxx --status researching
gptr move-topic my-project topic_xxxxxxxx --status done
```

### Source commands

```bash
gptr add-source my-project --url https://example.com --title "Example" --publisher "Example"
gptr list-sources my-project
```

### Checkpoint commands

```bash
gptr add-checkpoint my-project --kind outline_approval --prompt "Approve?"
gptr list-checkpoints my-project
gptr resolve-checkpoint my-project checkpoint_xxxxxxxx --status approved --response "Looks good"
```

### Artifact commands

```bash
gptr add-artifact my-project --type report --path reports/v1.md --summary "Initial draft"
gptr list-artifacts my-project
```

### Memory commands

```bash
gptr add-memory my-project --level project --summary "Prefer stronger source review" --confidence high
gptr list-memory my-project
```

### Other commands

```bash
gptr capabilities
gptr export my-project --output snapshot.md
gptr demo
```

## Workspace layout

By default, data is stored under `./workspace`:

```text
workspace/
  projects/
    <project_id>/
      project.json
      queue.json
      sources.json
      checkpoints.json
      artifacts.json
      memory/
        entries.json
      reports/
      drafts/
      traces/
      exports/
      notes.md
```

You can override the root with:

```bash
gptr --root /path/to/workspace init --title "Project"
```

or via environment variable:

```bash
export GPTR_WORKSPACE_ROOT=/path/to/workspace
```

## Run tests

```bash
source .venv/bin/activate
pytest -q
```

## Repository contents

- `src/gptr_upgrade/` — product code
- `tests/` — automated tests
- `docs/` — background design and schema docs

## Roadmap

The current MVP already works as a local-first research workspace.
Next likely steps:

- add richer state transitions
- add note-taking helpers
- add import/export adapters
- integrate with real research engines
- add API and TUI/web frontends

## License

MIT — see [LICENSE](./LICENSE).
