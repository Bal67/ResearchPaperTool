# Compliance Documentation

## Project Name: Research Paper Summarization Tool

---

## 1. Data Handling Policy

- **User-Uploaded Files**: All uploaded PDF files are processed in-session and are not stored after the session ends.
- **No Persistent Storage**: The application does not write any user data to disk or external databases.
- **Transient Memory**: Only session-based memory is used for summarization and Q&A history.

---

## 2. Privacy and Confidentiality

- **PII Avoidance**: The system does not collect or process personally identifiable information (PII).
- **Content Scope**: Only user-uploaded documents are used as prompt context for the LLM.
- **Session Isolation**: Each user’s session is isolated and inaccessible to others.

---

## 3. AI & LLM Compliance

- **Provider**: Claude (Anthropic) via Amazon Bedrock
- **Region**: Hardcoded to `us-east-1`
- **Content Filtering**: Prompts are strictly scoped to user documents to prevent inappropriate usage.
- **Prompt Engineering**: Structured prompts used to minimize bias, hallucination, and misuse.
- **Token Limits**: Prompt context capped to prevent overloading the model or triggering rate limits.

---

## 4. Security Practices

- **Streamlit Secrets**: AWS credentials and admin passwords are stored in `secrets.toml`, not in code.
- **Authentication**: Custom login system using Streamlit session state; admin logs gated by password.
- **No External Exposure**: No database, S3 bucket, or external file system integration used.

---

## 5. Infrastructure Compliance

- **AWS Bedrock**: All inference operations are handled by Amazon Bedrock, which adheres to:
  - ISO 27001
  - SOC 1, 2, 3
  - GDPR and HIPAA readiness
- **Streamlit Cloud**:
  - Secured with HTTPS
  - Environment secrets are encrypted at rest
  - Session timeout controls user lifecycle

---

## 6. Risk and Limitation Notices

- **Model Limitations**: Claude’s responses are based on input quality. Misinterpretation or summarization errors are possible.
- **User Responsibility**: Users are advised to validate any critical outputs before use in academic or professional settings.
- **Non-Persistence**: Data loss may occur on session expiration; this is by design for privacy.

---

## 7. Audit and Logging

- **Log Storage**: Admin logs are stored only in memory.
- **Access Control**: Logs accessible only with admin password.
- **Log Contents**: Timestamped actions with display names (no PII).

---

## 8. Change Management

- All changes to authentication, logging, or Claude prompt structures must be reviewed for compliance before deployment.
- Future support for persistent logs or databases must include explicit user consent and updated compliance documentation.
