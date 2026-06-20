"""
scoring_agent.py — combines signals from all three analyzers
into a single TrustScore from 0 (worst) to 100 (best).
"""

def calculate_trust_score(
    burst_result: dict,
    linguistic_result: dict,
    behavioral_result: dict
) -> dict:
    """
    Weighted scoring formula:
      Burst detection:        30%
      Linguistic fingerprint: 40%
      Behavioral analysis:    30%

    Each signal contributes a penalty (0-100).
    Final score = 100 - total weighted penalty.
    """

    # --- Burst penalty (0-100) ---
    burst_penalty = min(burst_result.get("burst_ratio", 0) * 100, 100)

    # --- Linguistic penalty (0-100) ---
    ling_total = linguistic_result.get("total_reviews", 1)
    ling_flagged = linguistic_result.get("flagged_review_count", 0)
    ling_penalty = min((ling_flagged / ling_total) * 100, 100)

    # --- Behavioral penalty (0-100) ---
    thin_ratio = behavioral_result.get("thin_reviewer_ratio", 0)
    polarized = 1.0 if behavioral_result.get("polarized_ratings", False) else 0.0
    behavioral_penalty = min((thin_ratio * 0.7 + polarized * 0.3) * 100, 100)

    # --- Weighted total penalty ---
    total_penalty = (
        burst_penalty     * 0.30 +
        ling_penalty      * 0.40 +
        behavioral_penalty * 0.30
    )

    trust_score = round(max(0, 100 - total_penalty))

    # --- Label ---
    if trust_score >= 70:
        label = "Trustworthy"
        color = "green"
    elif trust_score >= 40:
        label = "Suspicious"
        color = "orange"
    else:
        label = "Likely Manipulated"
        color = "red"

    return {
        "trust_score": trust_score,
        "label": label,
        "color": color,
        "breakdown": {
            "burst_penalty": round(burst_penalty, 1),
            "linguistic_penalty": round(ling_penalty, 1),
            "behavioral_penalty": round(behavioral_penalty, 1),
            "total_penalty": round(total_penalty, 1)
        }
    }
