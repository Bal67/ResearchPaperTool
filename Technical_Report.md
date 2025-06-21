# 📝 Technical Report

## Project Title: Research Paper Summarization Tool Using Amazon Bedrock and Streamlit

---

## 1. Abstract

This project presents a full-stack AI application that allows users to upload research papers in PDF format, summarize the content (both full paper and by section), ask questions about the paper, and compare multiple documents. The application leverages Amazon Bedrock with Anthropic Claude for natural language processing and is deployed via Streamlit Cloud for accessibility.

---

## 2. Introduction

Scientific literature is growing exponentially, making it challenging for researchers and students to keep up. This tool addresses the need for rapid comprehension by combining AI summarization, semantic search, and interactive Q&A, with an easy-to-use interface. The system ensures secure access and offers admin features for oversight.

---

## 3. System Architecture

### 3.1 Components
- **Frontend**: Built using Streamlit.
- **Backend**:
  - Claude on Bedrock for summarization and Q&A.
  - PDF parsing with PyMuPDF.
  - Session-based login and admin logging.

### 3.2 Architecture Diagram
```
User --> Streamlit Frontend --> PDF Parser --> Claude (via Bedrock)
                           ↘--> Q&A Memory --> Logs (Admin Only)
```

---

## 4. Implementation

### 4.1 Features
- Full paper summarization using Claude.
- Section detection and selective summarization.
- Question answering using hybrid semantic and memory-based approach.
- Multi-document upload and comparative summarization.
- Admin-only log viewer with password protection.

### 4.2 Claude Integration
All prompts are passed through Amazon Bedrock’s Claude endpoint using `boto3`. Summaries and answers are streamed back and presented in real-time.

---

## 5. Security and Privacy

- Admin access protected via Streamlit sidebar with password check.
- AWS credentials and configuration handled securely via `secrets.toml`.
- No user data or document content is stored after session ends.
- Complies with AWS Bedrock privacy standards.

---

## 6. Performance

- Summarization runs in under 3 seconds per section on average.
- Q&A memory supports dynamic context and past conversation recall.
- The chunking and fuzzy matching mechanism ensures relevant context selection for Q&A.

---

## 7. Deployment

- Application is hosted on [Streamlit Cloud](https://streamlit.io/cloud).
- GitHub integration ensures continuous updates.
- Instructions provided for `.streamlit/secrets.toml` to securely manage credentials.

---

## 8. Conclusion

This project demonstrates the integration of LLMs into research workflows, reducing cognitive overload while maintaining accessibility, security, and interactive capabilities. The modularity of the codebase also enables future extensions such as citation extraction, translation, and study-guide generation.