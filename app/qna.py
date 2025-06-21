import streamlit as st
from app.bedrock_client import call_claude

def init_qa_memory():
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

def add_to_qa_memory(question: str, answer: str):
    st.session_state.qa_history.append({"question": question, "answer": answer})

def ask_question_with_memory(paper_text: str, user_question: str, context_chunk: str = None) -> str:
    history = st.session_state.qa_history

    context_messages = [
        {"role": "system", "content": "You are a helpful research assistant answering questions about an academic paper."},
    ]

    # Inject relevant paper content
    if context_chunk:
        context_messages.append({"role": "user", "content": f"Here is the relevant passage:\n\n{context_chunk}"})
    else:
        context_messages.append({"role": "user", "content": f"Here is the full research paper:\n\n{paper_text[:20000]}"})

    # Add memory history
    for entry in history:
        context_messages.append({"role": "user", "content": entry["question"]})
        context_messages.append({"role": "assistant", "content": entry["answer"]})

    # Current question
    context_messages.append({"role": "user", "content": user_question})

    prompt = {
        "messages": context_messages,
        "max_tokens": 512,
        "temperature": 0.5,
        "anthropic_version": "bedrock-2023-05-31"
    }

    response = call_claude(prompt, raw=True)
    return response
