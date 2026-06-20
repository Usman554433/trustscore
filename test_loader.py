from utils.data_loader import load_reviews, get_all_product_ids
from analyzers.burst_detector import detect_burst
from analyzers.linguistic_fingerprinter import fingerprint_reviews
from analyzers.behavioral_analyzer import analyze_behavior
from agents.scoring_agent import calculate_trust_score
from agents.explanation_agent import generate_explanation

ids = get_all_product_ids(top_n=5)
reviews = load_reviews(ids[0])

burst      = detect_burst(reviews)
linguistic = fingerprint_reviews(reviews)
behavioral = analyze_behavior(reviews)
score      = calculate_trust_score(burst, linguistic, behavioral)
explanation = generate_explanation(burst, linguistic, behavioral, score)

print("=== TrustScore Result ===")
print(f"Score:     {score['trust_score']} / 100")
print(f"Label:     {score['label']}")
print(f"Breakdown: {score['breakdown']}")
print(f"\n=== Explanation ===")
print(explanation)
