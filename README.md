# AI Mutual Fund Advisor

A simple FastAPI-based backend + static frontend that provides mutual fund recommendations and generates an AI-driven explanation using an LLM.

## 🚀 Quick Start

### 1) Ensure dependencies are installed

From the repo root:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run the app

```powershell
venv\Scripts\python -m uvicorn main:app --reload
```

Then open: http://localhost:8000

### 3) LLM Backend (Ollama)

The `llm.py` client expects an Ollama server running on `http://localhost:11434` and a model named `llama3`.
If you are not running Ollama, the AI answer generation will fail.

## 🧠 Files

- `main.py` - FastAPI server + static frontend mount
- `frontend/index.html` - UI for collecting user inputs
- `rag.py` - Simple keyword-based retrieval for knowledge context
- `risk_model.py` - Computes a risk profile from inputs
- `fund_recommender.py` - Maps risk profile to sample funds
- `llm.py` - Calls an LLM endpoint to generate an explanation

## 🛠️ Fixes Included

- Corrected FastAPI endpoint to accept form data
- Normalized risk input and matched it with fund recommendation keys
- Added `requirements.txt` for easy setup
