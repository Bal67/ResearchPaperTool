import fitz  # PyMuPDF
import re
from difflib import get_close_matches

KNOWN_HEADERS = [
    "abstract", "introduction", "background", "related work", "methods",
    "methodology", "materials", "results", "experiments", "discussion",
    "conclusion", "references", "acknowledgements"
]

def extract_text_from_pdf(uploaded_file) -> str:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()

def normalize_line(line: str) -> str:
    line = re.sub(r"[^a-zA-Z ]", "", line.lower()).strip()
    return line

def match_header(line: str) -> str:
    norm = normalize_line(line)
    matches = get_close_matches(norm, KNOWN_HEADERS, n=1, cutoff=0.7)
    return matches[0] if matches else None

def extract_sections(text: str) -> dict:
    lines = text.split("\n")
    sections = {}
    current_section = None
    buffer = []

    for line in lines:
        line_clean = line.strip()
        matched = match_header(line_clean)
        if matched:
            if current_section and buffer:
                sections[current_section] = "\n".join(buffer).strip()
                buffer = []
            current_section = matched
        elif current_section:
            buffer.append(line)

    if current_section and buffer:
        sections[current_section] = "\n".join(buffer).strip()

    return sections

class ParsedPDF:
    def __init__(self, text: str, sections: dict):
        self.text = text
        self.sections = sections

def parse_uploaded_pdf(uploaded_file) -> ParsedPDF:
    raw_text = extract_text_from_pdf(uploaded_file)
    sections = extract_sections(raw_text)

    if not sections:
        sections = {"Full Paper": raw_text}

    return ParsedPDF(text=raw_text, sections=sections)
