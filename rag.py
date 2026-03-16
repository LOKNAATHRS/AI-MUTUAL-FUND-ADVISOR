"""
rag.py — Retrieval-Augmented Generation module
Loads the mutual fund knowledge base and retrieves relevant sections
based on keyword matching with the user's question.
"""

import os
import re
from typing import List

KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "data", "mutual_funds.txt")

# Section separator pattern
SECTION_PATTERN = re.compile(r"--- (.+?) ---")


def load_knowledge_base() -> dict:
    """Load and parse the knowledge base into sections."""
    sections = {}
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    parts = re.split(r"--- .+? ---", content)
    headers = SECTION_PATTERN.findall(content)

    for header, body in zip(headers, parts[1:]):
        sections[header.strip()] = body.strip()

    return sections


def retrieve_relevant_context(question: str, risk_profile: str = "", top_k: int = 2) -> str:
    """
    Retrieve top_k most relevant knowledge base sections for the given question.
    Uses simple keyword overlap scoring.
    """
    sections = load_knowledge_base()

    # Build keyword set from question + risk profile
    combined_query = (question + " " + risk_profile).lower()
    query_words = set(re.findall(r"\b\w{3,}\b", combined_query))

    # Score each section
    scored = []
    for title, body in sections.items():
        section_text = (title + " " + body).lower()
        section_words = set(re.findall(r"\b\w{3,}\b", section_text))
        overlap = len(query_words & section_words)
        scored.append((overlap, title, body))

    # Sort descending by overlap score
    scored.sort(key=lambda x: x[0], reverse=True)

    # Take top_k sections
    retrieved: List[str] = []
    for score, title, body in scored[:top_k]:
        retrieved.append(f"[{title}]\n{body}")

    return "\n\n".join(retrieved) if retrieved else "No specific context found."


if __name__ == "__main__":
    q = "What is SIP and how does it work?"
    ctx = retrieve_relevant_context(q)
    print(ctx)
