from app.bedrock_client import call_claude

def summarize_paper(title: str, text: str) -> str:
    prompt = f"""You are an academic summarization assistant. Summarize the following research paper in plain English. Focus on the research question, methods, and findings.

Title: {title}
Content:
{text[:5000]}"""
    
    return call_claude(prompt)


def compare_summaries(summary_dict: dict) -> str:
    summary_text = "\n\n".join([f"{title}:\n{summary}" for title, summary in summary_dict.items()])
    prompt = f"""You are an expert research assistant. Given the following paper summaries, compare and contrast them. 
    
    Highlight:
    - Year of publication
    - Main research questions
    - Similarities in research questions or methods
    - Key differences in findings
    - Notable strengths or weaknesses
    - Overall Findings and Results

Summaries:
{summary_text}
"""
    return call_claude(prompt)
