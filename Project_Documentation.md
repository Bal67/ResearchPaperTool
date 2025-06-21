# 📄 Technical Documentation

## Architecture Overview
- **Frontend**: Streamlit app (Python)
- **Backend Services**:
  - PDF parsing using PyMuPDF (fitz)
  - Summarization and Q&A via Claude on Amazon Bedrock
  - Monitoring and logging (in-memory, optionally exportable)
- **Authentication**: Custom login using Streamlit session state
- **Deployment**: Hosted via Streamlit Cloud

## File Structure
```
ResearchPaperTool/
├── app.py                # Main Streamlit app
├── app/
│   ├── auth.py          # Login handling
│   ├── bedrock_client.py# Claude integration
│   ├── comparison.py    # Multi-PDF summary comparison
│   ├── monitoring.py    # Logging and monitoring
│   ├── pdf_parser.py    # PDF parsing and section detection
│   ├── qna.py           # Q&A logic (hybrid semantic + memory)
│   └── admin_logs.py    # Admin viewer
├── tests/               # Unit tests
├── requirements.txt     # Dependencies
└── README.md            # Project overview
```

---

# 🔌 API Documentation

### Claude Prompting API
- **Function**: `call_claude(prompt: str) -> str`
- **Input**: Prompt containing context and question
- **Output**: Claude's response as string

### PDF Parser API
- **Function**: `parse_uploaded_pdf(uploaded_file) -> Document`
- **Returns**: Parsed object with `.sections` dictionary

### Question Answering API
- **Function**: `ask_question_with_memory(text, question, context_chunk=None)`
- **Handles**: Context selection, Claude prompt generation, memory logging

### Admin Logging APIs
- `log_event(user, action, detail)`
- `log_error(user, action, error)`
- `show_admin_logs(user)`

---

# 🚀 Deployment Guide

## 1. Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 2. Streamlit Cloud
1. Push repo to GitHub
2. In Streamlit Cloud dashboard:
   - Connect GitHub repo
   - Add secrets in **App > Settings > Secrets**:

```toml
AWS_ACCESS_KEY_ID = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
AWS_REGION = "us-east-1"
ADMIN_PASSWORD = "your_admin_password"
```

---

# 👩‍💻 User Manual

## Step 1: Login
- Enter username and password
- Admin users can access logs via sidebar

## Step 2: Upload PDF(s)
- Upload one or multiple PDFs
- Full summaries will generate automatically

## Step 3: Interact
- Choose sections to summarize
- Ask Claude questions using the input box
- Compare summaries across documents

## Step 4: Admin Logs
- Use sidebar to enter password and unlock log viewer

---

# 🔐 Security & Responsibility

## Security Measures
- Secrets stored via Streamlit’s built-in secrets manager
- Admin tools protected by password
- No persistent data storage

## Privacy Controls
- No user tracking or PII storage
- Session-based state handling

## Responsible AI Practices
- Claude is used with controlled, purpose-bound prompts
- Input limited to user-uploaded documents

## Compliance
- Claude via Amazon Bedrock ensures AWS-grade compliance
- No third-party transmission of data outside Bedrock