import pandas as pd
import numpy as np
import os

DATA_FILE = "data/trends_clean.csv"
OUTPUT_FILE = "data/trends_analysed.csv"


def main():
    # ---------- Step 1: Load ----------
    if not os.path.exists(DATA_FILE):
        print("File not found. Please run Task 2 first.")
        return

    try:
        df = pd.read_csv(DATA_FILE)
    except Exception as e:
        print("Error loading CSV:", e)
        return

    if df.empty:
        print("Dataset is empty.")
        return

    print(f"Loaded data: {df.shape}")

    print("\nFirst 5 rows:")
    print(df.head())

    # Ensure required columns exist
    required_cols = ["score", "num_comments", "category", "title"]
    for col in required_cols:
        if col not in df.columns:
            print(f"Missing column: {col}")
            return

    # Convert safely (in case types are wrong)
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0)

    scores = df["score"].values
    comments = df["num_comments"].values

    avg_score = np.mean(scores)
    avg_comments = np.mean(comments)

    print(f"\nAverage score   : {int(avg_score)}")
    print(f"Average comments: {int(avg_comments)}")

    # ---------- Step 2: NumPy Analysis ----------
    print("\n--- NumPy Stats ---")

    print(f"Mean score   : {int(np.mean(scores))}")
    print(f"Median score : {int(np.median(scores))}")
    print(f"Std deviation: {int(np.std(scores))}")
    print(f"Max score    : {int(np.max(scores))}")
    print(f"Min score    : {int(np.min(scores))}")

    # Category with most stories
    category_counts = df["category"].value_counts()
    if not category_counts.empty:
        top_category = category_counts.idxmax()
        print(f"\nMost stories in: {top_category} ({category_counts[top_category]} stories)")

    # Most commented story (safer way)
    if len(df) > 0:
        top_row = df.loc[df["num_comments"].idxmax()]
        print(f"\nMost commented story: \"{top_row['title']}\" — {int(top_row['num_comments'])} comments")

    # ---------- Step 3: New Columns ----------
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    df["is_popular"] = df["score"] > avg_score

    # ---------- Step 4: Save ----------
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()