"""
data_loader.py — loads and normalizes the Amazon Fine Food Reviews CSV.
Works both locally (from data/Reviews.csv) and on Streamlit Cloud
(downloads from GitHub releases or falls back to a sample).
"""

import pandas as pd
import os

DATA_PATH = "data/Reviews.csv"
SAMPLE_URL = "https://raw.githubusercontent.com/Usman554433/trustscore/main/data/sample_reviews.csv"

def _load_df() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.read_csv(SAMPLE_URL)

def load_reviews(product_id: str, max_reviews: int = 200) -> list[dict]:
    df = _load_df()
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
    df = _load_df()
    return df["ProductId"].value_counts().head(top_n).index.tolist()

def get_reviewer_history(reviewer_id: str) -> int:
    df = _load_df()
    return len(df[df["UserId"] == reviewer_id])
