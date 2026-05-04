from gpt_researcher.utils.output_sanitizer import sanitize_report_output


def test_sanitize_report_output_removes_think_block() -> None:
    raw = "<think>internal chain of thought</think>\n\n# Final Report\nUseful content"
    cleaned = sanitize_report_output(raw)
    assert cleaned == "# Final Report\nUseful content"


def test_sanitize_report_output_preserves_normal_markdown() -> None:
    raw = "# Title\n\nBody text"
    cleaned = sanitize_report_output(raw)
    assert cleaned == raw
