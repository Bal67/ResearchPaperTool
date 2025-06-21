from app.bedrock_client import call_claude

qa_memory = []

def init_qa_memory():
    global qa_memory
    qa_memory = []

def add_to_qa_memory(question, answer):
    qa_memory.append((question, answer))

def ask_question_with_memory(full_text, question):
    history = "\n".join([f"Q: {q}\nA: {a}" for q, a in qa_memory])

    prompt = f"""
You are an expert research assistant. Use the research paper content below to answer the user's question.

Paper content:
\"\"\"
{full_text[:15000]}
\"\"\"

{history}

Question: {question}
Answer:
""".strip()

    return call_claude(prompt)
