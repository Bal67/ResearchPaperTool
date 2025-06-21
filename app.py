import streamlit as st
from app.auth import login
from app.pdf_parser import parse_uploaded_pdf
from app.bedrock_client import call_claude
from app.monitoring import log_event
from app.token_utils import estimate_tokens

login()  # API key + login gate

st.title("Research Paper Summarizer")

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")

if uploaded_file:
    st.info("Extracting and analyzing the document...")
    parsed = parse_uploaded_pdf(uploaded_file)
    section_texts = parsed.sections

    if not section_texts:
        st.error("No sections detected.")
    else:
        st.success(f"{len(section_texts)} sections detected.")
        total_token_estimate = estimate_tokens(" ".join(section_texts.values()))
        st.info(f"Estimated total tokens: {total_token_estimate:,}")

        if st.button("Summarize All Sections"):
            summaries = {}
            for section_title, section_text in section_texts.items():
                st.markdown(f"#### Summarizing: {section_title}")
                prompt = f"""You are an AI assistant. Summarize the following section of a research paper in plain English:\n\nSection: {section_title}\n\nContent:\n{section_text[:4000]}"""
                try:
                    summary = call_claude(prompt)
                    summaries[section_title] = summary
                    log_event("demo", "Summarized Section", section_title)
                    st.markdown(f"**{section_title} Summary:**")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error summarizing {section_title}: {str(e)}")
