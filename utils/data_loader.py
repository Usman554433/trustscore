"""
data_loader.py — loads and normalizes the Amazon Fine Food Reviews CSV
into a standard list of review dicts for the TrustScore pipeline.
"""

import pandas as pd

def load_reviews(product_id: str, max_reviews: int = 200) -> list[dict]:
    """
    Loads reviews for a specific product from the dataset.
    Returns a list of normalized review dicts.
    """
    df = pd.read_csv("data/Reviews.csv")

    df = df[df["ProductId"] == product_id].head(max_reviews)

    reviews = []
    for _, row in df.iterrows():
        reviews.append({
            "review_id": str(row["Id"]),
            "product_id": str(row["ProductId"]),
            "reviewer_id": str(row["UserId"]),
            "rating": int(row["Score"]),
            "text": str(row["Text"]),
            "summary": str(row["Summary"]),
            "date": pd.to_datetime(row["Time"], unit="s"),
            "verified": bool(row.get("HelpfulnessNumerator", 0))
        })
    return reviews

def get_all_product_ids(top_n: int = 50) -> list[str]:
    """
    Returns the top N most-reviewed product IDs from the dataset.
    Useful for populating the UI dropdown.
    """
    df = pd.read_csv("data/Reviews.csv")
    top = df["ProductId"].value_counts().head(top_n).index.tolist()
    return top

def get_reviewer_history(reviewer_id: str) -> int:
    """
    Returns total number of reviews a reviewer has across the entire dataset.
    Used by the behavioral analyzer.
    """
    df = pd.read_csv("data/Reviews.csv")
    return len(df[df["UserId"] == reviewer_id])
