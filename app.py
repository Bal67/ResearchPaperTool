import streamlit as st
from app.auth import login
from app.monitoring import log_event, log_error
from app.bedrock_client import call_claude
from app.pdf_parser import parse_uploaded_pdf
from app.qna import (
    find_relevant_chunk,
    split_into_chunks,
    init_qa_memory,
    ask_question_with_memory,
    add_to_qa_memory,
)
from app.comparison import summarize_paper, compare_summaries
from app.admin_logs import show_admin_logs

st.set_page_config(page_title="Research Paper Tool", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

if "display_name" not in st.session_state:
    st.session_state.display_name = st.text_input("Enter your name:")
    if not st.session_state.display_name:
        st.stop()

init_qa_memory()

display_name = st.session_state.display_name

st.title("Research Paper Tool")

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")
if uploaded_file:
    st.session_state.selected_file = uploaded_file

if "selected_file" in st.session_state:
    selected_file = st.session_state.selected_file
    selected_file.seek(0)
    doc = parse_uploaded_pdf(selected_file)
    full_text = doc.sections.get("Full Paper", "")

    # Show summary once and cache it
    if "full_summary" not in st.session_state:
        with st.spinner("Summarizing full paper..."):
            prompt = f"""
            You are an AI assistant. Summarize this research paper in plain English. Focus on key methods, results, and conclusions:
            
            {full_text[:10000]}
            """
            summary = call_claude(prompt)
            st.session_state.full_summary = summary

    st.subheader("Summary")
    st.success(st.session_state.full_summary)

    # Section-based summarization
    st.header("Section-Based Summarization")
    section_list = list(doc.sections.keys())
    if section_list:
        st.info(f"{len(section_list)} sections detected.")
        selected_section = st.selectbox("Choose a section", section_list)
        if selected_section and st.button("Summarize Section"):
            section_text = doc.sections[selected_section][:5000]
            prompt = f"""You are an AI assistant. Summarize the '{selected_section}' section of this research paper in plain English:

            {section_text}"""
            section_summary = call_claude(prompt)
            st.subheader(f"Summary of {selected_section}")
            st.write(section_summary)
    else:
        st.warning("No sections found.")

    # Hybrid Q&A (Memory + Semantic)
    st.header("\U0001F9E0 Ask Questions (Hybrid: Memory + Semantic)")
    qa_text = st.text_input("Ask a question about the uploaded paper:")
    if st.button("Ask"):
        try:
            selected_file.seek(0)
            doc = parse_uploaded_pdf(selected_file)
            full_text = doc.sections.get("Full Paper", "")
            chunks = split_into_chunks(full_text)

            best_chunk = find_relevant_chunk(chunks, qa_text)
            if not best_chunk:
                best_chunk = st.session_state.get("full_summary", full_text[:4000])

            answer = ask_question_with_memory(full_text, qa_text, context_chunk=best_chunk)
            add_to_qa_memory(qa_text, answer)

            st.success("Answer:")
            st.write(answer)
            log_event(display_name, "Hybrid Q&A", qa_text)

        except Exception as e:
            st.error("Q&A failed.")
            log_error(display_name, "Hybrid Q&A", str(e))

    # Multi-document comparison
    st.header("\U0001F4DD Compare Multiple Papers")
    comparison_files = st.file_uploader("Upload multiple PDFs", type="pdf", accept_multiple_files=True)
    if comparison_files and st.button("Compare Summaries"):
        try:
            docs = [parse_uploaded_pdf(f) for f in comparison_files]
            summaries = [summarize_paper(d, call_claude) for d in docs]
            result = compare_summaries(summaries, call_claude)
            st.subheader("Comparative Summary")
            st.write(result)
            log_event(display_name, "Comparison", str([f.name for f in comparison_files]))
        except Exception as e:
            st.error("Comparison failed.")
            log_error(display_name, "Comparison", str(e))

    # Admin logs
    if st.checkbox("Show Admin Logs"):
        show_admin_logs()
else:
    st.info("Upload a research paper to begin.")
