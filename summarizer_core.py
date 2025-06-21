def summarize_text(text: str) -> str:
    text = text.strip()
    if len(text) <= 100:
        return text
    return text[:100] + "..."
