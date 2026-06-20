# run this once: python create_sample.py
import pandas as pd

df = pd.read_csv("data/Reviews.csv")
top_ids = df["ProductId"].value_counts().head(10).index.tolist()
sample = df[df["ProductId"].isin(top_ids)]
sample.to_csv("data/sample_reviews.csv", index=False)
print(f"Sample created: {len(sample)} rows, {sample['ProductId'].nunique()} products")
