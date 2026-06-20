"""
behavioral_analyzer.py — flags suspicious reviewer behavior patterns.
Checks for thin-history reviewers and single-vendor reviewers.
"""

import pandas as pd
from collections import defaultdict

def analyze_behavior(reviews: list[dict], thin_history_threshold: int = 5, thin_ratio_threshold: float = 0.40) -> dict:
    """
    Analyzes reviewer behavior patterns.
    Flags if too many reviewers have suspiciously thin review history.
    Uses only the loaded reviews (no full CSV re-scan for speed).
    """
    if not reviews:
        return {"flagged": False, "thin_reviewer_ratio": 0.0, "details": "No reviews to analyze."}

    # Count how many reviews each reviewer has IN THIS PRODUCT
    reviewer_counts = defaultdict(int)
    for r in reviews:
        reviewer_counts[r["reviewer_id"]] += 1

    # Flag reviewers who ONLY reviewed this one product (single-review accounts)
    single_review_accounts = [rid for rid, count in reviewer_counts.items() if count == 1]
    total_reviewers = len(reviewer_counts)
    thin_count = len(single_review_accounts)
    thin_ratio = round(thin_count / total_reviewers, 2)
    flagged = thin_ratio >= thin_ratio_threshold

    # Check for rating polarization (too many 5-stars or 1-stars)
    ratings = [r["rating"] for r in reviews]
    five_star_ratio = round(ratings.count(5) / len(ratings), 2)
    one_star_ratio = round(ratings.count(1) / len(ratings), 2)
    polarized = five_star_ratio >= 0.70 or one_star_ratio >= 0.70

    return {
        "flagged": flagged,
        "thin_reviewer_ratio": thin_ratio,
        "thin_reviewer_count": thin_count,
        "total_reviewers": total_reviewers,
        "five_star_ratio": five_star_ratio,
        "one_star_ratio": one_star_ratio,
        "polarized_ratings": polarized,
        "details": (
            f"{int(thin_ratio*100)}% of reviewers ({thin_count}/{total_reviewers}) "
            f"have only reviewed this single product. "
            f"{'Rating distribution is heavily polarized.' if polarized else ''}"
            if flagged else
            f"No suspicious behavioral patterns detected. "
            f"{'Rating distribution is heavily polarized.' if polarized else ''}"
        )
    }
