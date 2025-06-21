import pytest
from summarizer_core import summarize_text


def test_short_text_returns_same():
    """
    Should return the same text if it's already short.
    """
    text = "This is a short test sentence."
    summary = summarize_text(text)
    assert summary == text


def test_long_text_truncation():
    """
    Should truncate long text and append ellipsis.
    """
    long_text = "word " * 100
    summary = summarize_text(long_text)
    assert summary.endswith("...")
    assert len(summary) <= 103  # assuming truncate to 100 chars + "..."


def test_empty_text_returns_empty():
    """
    Should return empty string when given empty input.
    """
    summary = summarize_text("")
    assert summary == ""


def test_whitespace_only_input():
    """
    Should treat whitespace-only strings as empty.
    """
    summary = summarize_text("     ")
    assert summary.strip() == ""
