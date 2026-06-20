"""
burst_detector.py — detects abnormal spikes in review submission dates.
Flags products where a large % of reviews were posted in a short window.
"""

from collections import defaultdict

def detect_burst(reviews: list[dict], window_days: int = 3, threshold: float = 0.30) -> dict:
    """
    Checks if more than `threshold` % of reviews were posted
    within any `window_days` rolling window.
    Returns a result dict with flag, score, and details.
    """
    if not reviews:
        return {"flagged": False, "burst_ratio": 0.0, "details": "No reviews to analyze."}

    # Group reviews by date
    date_counts = defaultdict(int)
    for r in reviews:
        day = r["date"].date()
        date_counts[day] += 1

    sorted_dates = sorted(date_counts.keys())
    total = len(reviews)
    max_burst = 0
    burst_window = None

    # Sliding window
    for i, start in enumerate(sorted_dates):
        count = 0
        for date in sorted_dates[i:]:
            if (date - start).days <= window_days:
                count += date_counts[date]
            else:
                break
        if count > max_burst:
            max_burst = count
            burst_window = start

    burst_ratio = round(max_burst / total, 2)
    flagged = burst_ratio >= threshold

    return {
        "flagged": flagged,
        "burst_ratio": burst_ratio,
        "burst_count": max_burst,
        "total_reviews": total,
        "burst_window_start": str(burst_window),
        "details": (
            f"{int(burst_ratio*100)}% of reviews ({max_burst}/{total}) were posted "
            f"within a {window_days}-day window starting {burst_window}."
            if flagged else "No abnormal review burst detected."
        )
    }
