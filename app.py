"""
app.py — TrustScore Streamlit dashboard.
Wires all pipeline modules into an interactive UI.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_reviews, get_all_product_ids
from analyzers.burst_detector import detect_burst
from analyzers.linguistic_fingerprinter import fingerprint_reviews
from analyzers.behavioral_analyzer import analyze_behavior
from agents.scoring_agent import calculate_trust_score
from agents.explanation_agent import generate_explanation

st.set_page_config(page_title="TrustScore", page_icon="🔍", layout="wide")

st.title(" TrustScore - Fake Review Detector")
st.caption("AI-powered review authenticity analysis using burst detection, linguistic fingerprinting, and behavioral analysis.")

# --- Sidebar ---
st.sidebar.header("Select a Product")
with st.sidebar:
    with st.spinner("Loading product list..."):
        product_ids = get_all_product_ids(top_n=50)
    selected_product = st.selectbox("Product ID", product_ids)
    max_reviews = st.slider("Max reviews to analyze", 50, 200, 200, step=50)
    run_button = st.button("Analyze", type="primary", use_container_width=True)

if run_button:
    with st.spinner("Loading reviews..."):
        reviews = load_reviews(selected_product, max_reviews=max_reviews)

    if not reviews:
        st.error("No reviews found for this product.")
        st.stop()

    st.subheader(f"Product: `{selected_product}` — {len(reviews)} reviews analyzed")

    # --- Run pipeline ---
    with st.spinner("Running burst detection..."):
        burst = detect_burst(reviews)

    with st.spinner("Running linguistic fingerprinting (may take ~10s)..."):
        linguistic = fingerprint_reviews(reviews)

    with st.spinner("Running behavioral analysis..."):
        behavioral = analyze_behavior(reviews)

    with st.spinner("Calculating TrustScore..."):
        score = calculate_trust_score(burst, linguistic, behavioral)

    with st.spinner("Generating explanation..."):
        explanation = generate_explanation(burst, linguistic, behavioral, score)

    # --- Score display ---
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        color_map = {"green": "normal", "orange": "inverse", "red": "inverse"}
        st.metric("TrustScore", f"{score['trust_score']} / 100", delta=score['label'])

    with col2:
        st.metric("Burst Penalty", f"{score['breakdown']['burst_penalty']}")

    with col3:
        st.metric("Linguistic Penalty", f"{score['breakdown']['linguistic_penalty']}")

    # --- Explanation ---
    st.divider()
    if score["color"] == "green":
        st.success(f"✅ {explanation}")
    elif score["color"] == "orange":
        st.warning(f"⚠️ {explanation}")
    else:
        st.error(f"🚨 {explanation}")

    # --- Analyzer breakdown ---
    st.divider()
    st.subheader("Analyzer Breakdown")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Burst Detection**")
        st.write(f"Flagged: {'🔴 Yes' if burst['flagged'] else '🟢 No'}")
        st.write(burst["details"])

    with col_b:
        st.markdown("**Linguistic Fingerprinting**")
        st.write(f"Flagged: {'🔴 Yes' if linguistic['flagged'] else '🟢 No'}")
        st.write(linguistic["details"])

    with col_c:
        st.markdown("**Behavioral Analysis**")
        st.write(f"Flagged: {'🔴 Yes' if behavioral['flagged'] else '🟢 No'}")
        st.write(behavioral["details"])

    # --- Burst chart ---
    st.divider()
    st.subheader("Review Volume Over Time")
    df = pd.DataFrame(reviews)
    df["date"] = pd.to_datetime(df["date"])
    daily = df.groupby(df["date"].dt.date).size().reset_index(name="count")
    fig = px.bar(daily, x="date", y="count", title="Reviews per Day",
                 labels={"date": "Date", "count": "Number of Reviews"})
    st.plotly_chart(fig, use_container_width=True)

    # --- Suspicious reviews table ---
    st.divider()
    st.subheader("Flagged Reviews (Linguistic Cluster)")
    flagged_ids = set(linguistic.get("flagged_review_ids", []))
    flagged_df = pd.DataFrame([r for r in reviews if r["review_id"] in flagged_ids])
    if not flagged_df.empty:
        st.dataframe(
            flagged_df[["review_id", "reviewer_id", "rating", "date", "summary", "text"]],
            use_container_width=True
        )
    else:
        st.info("No flagged reviews to display.")

else:
    st.info("👈 Select a product from the sidebar and click Analyze to begin.")
