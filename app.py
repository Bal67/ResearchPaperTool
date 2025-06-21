import streamlit as st
from app.auth import login
from app.monitoring import log_event
from app.pdf_parser import parse_uploaded_pdf
from app.bedrock_client import call_claude

login()  # Require login before continuing

st.title("Research Paper Summarizer")

uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")
if uploaded_file:
    st.info("Parsing PDF...")
    full_text = parse_uploaded_pdf(uploaded_file)

    if not full_text or len(full_text.strip()) < 100:
        st.error("Unable to extract meaningful text from the PDF.")
    else:
        st.success("Document parsed successfully.")
        if st.button("Summarize Paper"):
            log_event("demo", "Summarize", uploaded_file.name)
            prompt = f"""You are an AI assistant. Summarize this research paper in plain English. Highlight the research question, methodology, and key findings:\n\n{full_text[:5000]}"""
            response = call_claude(prompt)

            st.subheader("Claude's Summary")
            st.write(response)
