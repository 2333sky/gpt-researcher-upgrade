# GPT Researcher Workspace Upgrade

A project proposal and design package for evolving GPT Researcher from a one-shot report generator into a continuous research workspace.

## Why this exists

GPT Researcher is strong as a research/report engine, but weaker as a continuous project workspace. This project captures a concrete upgrade path inspired by DeepTutor's strengths in:

- continuous workflows
- dynamic topic queues
- tool/workflow decoupling
- artifact persistence
- project memory
- human checkpoints

The goal is **not** to turn GPT Researcher into a tutoring product. The goal is to preserve GPT Researcher's research-quality core while making research work resumable, collaborative, and cumulative.

## Package contents

- `docs/prd.md` — product requirements draft
- `docs/technical-design.md` — architecture and module design
- `docs/roadmap.md` — phased implementation roadmap
- `docs/github-publish.md` — how to publish this repo to GitHub

## Suggested repository use

This repo can serve as:

1. a design proposal repo
2. a planning repo before implementation
3. a seed repo for a real implementation branch
4. a public thinking artifact for discussion on GitHub

## Recommended next moves

- refine the PRD to match your target audience (open-source maintainers / internal team / investors)
- decide whether this remains a proposal repo or becomes an implementation repo
- if implementation starts, add `src/` and issue templates
- optionally add an OpenClaw skill later for recurring repo-analysis / architecture-comparison workflows
