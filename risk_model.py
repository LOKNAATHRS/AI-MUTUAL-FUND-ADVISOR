"""
risk_model.py — Risk Profiling Module
Classifies an investor into Conservative, Moderate, or Aggressive
based on age, investment horizon, and self-reported risk level.
"""


def classify_risk_profile(age: int, horizon: int, risk_level: str) -> str:
    """
    Classify the investor's risk profile.

    Scoring system:
    - Age contributes a score (younger = higher risk tolerance)
    - Horizon contributes a score (longer = higher risk tolerance)
    - Self-reported risk level adds a direct weight

    Returns: "Conservative", "Moderate", or "Aggressive"
    """
    score = 0

    # --- Age scoring ---
    if age < 30:
        score += 3
    elif age < 40:
        score += 2
    elif age < 55:
        score += 1
    else:
        score += 0  # Near retirement — conservative

    # --- Horizon scoring ---
    if horizon >= 10:
        score += 3
    elif horizon >= 5:
        score += 2
    elif horizon >= 3:
        score += 1
    else:
        score += 0  # Short-term — conservative

    # --- Self-reported risk level ---
    risk_weights = {
        "low": 0,
        "medium": 2,
        "high": 3,
    }
    score += risk_weights.get(risk_level.lower(), 1)

    # --- Classification ---
    if score <= 3:
        return "Conservative"
    elif score <= 6:
        return "Moderate"
    else:
        return "Aggressive"


def get_profile_description(profile: str) -> str:
    """Return a human-readable description of the risk profile."""
    descriptions = {
        "Conservative": (
            "You prefer capital preservation over high returns. "
            "Your portfolio should prioritize stability and regular income."
        ),
        "Moderate": (
            "You are comfortable with some market fluctuations in pursuit of "
            "balanced growth. A mix of equity and debt suits your profile."
        ),
        "Aggressive": (
            "You can tolerate significant short-term volatility in exchange for "
            "potentially high long-term returns. Equity-heavy portfolios suit you."
        ),
    }
    return descriptions.get(profile, "")


if __name__ == "__main__":
    # Quick test
    for age, horizon, risk in [(25, 15, "high"), (45, 5, "medium"), (60, 2, "low")]:
        profile = classify_risk_profile(age, horizon, risk)
        print(f"Age={age}, Horizon={horizon}, Risk={risk} → {profile}")
