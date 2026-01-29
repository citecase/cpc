import feedparser
import json
import os
from datetime import datetime

FEEDS = [
    "https://www.livelaw.in/google_feeds.xml",
    "https://www.verdictum.in/feed",
    "https://caseciter.com/rss",
    "https://www.scconline.com/blog/feed/"
]
KEYWORDS = ["cpc", "civil procedure"]
JSON_FILE = "cpc.json"
MD_FILE = "cpc.md"

def fetch_and_filter():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                all_entries = json.load(f)
            except:
                all_entries = []
    else:
        all_entries = []

    existing_links = {item['link'] for item in all_entries}
    new_found = False

    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            text = (entry.title + " " + entry.get('summary', '')).lower()
            if any(kw in text for kw in KEYWORDS) and entry.link not in existing_links:
                all_entries.insert(0, {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get('published', datetime.now().strftime("%d %b %Y")),
                    "source": url
                })
                existing_links.add(entry.link)
                new_found = True

    if new_found:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(all_entries, f, indent=4)
        with open(MD_FILE, "w", encoding="utf-8") as f:
            f.write("# CPC & Civil Procedure Updates\n\n")
            for item in all_entries:
                f.write(f"### [{item['title']}]({item['link']})\n- {item['published']}\n\n")

if __name__ == "__main__":
    fetch_and_filter()
