import streamlit as st
from app.auth import login
from app.pdf_parser import parse_uploaded_pdf
from app.bedrock_client import call_claude
from app.monitoring import log_event, log_error
from app.comparison import summarize_paper, compare_summaries
from app.qna import find_relevant_chunk, split_into_chunks
from app.qna import init_qa_memory, ask_question_with_memory, add_to_qa_memory
from app.table_extractor import extract_table_and_figure_text, summarize_figures_and_tables
from app.admin_logs import show_admin_logs

login()

st.title("📚 Research Paper Summarizer")

display_name = st.session_state.get("display_name", "User")
uploaded_files = st.file_uploader("Upload one or more research papers (PDF)", type="pdf", accept_multiple_files=True)

# Multi-document summarization + comparison
if uploaded_files:
    summaries = {}
    for file in uploaded_files:
        try:
            file.seek(0)
            doc = parse_uploaded_pdf(file)
            full_text = "\n".join(doc.sections.values())
            summary_key = f"summary_{file.name}"

            if summary_key not in st.session_state:
                summary = summarize_paper(file.name, full_text)
                st.session_state[summary_key] = summary
            else:
                summary = st.session_state[summary_key]

            summaries[file.name] = summary
            st.success("Summary:")
            st.write(summary)
            log_event(display_name, "Summary", file.name)
        except Exception as e:
            st.error(f"Error summarizing {file.name}: {e}")
            log_error(display_name, f"Summarize {file.name}", e)

    if len(summaries) > 1:
        st.markdown("---")
        if st.button("Compare All Summaries"):
            try:
                comparison = compare_summaries(summaries)
                st.subheader("🧠 Comparison Summary")
                st.write(comparison)
                log_event(display_name, "Comparison", f"{len(summaries)} papers")
            except Exception as e:
                st.error("Comparison failed.")
                log_error(display_name, "Comparison", e)

# Section-based summarization
if uploaded_files:
    st.markdown("---")
    st.subheader("📑 Section-Based Summarization")
    selected_file = st.selectbox("Select a file", uploaded_files, format_func=lambda f: f.name)
    selected_file.seek(0)
    selected_doc = parse_uploaded_pdf(selected_file)
    sections = selected_doc.sections
    st.info(f"{len(sections)} sections detected.")
    selected_section = st.selectbox("Choose a section", list(sections.keys()))
    if st.button("Summarize Section"):
        try:
            prompt = f"Summarize the '{selected_section}' section:\n\n{sections[selected_section][:4000]}"
            summary = call_claude(prompt)
            st.success(f"Summary of {selected_section}:")
            st.write(summary)
            log_event(display_name, "Section Summary", selected_section)
        except Exception as e:
            st.error("Error during section summarization.")
            log_error(display_name, "Section Summarization", e)


# 🔁 Hybrid Q&A (Semantic Search + Memory)
st.markdown("---")
st.subheader("🧠 Ask Questions (Hybrid: Memory + Semantic)")
init_qa_memory()
qa_text = st.text_input("Ask a question about the uploaded paper:")
if st.button("Ask"):
    try:
        selected_file.seek(0)
        doc = parse_uploaded_pdf(selected_file)
        full_text = doc.sections.get("Full Paper", "")
        chunks = split_into_chunks(full_text)
        best_chunk = find_relevant_chunk(chunks, qa_text)
        answer = ask_question_with_memory(full_text, qa_text, context_chunk=best_chunk)
        add_to_qa_memory(qa_text, answer)
        st.success("Answer:")
        st.write(answer)
        log_event(display_name, "Hybrid Q&A", qa_text)
    except Exception as e:
        st.error("Q&A failed.")
        log_error(display_name, "Hybrid Q&A", e)

# Admin log viewer
st.sidebar.markdown("⚙️ Admin Tools")
if st.sidebar.checkbox("View Logs"):
    show_admin_logs(st.session_state.get("username", "guest"))
