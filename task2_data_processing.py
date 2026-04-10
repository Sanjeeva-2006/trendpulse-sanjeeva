import pandas as pd
import os
import json

# Update this if your file has a different date
DATA_FILE = "data/trends_20240115.json"
OUTPUT_FILE = "data/trends_clean.csv"


def main():
    # ---------- Step 1: Load JSON ----------
    if not os.path.exists(DATA_FILE):
        print("File not found. Please check the path.")
        return

    # Load JSON manually first (more reliable than direct read_json)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data)

    except Exception as e:
        print("Error reading JSON file:", e)
        return

    print(f"Loaded {len(df)} stories from {DATA_FILE}")

    # ---------- Step 2: Cleaning ----------

    # Remove duplicates
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # Remove missing values
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Convert data types safely
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

    # Replace NaN with 0 before converting to int
    df["score"] = df["score"].fillna(0).astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # Remove low score entries
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Clean title (extra spaces)
    df["title"] = df["title"].astype(str).str.strip()

    # ---------- Step 3: Save CSV ----------
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved {len(df)} rows to {OUTPUT_FILE}")

    # Category summary
    print("\nStories per category:")
    print(df["category"].value_counts())


if __name__ == "__main__":
    main()