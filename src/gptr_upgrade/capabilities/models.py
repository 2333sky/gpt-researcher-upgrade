from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Capability:
    name: str
    stages: list[str]
    tool_profile: str
    review_policy: str = "standard"
    checkpoint_policy: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)


DEFAULT_CAPABILITIES: dict[str, Capability] = {
    "quick_brief": Capability(
        name="quick_brief",
        stages=["clarify", "research", "write"],
        tool_profile="fast_web",
        artifacts=["final_report.md", "source_index.jsonl"],
    ),
    "deep_research": Capability(
        name="deep_research",
        stages=["clarify", "explore", "research", "review", "write", "publish"],
        tool_profile="hybrid_deep",
        review_policy="strict",
        checkpoint_policy=["outline_approval", "source_review"],
        artifacts=["final_report.md", "outline.json", "evidence_map.json", "contradictions.md"],
    ),
}
