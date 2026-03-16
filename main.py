from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"


@app.post("/api/advisor")
async def advisor(
    age: int = Form(...),
    horizon: int = Form(...),
    risk_level: str = Form(...),
    question: str = Form(...)
):

    prompt = f"""
You are an AI financial advisor.

User Age: {age}
Investment Horizon: {horizon} years
Risk Level: {risk_level}

User Question:
{question}

Explain clearly.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    answer = data.get("response", "No AI response.")

    return {"answer": answer}


# serve frontend
BASE_DIR = os.path.dirname(__file__)

app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True),
    name="frontend"
)