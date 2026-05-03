# PRD: GPT Researcher Workspace Upgrade

## Summary

Upgrade GPT Researcher from a one-shot research report generator into a continuous research workspace while preserving its strong editor/reviewer/revisor/writer pipeline.

## Product thesis

The most valuable lesson to borrow from DeepTutor is not tutoring UX, but the way research-related work is organized as a continuous, reusable, collaborative system.

## Goals

1. Support resumable project-based research
2. Persist intermediate research artifacts
3. Add configurable workflows and tool profiles
4. Introduce human checkpoints at key stages
5. Preserve GPT Researcher's research quality pipeline

## Non-goals

1. Do not become a general-purpose chatbot
2. Do not become a tutoring/pedagogy product
3. Do not dilute research rigor for broader feature scope
4. Do not replace existing report-generation strengths

## Target users

- analysts
- researchers
- open-source maintainers
- technical strategy teams
- users running repeated topic investigations

## Core user stories

### 1. Resumable research
As a user, I want to continue a research project later without recomputing everything from scratch.

### 2. Artifact reuse
As a user, I want the system to preserve source maps, evidence, contradictions, and outlines, not just the final report.

### 3. Guided collaboration
As a user, I want to review the outline and source set before the final report is generated.

### 4. Topic monitoring
As a user, I want repeated research on a topic to benefit from project/topic memory.

## Core concepts

### Research Workspace
A durable project container with:
- project metadata
- outline
- source index
- evidence map
- reports
- traces
- memory

### Capability Registry
Explicit research capabilities such as:
- quick_brief
- deep_research
- reviewed_report
- literature_review
- company_dossier
- monitor_update

### Human checkpoints
- clarify intent
- approve outline
- review sources
- confirm publication/output format

## Success metrics

### Product metrics
- project resume rate
- repeat usage per project
- artifact reuse rate
- checkpoint usage rate

### Quality metrics
- citation coverage
- contradiction detection rate
- reduction in hallucination complaints
- revision efficiency
