# GPT Researcher Upgrade

> Evolving GPT Researcher from a one-shot report generator into a continuous research workspace.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## Overview

This repository captures a concrete upgrade path for GPT Researcher inspired by one specific class of lessons from DeepTutor: not tutoring UX, but **workflow organization for long-running, cumulative research**.

The core thesis is simple:

- **Keep** GPT Researcher's strong research-quality pipeline
  - editor
  - reviewer
  - revisor
  - writer
  - publisher
- **Add** the missing workspace layer around it
  - resumable projects
  - dynamic topic queues
  - artifact persistence
  - project memory
  - human checkpoints

This repo is currently a **proposal + prototype seed**.

## Why this matters

GPT Researcher is already good at generating research outputs.
What it lacks is a strong model for:

- continuing a research project over time
- preserving intermediate artifacts
- letting users steer the workflow at key stages
- reusing topic knowledge across repeated runs

This project explores how to close that gap without turning GPT Researcher into a general-purpose assistant or tutoring product.

## Goals

- upgrade GPT Researcher into a continuous research workspace
- preserve its high-quality multi-agent report pipeline
- add reusable project structure and research artifacts
- support more exploratory research via dynamic topic queues
- make collaboration checkpoints first-class

## Non-goals

- do not turn GPT Researcher into a generic chatbot
- do not turn it into a tutoring platform
- do not sacrifice rigor for broad feature sprawl

## Repository structure

```text
.
├── README.md
├── LICENSE
├── pyproject.toml
├── docs/
│   ├── prd.md
│   ├── technical-design.md
│   ├── roadmap.md
│   ├── decision-log.md
│   └── example-schemas.md
├── tests/
└── src/
    └── gptr_upgrade/
        ├── artifacts/
        ├── capabilities/
        ├── checkpoints/
        ├── memory/
        ├── queue/
        └── workspace/
```

## Documentation

- `docs/prd.md` — product requirements draft
- `docs/technical-design.md` — architecture and module design
- `docs/roadmap.md` — phased implementation roadmap
- `docs/decision-log.md` — major decisions and rationale
- `docs/example-schemas.md` — example data contracts

## Prototype scope

The initial `src/` prototype is intentionally small.
It exists to make the proposal more concrete by defining:

- workspace/project metadata
- capability contracts
- topic queue schemas
- artifact/checkpoint/memory persistence skeletons

This is **not yet a full implementation of GPT Researcher**.
It is the seed of a future implementation path.

## Run the prototype demo

```bash
cd /path/to/gpt-researcher-upgrade
PYTHONPATH=src python3 src/gptr_upgrade/demo.py
```

This creates a minimal demo workspace under `./workspace/` (gitignored).

## Run tests

```bash
cd /path/to/gpt-researcher-upgrade
PYTHONPATH=src pytest
```

## Initial implementation themes

### 1. Research Workspace
Persist project state and research artifacts across runs.

### 2. Capability Registry
Turn report modes into explicit capabilities with policies.

### 3. Dynamic Topic Queue
Support exploratory research before report convergence.

### 4. Human Checkpoints
Add review/approval points for outline, sources, and output intent.

### 5. Project Memory
Retain durable knowledge at the project/topic/source-trust levels.

## GitHub issues

This repo already contains initial implementation slices as GitHub issues:

- Phase 1: Research Workspace and artifact persistence
- Phase 2: Capability Registry and tool profiles
- Phase 3: Dynamic Topic Queue
- Phase 4: Human Checkpoints and Project Memory

## Suggested next steps

- refine the PRD
- expand the prototype under `src/`
- convert roadmap phases into implementation milestones
- add tests and example fixtures
- validate the design against real GPT Researcher flows

## License

MIT — see [LICENSE](./LICENSE).
