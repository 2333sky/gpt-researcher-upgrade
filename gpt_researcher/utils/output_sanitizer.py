from __future__ import annotations

import re

_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL)
_LEADING_BLANKS_RE = re.compile(r"^\s+")


def sanitize_report_output(text: str) -> str:
    """Remove internal reasoning blocks and trim noisy leading whitespace.

    Some providers may leak hidden reasoning wrapped in <think>...</think> tags.
    This sanitizer strips those blocks from final user-visible report text.
    """
    if not text:
        return text
    cleaned = _THINK_BLOCK_RE.sub("", text)
    cleaned = _LEADING_BLANKS_RE.sub("", cleaned)
    return cleaned.strip()
