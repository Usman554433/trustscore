"""
linguistic_fingerprinter.py — detects reviews that are suspiciously
similar in writing style, suggesting they may come from the same source
despite different account names (review farm signature).
"""

from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def fingerprint_reviews(reviews: list[dict], eps: float = 0.25, min_samples: int = 3) -> dict:
    """
    Generates sentence embeddings for all reviews, then clusters them
    using DBSCAN. Clusters with 3+ reviews are flagged as suspicious.
    Returns flag, suspicious clusters, and details.
    """
    if len(reviews) < 3:
        return {"flagged": False, "suspicious_clusters": 0, "flagged_review_ids": [], "details": "Not enough reviews to analyze."}

    texts = [r["text"] for r in reviews]
    review_ids = [r["review_id"] for r in reviews]

    print("Generating embeddings... (first run downloads ~80MB model, be patient)")
    embeddings = model.encode(texts, show_progress_bar=True)

    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

    # DBSCAN clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine").fit(embeddings)
    labels = clustering.labels_

    # Find suspicious clusters (label != -1 means it's a cluster, not noise)
    cluster_ids = set(labels) - {-1}
    suspicious_clusters = len(cluster_ids)

    flagged_review_ids = []
    for cluster_id in cluster_ids:
        indices = [i for i, l in enumerate(labels) if l == cluster_id]
        flagged_review_ids.extend([review_ids[i] for i in indices])

    flagged = suspicious_clusters > 0

    return {
        "flagged": flagged,
        "suspicious_clusters": suspicious_clusters,
        "flagged_review_count": len(flagged_review_ids),
        "total_reviews": len(reviews),
        "flagged_review_ids": flagged_review_ids,
        "details": (
            f"{suspicious_clusters} suspicious cluster(s) found — "
            f"{len(flagged_review_ids)} reviews share near-identical writing style."
            if flagged else "No suspicious linguistic patterns detected."
        )
    }
