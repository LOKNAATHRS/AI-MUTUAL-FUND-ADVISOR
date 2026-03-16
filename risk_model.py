def risk_profile(age, horizon, risk_level):
    """Compute a normalized risk profile string used for fund recommendations."""
 
    # Normalize risk input (e.g. "High", "high", "HIGH", "moderate")
    risk_level = str(risk_level or "").strip().lower()
 
    score = 0
 
    if age < 30:
        score += 2
    elif age < 50:
        score += 1
 
    if horizon > 7:
        score += 2
    elif horizon > 3:
        score += 1
 
    if risk_level == "high":
        score += 2
    # Fix: added "moderate" as a valid alias alongside "medium" / "med"
    elif risk_level in ("medium", "med", "moderate"):
        score += 1
 
    # Map score to return values that match the fund recommender keys
    if score >= 5:
        return "High Risk"
    elif score >= 3:
        return "Moderate Risk"
    else:
        return "Low Risk"
 