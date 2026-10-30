import requests
import json
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
NEW_STORIES_URL = "https://hacker-news.firebaseio.com/v0/newstories.json"
headers = {
    "User-Agent": "TrendPulse/1.0"
}
# Category keywords for identifying trending stories
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}
# Function to assign a category based on the story title
def assign_category(title):

    title = title.lower()

    for category_name, keywords in categories.items():

        for keyword in keywords:

            if keyword.lower() in title:
                return category_name

    return None


# Function to fetch an individual story from HackerNews API
def fetch_story(story_id):

    story_url = (
        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    )

    try:
        response = requests.get(
            story_url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        story = response.json()

        if story and story.get("type") == "story":
            return story

    except requests.exceptions.RequestException as error:

        print(f"Failed to fetch story {story_id}: {error}")

    return None
# Fetch the top 500 story IDs from HackerNews
def fetch_story_ids(url):

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        story_ids = response.json()

        return story_ids[:500]

    except requests.exceptions.RequestException as error:

        print(f"Failed to fetch story IDs: {error}")
        return []


# Get the top 500 story IDs
story_ids = fetch_story_ids(TOP_STORIES_URL)

print("Top story IDs fetched:", len(story_ids))
# Fetch story details using multiple threads
def fetch_multiple_stories(story_ids):

    with ThreadPoolExecutor(max_workers=10) as executor:

        results = list(
            executor.map(fetch_story, story_ids)
        )

    # Remove failed or empty responses
    stories = [
        story for story in results
        if story is not None
    ]

    return stories


# Fetch details of the top 500 stories
all_stories = fetch_multiple_stories(story_ids)

print("Successfully fetched stories:", len(all_stories))
# Create empty lists for all five categories
collected_stories = {
    category: [] for category in categories
}
# Track story IDs to avoid duplicates
used_ids = set()

# Collect a maximum of 25 stories per category
for category_index, (category_name, keywords) in enumerate(categories.items()):

    print("Collecting:", category_name)

    for story in all_stories:
        if story["id"] in used_ids:
            continue

        # Stop when the category reaches 25 stories
        if len(collected_stories[category_name]) >= 25:
            break

        title = story.get("title", "").lower()

        # Check whether the title contains a category keyword
        if any(keyword.lower() in title for keyword in keywords):

            story_data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category_name,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "Unknown"),
                "collected_at": datetime.now().isoformat()
            }

            collected_stories[category_name].append(story_data)

    print(
        category_name,
        "stories collected:",
        len(collected_stories[category_name])
    )

    # Wait 2 seconds between categories
    if category_index < len(categories) - 1:
        time.sleep(2)


# Calculate total collected stories
total_stories = sum(
    len(stories) for stories in collected_stories.values()
)

print("Total stories collected:", total_stories)
# Fetch 500 additional story IDs from HackerNews
new_story_ids = fetch_story_ids(NEW_STORIES_URL)

print("Additional story IDs:", len(new_story_ids))


# Fetch details of the additional stories
extra_stories = fetch_multiple_stories(new_story_ids)

print("Additional stories fetched:", len(extra_stories))
# Fill categories that have fewer than 25 stories
for category_index, (category_name, keywords) in enumerate(categories.items()):

    print("\nChecking:", category_name)

    for story in extra_stories:

        # Stop when the category reaches 25 stories
        if len(collected_stories[category_name]) >= 25:
            break

        # Avoid collecting duplicate story IDs
        if story["id"] in used_ids:
            continue

        title = story.get("title", "").lower()

        # Check for matching category keywords
        if any(keyword.lower() in title for keyword in keywords):

            story_data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category_name,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "Unknown"),
                "collected_at": datetime.now().isoformat()
            }

            collected_stories[category_name].append(story_data)
            used_ids.add(story["id"])

    print(
        "Stories collected:",
        len(collected_stories[category_name])
    )

    # Wait 2 seconds between categories
    if category_index < len(categories) - 1:
        time.sleep(2)


# Calculate the final total
total_stories = sum(
    len(stories) for stories in collected_stories.values()
)

print("\nTotal stories collected:", total_stories)
# Combine all category stories into one list
all_collected_stories = []

for category_stories in collected_stories.values():
    all_collected_stories.extend(category_stories)


# Validate required fields
required_fields = [
    "post_id",
    "title",
    "category",
    "score",
    "num_comments",
    "author",
    "collected_at"
]

missing_fields = []

for story in all_collected_stories:
    for field in required_fields:
        if field not in story or story[field] is None:
            missing_fields.append((story.get("post_id"), field))

if missing_fields:
    print("Validation failed!")
    print("Missing fields:", missing_fields)

else:
    print("Validation successful!")
    print("All 7 required fields are available.")


# Create data folder if it does not exist
os.makedirs("data", exist_ok=True)


# Create JSON filename using today's date
file_name = f"trends_{datetime.now().strftime('%Y%m%d')}.json"

file_path = os.path.join("data", file_name)


# Save stories into JSON file
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(
        all_collected_stories,
        file,
        indent=4,
        ensure_ascii=False
    )


print("\nTotal stories saved:", len(all_collected_stories))
print("File saved successfully!")
print("File location:", file_path)
# ==========================================
# Final Summary
# ==========================================

print("\n========== TrendPulse Task 1 Completed ==========")

print("Total stories collected:", total_stories)

for category_name, stories in collected_stories.items():
    print(f"{category_name}: {len(stories)} stories")

print("JSON file:", file_path)

print("=================================================")