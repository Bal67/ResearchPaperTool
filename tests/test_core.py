import os
from summarizer_core import summarize_text

def test_short_text():
    text = "This is a short test sentence."
    summary = summarize_text(text)
    assert summary == text

def test_long_text_truncation():
    long_text = "word " * 100
    summary = summarize_text(long_text)
    assert summary.endswith("...")
    assert len(summary) <= 103  # 100 chars + "..."

def test_empty_text():
    summary = summarize_text("")
    assert summary == ""

def test_whitespace_only():
    summary = summarize_text("     ")
    assert summary.strip() == ""
