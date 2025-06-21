import re
from app.bedrock_client import call_claude

def split_into_chunks(text: str, max_words: int = 200, overlap: int = 50) -> list:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start:start + max_words])
        chunks.append(chunk)
        start += max_words - overlap
    return chunks


def find_relevant_chunk(chunks: list, question: str) -> str:
    scores = []
    q_words = set(re.findall(r"\w+", question.lower()))

    for chunk in chunks:
        c_words = set(re.findall(r"\w+", chunk.lower()))
        common = q_words.intersection(c_words)
        scores.append((len(common), chunk))

    scores.sort(reverse=True)
    return scores[0][1] if scores else ""


def ask_question_by_chunk(paper_text: str, question: str) -> str:
    chunks = split_into_chunks(paper_text, max_words=200, overlap=50)
    relevant = find_relevant_chunk(chunks, question)

    prompt = f"""Use the following excerpt from a research paper to answer the question below as accurately as possible.

Excerpt:
{relevant}

Question:
{question}
"""

    return call_claude(prompt)
