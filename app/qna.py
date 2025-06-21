import streamlit as st
import re
from app.bedrock_client import call_claude

# --- Memory management ---
def init_qa_memory():
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

def add_to_qa_memory(question: str, answer: str):
    st.session_state.qa_history.append({"question": question, "answer": answer})

# --- Hybrid Q&A ---
def ask_question_with_memory(paper_text: str, user_question: str, context_chunk: str = None) -> str:
    history = st.session_state.qa_history

    context_messages = [
        {"role": "system", "content": "You are a helpful research assistant answering questions about an academic paper."}
    ]

    if context_chunk:
        context_messages.append({"role": "user", "content": f"Context chunk:\n\n{context_chunk}"})
    else:
        context_messages.append({"role": "user", "content": f"Paper content:\n\n{paper_text[:20000]}"})

    for entry in history:
        context_messages.append({"role": "user", "content": entry["question"]})
        context_messages.append({"role": "assistant", "content": entry["answer"]})

    context_messages.append({"role": "user", "content": user_question})

    prompt = {
        "messages": context_messages,
        "max_tokens": 512,
        "temperature": 0.5,
        "anthropic_version": "bedrock-2023-05-31"
    }

    response = call_claude(prompt, raw=True)
    return response


def split_into_chunks(text: str, max_tokens: int = 400) -> list:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    chunk = ""
    for p in paragraphs:
        if len((chunk + p).split()) <= max_tokens:
            chunk += p + "\n\n"
        else:
            chunks.append(chunk.strip())
            chunk = p + "\n\n"
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def find_relevant_chunk(chunks: list, question: str) -> str:
    q_words = set(re.findall(r"\w+", question.lower()))
    scored = []
    for chunk in chunks:
        c_words = set(re.findall(r"\w+", chunk.lower()))
        score = len(q_words & c_words)
        scored.append((score, chunk))
    scored.sort(reverse=True)
    return scored[0][1] if scored else ""
