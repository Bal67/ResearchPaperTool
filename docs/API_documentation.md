# API Documentation

## Overview

This documentation outlines the key internal APIs used within the Research Paper Summarization Tool application. These APIs are not public REST endpoints but are function-level integrations within the Python codebase.

---

## Claude Integration

### call_claude(prompt: str) -> str

- **Description**: Sends a prompt to the Claude model via Amazon Bedrock and returns the response.
- **Input**: A full prompt string (including instructions and context).
- **Output**: Claude's response as a plain string.
- **Location**: `app/bedrock_client.py`

---

## PDF Parsing

### parse_uploaded_pdf(uploaded_file) -> Document

- **Description**: Parses an uploaded PDF file into structured sections using PyMuPDF.
- **Input**: A file-like PDF object (from Streamlit uploader).
- **Output**: A `Document` object with `.sections: dict[str, str]`
- **Location**: `app/pdf_parser.py`

---

## Summarization

### summarize_paper(filename: str, text: str) -> str

- **Description**: Generates a full-paper summary using Claude.
- **Input**: Filename (for labeling) and the full text of the paper.
- **Output**: A summary string.
- **Location**: `app/comparison.py`

---

## Multi-Document Comparison

### compare_summaries(summaries: dict[str, str]) -> str

- **Description**: Compares summaries of multiple papers and generates a synthesized comparative summary.
- **Input**: A dictionary mapping filenames to their summaries.
- **Output**: A comparison summary string.
- **Location**: `app/comparison.py`

---

## Q&A (Hybrid: Semantic Search + Memory)

### split_into_chunks(text: str, chunk_size: int = 1000) -> list[str]

- **Description**: Splits a long string into smaller overlapping chunks for better context handling.
- **Output**: List of chunk strings.

### find_relevant_chunk(chunks: list[str], question: str) -> str

- **Description**: Scores chunks based on keyword overlap with the user question.
- **Output**: Best-matching chunk string.

### ask_question_with_memory(full_text: str, question: str, context_chunk: str) -> str

- **Description**: Assembles a prompt combining history, context, and current question.
- **Output**: Claude’s answer string.

### init_qa_memory() and add_to_qa_memory(q, a)

- **Description**: Manage in-memory session-based Q&A context.
- **Location**: `app/qna.py`

---

## Monitoring

### log_event(user: str, action: str, detail: str)

- **Description**: Records a successful interaction for auditing.
- **Location**: `app/monitoring.py`

### log_error(user: str, action: str, error: str)

- **Description**: Logs an error message with traceback or exception string.
- **Location**: `app/monitoring.py`

---

## Admin Logs

### show_admin_logs(user: str)

- **Description**: Displays recent event and error logs if the user is an admin.
- **Location**: `app/admin_logs.py`

---

## Authentication

### login()

- **Description**: Displays Streamlit login UI, sets session state with username and role.
- **Location**: `app/auth.py`