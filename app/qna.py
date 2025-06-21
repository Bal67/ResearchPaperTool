import streamlit as st
from app.bedrock_client import call_claude

def init_qa_memory():
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

def add_to_qa_memory(question: str, answer: str):
    st.session_state.qa_history.append({"question": question, "answer": answer})

def ask_question_with_memory(paper_text: str, user_question: str) -> str:
    history = st.session_state.qa_history

    context_messages = [
        {"role": "system", "content": "You are a helpful academic assistant answering questions based on a research paper."},
        {"role": "user", "content": f"Here is the research paper:\n\n{paper_text[:20000]}"}
    ]

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
