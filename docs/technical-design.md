# Technical Design: GPT Researcher Workspace Upgrade

## Design principle

Keep GPT Researcher's high-quality research/report pipeline intact, and add a project/workspace layer around it.

## Proposed architecture layers

1. Research Workspace layer
2. Capability Registry layer
3. Dynamic Topic Queue layer
4. Artifact Store layer
5. Project/Topic Memory layer
6. Existing GPT Researcher multi-agent quality pipeline

## 1. Research Workspace

Suggested structure:

```text
workspace/
  projects/
    <project_id>/
      project.json
      outline.json
      queue.json
      sources.jsonl
      evidence.jsonl
      contradictions.jsonl
      open_questions.jsonl
      reports/
      drafts/
      traces/
      memory/
```

Suggested `project.json`:

```json
{
  "project_id": "proj_ai_agents_20260503",
  "title": "AI Agent Infrastructure Trends",
  "status": "active",
  "capability": "deep_research",
  "profile": "high_confidence_mode",
  "current_stage": "researching"
}
```

## 2. Capability Registry

Each capability defines:
- stages
- allowed tools
- retriever defaults
- review strictness
- checkpoint requirements
- artifact outputs

Example capabilities:
- quick_brief
- deep_research
- reviewed_report
- monitor_update

## 3. Dynamic Topic Queue

Add an exploratory phase before the classic report pipeline.

Flow:

```text
query -> clarify -> topic exploration -> queue -> research workers -> editor/reviewer/revisor/writer
```

Suggested topic block fields:
- block_id
- title
- parent
- status
- priority
- evidence_count
- assigned_worker
- source_reason

## 4. Artifact Store

Default outputs:
- final_report.md
- executive_summary.md
- outline.json
- source_index.jsonl
- evidence_map.json
- contradictions.md
- open_questions.md
- reusable_claims.jsonl

## 5. Memory model

### Run Memory
Execution-local information

### Project Memory
Stable knowledge for this project

### Topic Memory
Reusable patterns and open questions for a topic/domain

### Source Trust Memory
Long-term judgments about recurring sources

## 6. Human checkpoints

Checkpoint A: clarify scope
Checkpoint B: outline approval
Checkpoint C: source review
Checkpoint D: output/publish intent

## 7. Suggested agent graph

```text
query
  -> clarifier
  -> topic_explorer
  -> dynamic_topic_queue
      -> researcher workers
      -> contradiction checker
      -> source curator
  -> editor
  -> reviewer
  -> revisor
  -> writer
  -> publisher
  -> artifact_store
  -> project_memory
```

## 8. Migration strategy

### Phase 1
Add workspace + artifact persistence without changing core research logic

### Phase 2
Introduce capability registry and tool profiles

### Phase 3
Introduce dynamic topic queue for complex research modes

### Phase 4
Add checkpoints and memory
