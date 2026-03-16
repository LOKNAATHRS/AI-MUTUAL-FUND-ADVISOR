"""
llm.py — LLM Integration using Ollama (Llama3)
Sends prompts to the local Ollama API and returns generated text.
"""

import requests
import json
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"


def build_prompt(question, age, horizon, risk_level, risk_profile, recommended_funds, context):
    funds_str = ", ".join(recommended_funds[:2])  # only top 2 funds
    return f"""You are a mutual fund advisor. Answer briefly in 2-3 short paragraphs.

Investor: Age {age}, {horizon} yr horizon, {risk_level} risk, {risk_profile} profile.
Funds: {funds_str}

Question: {question}

Give short, direct advice only."""

    return prompt


def query_llm(prompt: str, timeout: int = 300) -> str:
    """
    Send a prompt to Ollama's Llama3 model and return the full response text.
    Falls back to a structured message if Ollama is unavailable.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.5,
            "top_p": 0.9,
            "num_predict": 200,
        },
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response generated.").strip()

    except requests.exceptions.ConnectionError:
        return _fallback_response(prompt)
    except requests.exceptions.Timeout:
        return "⚠️ The LLM took too long to respond. Please try again or simplify your question."
    except Exception as e:
        return f"⚠️ LLM error: {str(e)}"


def _fallback_response(prompt: str) -> str:
    """Return a helpful fallback when Ollama is not running."""
    return (
        "⚠️ **Ollama LLM is not running locally.**\n\n"
        "To enable AI-powered advice:\n"
        "1. Install Ollama from https://ollama.com\n"
        "2. Run: `ollama pull llama3`\n"
        "3. Start the server: `ollama serve`\n"
        "4. Retry your question.\n\n"
        "---\n"
        "**In the meantime, here is general guidance based on your profile:**\n\n"
        "Based on the information you provided, consider the following:\n"
        "- Start with a diversified hybrid or index fund via SIP.\n"
        "- Invest consistently every month regardless of market conditions.\n"
        "- Review your portfolio every 6-12 months.\n"
        "- Ensure you have an emergency fund before investing in equity.\n"
        "- Consult a SEBI-registered investment advisor for personalized advice."
    )
