# 📚 ResearchPaperTool

An AI-powered research paper assistant that helps users:
- Upload and summarize scientific PDFs
- Get section-specific summaries
- Ask interactive questions about the content
- Compare summaries across multiple documents
- Monitor admin activity securely

Powered by [Amazon Bedrock](https://aws.amazon.com/bedrock/) and [Anthropic Claude](https://www.anthropic.com/index/claude), wrapped in a clean [Streamlit](https://streamlit.io/) interface.

---

## 🔍 Features

- 📄 **Full-paper Summarization**: Upload any research PDF and instantly get a plain-English summary.
- 🧠 **Section-based Summarization**: Select specific sections like "Methods" or "Results" to summarize independently.
- ❓ **Ask Questions**: Ask Claude anything about your uploaded paper with context-aware memory.
- 📊 **Compare Multiple Papers**: Upload several documents and compare their summaries side-by-side.
- 🔒 **Admin Mode**: View user logs and monitor app usage with a password-protected panel.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Bal67/ResearchPaperTool.git
cd ResearchPaperTool
```

### 2. Set Up Dependencies
Install required packages:
```bash
pip install -r requirements.txt
```

Make sure to use Python 3.9+.

### 3. Configure AWS & Claude (via Bedrock)

Create a `.streamlit/secrets.toml` file:

```toml
AWS_ACCESS_KEY_ID = "your_key"
AWS_SECRET_ACCESS_KEY = "your_secret"
AWS_REGION = "us-east-1"
ADMIN_PASSWORD = "your_admin_password"
```

Claude via Bedrock is accessed using `boto3` (no API key required).

---

## 🧪 Running Locally

```bash
streamlit run app.py
```

---

## ☁️ Deployment (Streamlit Cloud)

To deploy:
1. Push your repo to GitHub (remove `.streamlit/secrets.toml` from the repo!)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Paste secrets into **App > Settings > Secrets** (same format as `.toml`)

---

## 🧪 Testing & Coverage

Run all tests:
```bash
coverage run -m unittest discover -s tests
coverage report -m
```

Generate HTML report:
```bash
coverage html
```

---

## 📁 Project Structure

```
ResearchPaperTool/
├── app.py
├── app/
│   ├── auth.py
│   ├── bedrock_client.py
│   ├── comparison.py
│   ├── monitoring.py
│   ├── pdf_parser.py
│   ├── qna.py
│   └── admin_logs.py
├── tests/
│   └── test_core.py
├── requirements.txt
└── README.md
```

---

## 🔐 Security Notes

- Admin logs are protected by a password prompt
- Do **not** commit credentials or `.streamlit/secrets.toml` to version control
- Claude prompts are token-limited (~15k characters per PDF)

---

## 📬 Contact

Created by [@Bal67](https://github.com/Bal67). PRs and feedback welcome.