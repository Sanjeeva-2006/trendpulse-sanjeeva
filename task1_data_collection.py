import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (required in question)
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords (lowercase for easy matching)
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 25


def get_top_story_ids():
    """Fetch top story IDs from HackerNews"""
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        return response.json()[:500]  # first 500
    except Exception as e:
        print("Error fetching top stories:", e)
        return []


def get_story_details(story_id):
    """Fetch details of a single story"""
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None


def assign_category(title):
    """Assign category based on keywords"""
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for word in keywords:
            if word in title_lower:
                return category

    return None  # ignore if no match


def main():
    story_ids = get_top_story_ids()
    if not story_ids:
        print("No story IDs fetched. Exiting.")
        return

    collected_data = []
    category_count = {cat: 0 for cat in CATEGORY_KEYWORDS}

    for story_id in story_ids:
        story = get_story_details(story_id)
        if not story:
            continue

        category = assign_category(story.get("title"))

        # skip if not matched or already full
        if not category:
            continue
        if category_count[category] >= MAX_PER_CATEGORY:
            continue

        # extract required fields
        record = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_data.append(record)
        category_count[category] += 1

        # check if all categories are filled
        if all(count >= MAX_PER_CATEGORY for count in category_count.values()):
            break

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()