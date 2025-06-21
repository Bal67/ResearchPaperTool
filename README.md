# Research Paper Summarizer

A full-stack AI application for uploading and summarizing research papers using Amazon Bedrock (Claude 3 Sonnet) and Streamlit.

## Demo

https://github.com/user-attachments/assets/825a9ae7-6bdb-4503-88c3-f32581e32093

## Features

- Upload a PDF research paper
- Extracts text using PyMuPDF
- Summarizes content using Claude 3 via Amazon Bedrock
- Secure login with Streamlit session state
- Activity logging for monitoring user actions

## Tech Stack

- Frontend: [Streamlit](https://streamlit.io/)
- Backend: Python + [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- LLM: [Claude 3 Sonnet](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html) via Amazon Bedrock
- PDF Parsing: [PyMuPDF](https://pymupdf.readthedocs.io/)
- Logging: Python `logging` module

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/research-paper-summarizer.git
cd research-paper-summarizer
```

### 2. Install dependencies

If you're using Conda (recommended):

```bash
conda install -c conda-forge streamlit boto3 python-dotenv pymupdf -y
```

Then install any remaining dependencies via pip:

```bash
pip install -r requirements.txt
```

### 3. Configure AWS credentials

You can either:

- Set up your AWS credentials using the AWS CLI (`aws configure`),  
**or**
- Use a `.env` file (optional) if you're not hardcoding credentials:

```env
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_REGION=us-east-1
```

If you're hardcoding the region (as in `bedrock_client.py`), `.env` is not required.

### 4. Run the application

```bash
streamlit run app.py
```

## Usage

1. Log in using the demo account:
   - **Username**: `demo`
   - **Password**: `demo123`
2. Upload a `.pdf` research paper
3. Click "Summarize Paper" to receive a Claude-generated summary
4. All actions are logged to the `logs/` directory

## File Structure

```
research-paper-summarizer/
├── app.py
├── app/
│   ├── auth.py
│   ├── bedrock_client.py
│   ├── monitoring.py
│   └── pdf_parser.py
├── logs/
├── requirements.txt
└── README.md
```

## License

MIT License. Feel free to use, modify, and distribute this project.
