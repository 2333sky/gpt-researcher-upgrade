# GPT Researcher Upgrade

> A user-owned upgrade playground that now contains **two related layers**:
> 1. a local-first research workspace CLI (`gptr`), and
> 2. a GPT Researcher fork with optional persisted project workspace mode (`gpt-researcher`).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## What this repository is

This repository is no longer just a tiny MVP wrapper. It currently contains:

- **`src/gptr_upgrade/`** — a standalone local-first workspace product
- **`gpt_researcher/`** — a GPT Researcher codebase extended with optional project persistence
- **focused tests** for both layers
- **clean-history user-owned branch workflow** suitable for continued independent development

In plain language:

- If you want a **small structured workspace tool**, use `gptr`
- If you want a **full research runner with project persistence**, use `gpt-researcher`

## What changed on this branch

This branch adds and validates:

- project workspace persistence for GPT Researcher runs
- project metadata, queue, checkpoints, sources, artifacts, memory, and markdown export
- a package CLI for GPT Researcher (`python -m gpt_researcher` / `gpt-researcher`)
- backward-compatible top-level `cli.py`
- output sanitization that strips leaked `<think>...</think>` blocks from final reports
- real local end-to-end validation using a protein thermostability prediction research topic

## Repository layout

```text
.
├── src/gptr_upgrade/         # local-first workspace CLI product (gptr)
├── gpt_researcher/           # GPT Researcher fork + project workspace mode
├── backend/                  # supporting backend/report helpers used by GPT Researcher CLI
├── tests/                    # focused validation for both layers
├── docs/                     # upstream and local docs/reference material
├── .github/workflows/        # CI/deployment workflows
├── pyproject.toml            # gptr package definition + focused pytest config
└── setup.py                  # legacy/upstream packaging path for gpt-researcher
```

## Which entrypoint should I use?

### Option A — `gptr` (recommended for local project bookkeeping)

Use this when you want a lightweight structured workspace without running the full GPT Researcher execution pipeline.

Install:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Examples:

```bash
gptr init --title "AI Agent Infrastructure Trends" --project-id ai-agent-infra
gptr add-topic ai-agent-infra --title "Memory architectures" --priority 0.9
gptr export ai-agent-infra
```

### Option B — `gpt-researcher` / `python -m gpt_researcher`

Use this when you want a real research run plus persistent project artifacts.

Example:

```bash
python -m gpt_researcher "map the AI agent tooling landscape" \
  --report_type research_report \
  --project-root ./research_projects \
  --project-id agent-tooling-landscape \
  --project-title "AI Agent Tooling Landscape" \
  --no-pdf --no-docx
```

This will persist a reusable project workspace alongside the report.

## GPT Researcher project workspace mode

When project mode is enabled, GPT Researcher stores run state under the selected root:

```text
research_projects/
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
        latest_report.md
      exports/
        <project_id>.md
      drafts/
      traces/
      notes.md
```

Supported knobs in `GPTResearcher(...)` and the CLI:

- `project_root`
- `project_id`
- `project_title`
- `project_capability`
- `project_profile`

## Real validation status

This branch was validated with:

1. focused regression tests for workspace sync, CLI wiring, and report sanitization
2. a real local end-to-end research run on:
   - **protein thermostability prediction**
3. a bugfix discovered during that real run:
   - leaked `<think>` blocks were stripped from final user-visible report output

## Quick commands

### `gptr`

```bash
gptr init --title "Project Title" --project-id my-project
gptr projects
gptr show my-project
gptr add-topic my-project --title "Topic" --priority 0.8
gptr add-source my-project --url https://example.com --title "Example"
gptr add-checkpoint my-project --kind outline_approval --prompt "Approve?"
gptr add-artifact my-project --type report --path reports/v1.md
gptr add-memory my-project --level project --summary "Prefer stronger source review"
gptr export my-project --output snapshot.md
```

### `gpt-researcher`

```bash
python -m gpt_researcher "Recent research on protein thermostability prediction" \
  --report_type research_report \
  --report_source web \
  --project-root ./research_projects \
  --project-id protein-thermostability-prediction \
  --project-title "Protein Thermostability Prediction Research" \
  --no-pdf --no-docx
```

## Installation notes

### For `gptr`

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

### For GPT Researcher execution

This repo still carries the broader upstream-style dependency surface used by GPT Researcher. The most reliable source-based setup is:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Then run GPT Researcher directly from the repository root:

```bash
python -m gpt_researcher --help
python cli.py --help
```

Examples used during validation:

```bash
python -m pytest -q \
  tests/test_output_sanitizer.py \
  tests/test_project_workspace.py \
  tests/test_agent_project_mode.py \
  tests/test_cli_project_mode.py \
  tests/test_quick_search.py
```

## Generated files to expect locally

This repository may generate local files during testing or research runs, for example:

- `workspace/`
- `research_projects/`
- `.local-test-runs/`
- `outputs/`

These are intentionally ignored in git.

## Recommended next cleanup after this branch

If you want to make this repository even cleaner later, the best next step is to choose one of these directions explicitly:

1. **product split**
   - separate `gptr` and the GPT Researcher fork into two repositories
2. **single-repo integration**
   - treat this as a long-lived fork and align packaging/docs/CI fully around GPT Researcher
3. **workspace-first productization**
   - keep `gptr` as the main product and treat GPT Researcher integration as an optional engine layer

## License

MIT — see [LICENSE](./LICENSE).
