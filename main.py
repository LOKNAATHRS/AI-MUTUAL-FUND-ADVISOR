"""
main.py — FastAPI Backend for Mutual Fund AI Advisor
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Literal
import os

from rag import retrieve_relevant_context
from llm import build_prompt, query_llm
from risk_model import classify_risk_profile, get_profile_description
from fund_recommender import get_recommendations, get_fund_type_names

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Mutual Fund AI Advisor",
    description="AI-powered mutual fund advisor using RAG + Llama3 via Ollama",
    version="1.0.0",
)

# Serve frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# ── Request / Response models ──────────────────────────────────────────────────
class AdvisorRequest(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Investor's age")
    horizon: int = Field(..., ge=1, le=40, description="Investment horizon in years")
    risk_level: Literal["Low", "Medium", "High"] = Field(
        ..., description="Self-reported risk preference"
    )
    question: str = Field(..., min_length=5, max_length=1000, description="User's question")


class FundRecommendation(BaseModel):
    type: str
    reason: str
    allocation: str


class AdvisorResponse(BaseModel):
    risk_profile: str
    profile_description: str
    recommended_funds: list[FundRecommendation]
    advice: str


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the main HTML frontend."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index_path)


@app.post("/api/advisor", response_model=AdvisorResponse)
async def get_advice(request: AdvisorRequest):
    """
    Main advisor endpoint.
    1. Classify risk profile
    2. Get fund recommendations
    3. Retrieve relevant RAG context
    4. Build prompt and query LLM
    5. Return structured response
    """
    # Step 1: Risk profiling
    risk_profile = classify_risk_profile(
        age=request.age,
        horizon=request.horizon,
        risk_level=request.risk_level,
    )
    profile_description = get_profile_description(risk_profile)

    # Step 2: Fund recommendations
    recommendations = get_recommendations(risk_profile)
    fund_names = get_fund_type_names(risk_profile)

    # Step 3: RAG — retrieve relevant knowledge
    context = retrieve_relevant_context(
        question=request.question,
        risk_profile=risk_profile,
        top_k=3,
    )

    # Step 4: Build prompt and query LLM
    prompt = build_prompt(
        question=request.question,
        age=request.age,
        horizon=request.horizon,
        risk_level=request.risk_level,
        risk_profile=risk_profile,
        recommended_funds=fund_names,
        context=context,
    )
    advice = query_llm(prompt)

    # Step 5: Return response
    return AdvisorResponse(
        risk_profile=risk_profile,
        profile_description=profile_description,
        recommended_funds=[FundRecommendation(**f) for f in recommendations],
        advice=advice,
    )


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Mutual Fund AI Advisor"}


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
