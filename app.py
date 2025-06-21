import streamlit as st
from app.auth import login
from app.pdf_parser import parse_uploaded_pdf
from app.bedrock_client import call_claude
from app.monitoring import log_event, log_error
from app.comparison import summarize_paper, compare_summaries
from app.qna import (
    init_qa_memory,
    ask_question_with_memory,
    add_to_qa_memory,
)
from app.admin_logs import show_admin_logs


login()
st.title("📚 Research Paper Summarizer")

display_name = st.session_state.get("display_name", "User")
init_qa_memory()

uploaded_files = st.file_uploader(
    "Upload one or more research papers (PDF)", type="pdf", accept_multiple_files=True
)

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
            st.success(f"Summary for {file.name}:")
            st.write(summary)
            log_event(display_name, "Summary", file.name)
        except Exception as e:
            st.error(f"Error summarizing {file.name}: {e}")
            log_error(display_name, f"Summarize {file.name}", str(e))

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
                log_error(display_name, "Comparison", str(e))

    st.markdown("---")
    st.subheader("📑 Section-Based Summarization")
    selected_file = st.selectbox(
        "Select a file", uploaded_files, format_func=lambda f: f.name, key="section_file"
    )

    if selected_file:
        try:
            selected_file.seek(0)
            selected_doc = parse_uploaded_pdf(selected_file)
            sections = selected_doc.sections
            st.info(f"{len(sections)} sections detected.")
            selected_section = st.selectbox(
                "Choose a section", list(sections.keys()), key="section_select"
            )
            if st.button("Summarize Section"):
                prompt = f"Summarize the '{selected_section}' section:\n\n{sections[selected_section][:4000]}"
                summary = call_claude(prompt)
                st.success(f"Summary of {selected_section}:")
                st.write(summary)
                log_event(display_name, "Section Summary", selected_section)
        except Exception as e:
            st.error("Error during section summarization.")
            log_error(display_name, "Section Summarization", str(e))

st.markdown("---")
st.subheader("🧠 Ask Questions")
qa_text = st.text_input("Ask a question about the uploaded paper:")
if st.button("Ask"):
    try:
        if not selected_file:
            raise ValueError("No file selected.")

        selected_file.seek(0)
        doc = parse_uploaded_pdf(selected_file)

        # Prefer full paper; fallback to all sections
        full_text = doc.sections.get("Full Paper")
        if not full_text:
            full_text = "\n\n".join([f"{k}:\n{v}" for k, v in doc.sections.items()])

        if not full_text.strip():
            raise ValueError("Full paper text is empty or not found.")

        answer = ask_question_with_memory(full_text, qa_text)
        add_to_qa_memory(qa_text, answer)

        st.success("Answer:")
        st.write(answer)
        log_event(display_name, "Hybrid Q&A", qa_text)

    except Exception as e:
        st.error(f"Q&A failed: {str(e)}")
        log_error(display_name, "Hybrid Q&A", str(e))


# Admin Tools
st.sidebar.markdown("⚙️ Admin Tools")
if st.sidebar.checkbox("View Logs"):
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if not st.session_state["admin_authenticated"]:
        admin_pass = st.sidebar.text_input("Enter Admin Password", type="password")
        if st.sidebar.button("Authenticate"):
            if admin_pass == st.secrets.get("ADMIN_PASSWORD", ""):
                st.session_state["admin_authenticated"] = True
                st.sidebar.success("Access granted.")
            else:
                st.sidebar.error("Incorrect password.")
    else:
        show_admin_logs(st.session_state.get("username", "guest"))
