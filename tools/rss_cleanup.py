import csv
import argparse
import feedparser
import requests
from pathlib import Path

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

def update_feed_metadata(csv_file=CSV_FILE, full=False):
    csv_path = Path(csv_file)
    if not csv_path.exists():
        print(f"File not found: {csv_file}")
        return

    rows = []

    with csv_path.open(newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        for row in reader:
            if row.get('url_type') in ('rss', 'atom'):
                if full or not row.get('title', '').strip():
                    new_title, new_summary = fetch_feed_metadata(row['url'])

                    if new_title or new_summary:
                        print(f"\nFeed: {row['url']}")
                        print(f"Current title:    {row.get('title', '')}")
                        print(f"New fetched title: {new_title}")
                        print(f"Current summary:  {row.get('description', '')}")
                        print(f"New fetched summary: {new_summary}")

                        title_choice = "y"
                        summary_choice = "n"
                        if row.get('title') or row.get('description'):
                            title_choice = input("Use new title? (y/N): ").strip().lower()
                            summary_choice = input("Use new summary? (y/N): ").strip().lower()

                        if title_choice == "y" and new_title:
                            row['title'] = new_title
                        if summary_choice == "y" and new_summary:
                            row['description'] = new_summary

            rows.append(row)

    with csv_path.open('w', newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="Update RSS/Atom titles and descriptions in CSV.")
    parser.add_argument("--full", action="store_true", help="Check all feeds instead of just ones missing a title.")
    args = parser.parse_args()
    update_feed_metadata(full=args.full)

if __name__ == "__main__":
    main()
