def summarize_text(text, max_length=100):
    text = text.strip()
    if not text:
        return ""
    return text if len(text) <= max_length else text[:max_length] + "..."
