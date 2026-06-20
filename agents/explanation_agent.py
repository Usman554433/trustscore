"""
explanation_agent.py — uses Groq (Llama 3) to convert raw analyzer
flags into a plain-English consumer-facing explanation.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explanation(
    burst_result: dict,
    linguistic_result: dict,
    behavioral_result: dict,
    score_result: dict
) -> str:
    """
    Sends analyzer results to Llama 3 via Groq and returns
    a 3-4 sentence plain-English explanation of the TrustScore.
    """

    prompt = f"""You are a consumer protection AI that explains fake review analysis results in plain English.

Here are the analysis results for a product:

TRUST SCORE: {score_result['trust_score']} / 100 ({score_result['label']})

BURST DETECTION:
- Flagged: {burst_result['flagged']}
- {burst_result['details']}

LINGUISTIC FINGERPRINTING:
- Flagged: {linguistic_result['flagged']}
- {linguistic_result['details']}

BEHAVIORAL ANALYSIS:
- Flagged: {behavioral_result['flagged']}
- {behavioral_result['details']}

Write a 3-4 sentence explanation for a regular consumer explaining why this product received this TrustScore.
Be specific, use the actual numbers, and be direct about what the red flags mean.
Do NOT use bullet points. Write in plain paragraph form only.
Do NOT start with "I" or "As an AI".
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
