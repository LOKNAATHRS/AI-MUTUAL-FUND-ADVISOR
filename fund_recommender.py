"""
fund_recommender.py — Mutual Fund Recommendation Engine
Recommends fund types based on the investor's risk profile.
"""

from typing import List, Dict


FUND_RECOMMENDATIONS: Dict[str, List[Dict]] = {
    "Conservative": [
        {
            "type": "Liquid Funds",
            "reason": "Ideal for short-term parking with minimal risk and easy liquidity.",
            "allocation": "40%",
        },
        {
            "type": "Short-Duration Debt Funds",
            "reason": "Stable returns with low volatility, suitable for 1-3 year goals.",
            "allocation": "35%",
        },
        {
            "type": "Conservative Hybrid Funds",
            "reason": "Small equity component (10-25%) for slight growth with debt stability.",
            "allocation": "25%",
        },
    ],
    "Moderate": [
        {
            "type": "Balanced Advantage / Dynamic Asset Allocation Funds",
            "reason": "Automatically adjusts equity-debt ratio based on market valuation.",
            "allocation": "35%",
        },
        {
            "type": "Large-Cap Equity Funds",
            "reason": "Stable equity growth through top 100 companies.",
            "allocation": "30%",
        },
        {
            "type": "Medium-Duration Debt Funds",
            "reason": "Provides portfolio stability and regular income.",
            "allocation": "20%",
        },
        {
            "type": "NIFTY 50 Index Fund",
            "reason": "Low-cost, passive exposure to India's top 50 companies.",
            "allocation": "15%",
        },
    ],
    "Aggressive": [
        {
            "type": "Flexi-Cap / Multi-Cap Equity Funds",
            "reason": "Broad equity exposure across market caps for maximum long-term growth.",
            "allocation": "35%",
        },
        {
            "type": "Mid-Cap Funds",
            "reason": "Higher growth potential from India's emerging mid-sized companies.",
            "allocation": "25%",
        },
        {
            "type": "Small-Cap Funds",
            "reason": "Maximum growth potential for very long investment horizons.",
            "allocation": "20%",
        },
        {
            "type": "NIFTY NEXT 50 Index Fund",
            "reason": "Passive exposure to the next tier of large-cap companies.",
            "allocation": "15%",
        },
        {
            "type": "ELSS (Tax-Saving Funds)",
            "reason": "Equity growth with Section 80C tax benefits under ₹1.5L limit.",
            "allocation": "5%",
        },
    ],
}


def get_recommendations(risk_profile: str) -> List[Dict]:
    """Return a list of recommended fund types for the given risk profile."""
    return FUND_RECOMMENDATIONS.get(risk_profile, FUND_RECOMMENDATIONS["Moderate"])


def get_fund_type_names(risk_profile: str) -> List[str]:
    """Return just the fund type names as a list."""
    return [f["type"] for f in get_recommendations(risk_profile)]


def format_recommendations(risk_profile: str) -> str:
    """Format recommendations as a readable string."""
    funds = get_recommendations(risk_profile)
    lines = [f"Recommended Funds for {risk_profile} Investor:\n"]
    for fund in funds:
        lines.append(f"  • {fund['type']} ({fund['allocation']}): {fund['reason']}")
    return "\n".join(lines)


if __name__ == "__main__":
    for profile in ["Conservative", "Moderate", "Aggressive"]:
        print(format_recommendations(profile))
        print()
