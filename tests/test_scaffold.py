from gptr_upgrade.scaffold import infer_topics_from_query


def test_infer_topics_from_query() -> None:
    topics = infer_topics_from_query("AI agent infrastructure with memory architectures and orchestration patterns")
    assert topics
    assert any("memory" in topic.lower() for topic in topics)
