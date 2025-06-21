import fitz  # PyMuPDF
from app.bedrock_client import call_claude

def extract_table_and_figure_text(uploaded_file) -> list:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    results = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                text = " ".join([span["text"] for line in block["lines"] for span in line["spans"]])
                text_lower = text.lower()
                if any(kw in text_lower for kw in ["table", "figure", "fig.", "caption"]):
                    results.append(text.strip())

    return results


def summarize_figures_and_tables(texts: list) -> str:
    if not texts:
        return "No figure or table content detected in the document."

    joined = "\n\n".join(texts)
    prompt = f"""The following are figure and table captions or descriptions extracted from a research paper. Please summarize the key trends or insights they represent in plain English:\n\n{joined}"""

    return call_claude(prompt)
