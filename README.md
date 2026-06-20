# TrustScore — Fake Review Detector

AI-powered review authenticity analysis using burst detection, linguistic fingerprinting, and behavioral analysis.

## Live Demo
https://trustscore-usman.streamlit.app

## How it works
1. Burst Detection — flags abnormal volume spikes in review dates
2. Linguistic Fingerprinting — uses sentence embeddings + DBSCAN to detect reviews written by the same source
3. Behavioral Analysis — flags reviewers with suspiciously thin history
4. Scoring Agent — combines signals into a weighted TrustScore (0–100)
5. Explanation Agent — Llama 3 via Groq generates a plain-English summary

## Stack
- Python 3.12
- Streamlit
- sentence-transformers (all-MiniLM-L6-v2)
- scikit-learn (DBSCAN)
- Groq API (Llama 3)
- Plotly
- Dataset: Amazon Fine Food Reviews (Kaggle)

## Setup
```bash
git clone https://github.com/Usman554433/trustscore
cd trustscore
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
