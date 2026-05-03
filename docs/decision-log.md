# Decision Log

## 2026-05-03

### D-001 — Positioning
Keep this repository as a proposal/design repo first, not a full implementation repo.

Rationale:
- the current value is architectural clarity
- proposal assets can be reviewed before coding starts
- implementation can later be added incrementally under `src/`

### D-002 — Product direction
Treat the core opportunity as upgrading GPT Researcher from one-shot report generation into a continuous research workspace.

Rationale:
- preserves GPT Researcher's research-quality core
- borrows organizational strengths from DeepTutor without turning into a tutoring product

### D-003 — Key borrowed concepts from DeepTutor
Prioritize the following concepts:
- continuous workflows
- dynamic topic queue
- tool/workflow decoupling
- artifact persistence
- project memory
- human checkpoints

### D-004 — Key non-goal
Do not expand into a general-purpose tutor/chatbot product.

Rationale:
- keeps scope aligned with research workflows
- avoids diluting GPT Researcher's strongest value proposition
