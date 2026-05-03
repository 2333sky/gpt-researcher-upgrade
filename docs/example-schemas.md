# Example Schemas

## `project.json`

```json
{
  "project_id": "proj_ai_agents_20260503",
  "title": "AI Agent Infrastructure Trends",
  "status": "active",
  "capability": "deep_research",
  "profile": "high_confidence_mode",
  "current_stage": "researching",
  "created_at": "2026-05-03T17:00:00Z",
  "updated_at": "2026-05-03T17:30:00Z",
  "latest_report_path": "reports/v1.md"
}
```

## `topic_block.json`

```json
{
  "block_id": "topic_07",
  "title": "Memory architectures for agents",
  "parent": "topic_02",
  "status": "pending",
  "priority": 0.82,
  "source_reason": "emerged_during_research",
  "assigned_worker": null,
  "evidence_count": 0,
  "notes_ref": []
}
```

## `artifacts.json`

```json
[
  {
    "artifact_id": "artifact_01",
    "artifact_type": "report",
    "path": "reports/v1.md",
    "summary": "First draft report placeholder",
    "tags": ["draft"]
  }
]
```

## `checkpoints.json`

```json
[
  {
    "checkpoint_id": "cp_01",
    "kind": "outline_approval",
    "status": "pending",
    "prompt": "Approve the initial outline before deeper research?",
    "options": ["approve", "revise"]
  }
]
```

## `memory/entries.json`

```json
[
  {
    "memory_id": "mem_01",
    "level": "project",
    "summary": "Prefer stronger source review before publishing.",
    "confidence": "medium"
  }
]
```

## `source_index.jsonl`

```json
{"url":"https://example.com/post-1","title":"Example Post","publisher":"Example","source_type":"web","retrieval_time":"2026-05-03T17:10:00Z","credibility":"medium"}
{"url":"https://arxiv.org/abs/1234.5678","title":"Example Paper","publisher":"arXiv","source_type":"paper","retrieval_time":"2026-05-03T17:12:00Z","credibility":"high"}
```
