import fitz  # PyMuPDF
import re

def parse_uploaded_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    return extract_sections(full_text)


def extract_sections(text):
    sections = {}

    # Regex pattern: uppercase headings on their own line (e.g., ABSTRACT, INTRODUCTION)
    pattern = re.compile(r"\n([A-Z][A-Z\s]{3,40})\n")

    parts = pattern.split(text)

    if len(parts) < 3:
        return type("ParsedPDF", (), {"sections": {"Full Paper": text}})()

    # Assemble sections
    for i in range(1, len(parts) - 1, 2):
        header = parts[i].strip().title()  
        content = parts[i + 1].strip()

        if len(content) > 100:
            sections[header] = content

    return type("ParsedPDF", (), {"sections": sections})()
