import csv
import argparse
import feedparser
import requests
from urllib.parse import urlparse

CSV_FILE = "ohio.csv"

def fetch_feed_metadata(url):
    try:
        response = requests.get(url, timeout=10)
        feed = feedparser.parse(response.content)
        if feed.bozo:
            return None, None
        title = feed.feed.get("title", "").strip()
        summary = feed.feed.get("subtitle", "").strip()
        return title, summary
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None, None

def main(full: bool):
    rows = []

    with open(CSV_FILE, newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['url_type'] in ('rss', 'atom'):
                if full or not row['title'].strip():
                    new_title, new_summary = fetch_feed_metadata(row['url'])

                    if new_title or new_summary:
                        print(f"\nFeed: {row['url']}")
                        print(f"Current title:    {row['title']}")
                        print(f"New fetched title: {new_title}")
                        print(f"Current summary:    {row['description']}")
                        print(f"New fetched summary: {new_summary}")

                        title_choice = "y"
                        summary_choice = "n"
                        if row['title'] or row['description']:
                            title_choice = input("Use new title? (y/N): ").strip().lower()
                            summary_choice = input("Use new summary? (y/N): ").strip().lower()

                        if title_choice == "y" and new_title or not row['title']:
                            row['title'] = new_title
                        if summary_choice == "y" and new_summary or not row['description']:
                            row['description'] = new_summary

            rows.append(row)

    # Write back to CSV
    with open(CSV_FILE, 'w', newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update RSS/Atom titles and descriptions in CSV.")
    parser.add_argument("--full", action="store_true", help="Check all feeds instead of just ones missing a title.")
    args = parser.parse_args()
    main(args.full)
