from gptr_upgrade.capabilities import DEFAULT_CAPABILITIES


def test_default_capabilities_include_deep_research() -> None:
    capability = DEFAULT_CAPABILITIES["deep_research"]
    assert capability.review_policy == "strict"
    assert "outline_approval" in capability.checkpoint_policy
    assert "contradictions.md" in capability.artifacts
