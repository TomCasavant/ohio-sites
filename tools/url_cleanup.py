import csv
import json
import argparse
import requests
from bs4 import BeautifulSoup
from pathlib import Path

CSV_FILE = "ohio.csv"

def fetch_page_metadata(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = (
            description_tag["content"].strip()
            if description_tag and description_tag.get("content")
            else ""
        )
        return {"url": url, "title": title, "description": description, "success": True}
    except Exception as e:
        return {"url": url, "title": "", "description": "", "success": False, "error": str(e)}

def update_csv_metadata(csv_file=CSV_FILE, full=False):
    csv_path = Path(csv_file)
    if not csv_path.exists():
        print(f"File not found: {csv_file}")
        return

    rows = []

    with csv_path.open(newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            if row.get("url_type") == "url":
                if full or not row.get("title", "").strip():
                    result = fetch_page_metadata(row["url"])
                    title, description = result["title"], result["description"]

                    if title or description:
                        print(f"\nPage: {row['url']}")
                        print(f"Current title:    {row.get('title', '')}")
                        print(f"Fetched title:    {title}")
                        print(f"Current summary:  {row.get('description', '')}")
                        print(f"Fetched summary:  {description}")

                        title_choice = "y" if not row['title'] else input("Use new title? (y/N): ").strip().lower()
                        summary_choice = "y" if not row['description'] else input("Use new summary? (y/N): ").strip().lower()

                        if title_choice == "y" and title:
                            row["title"] = title
                        if summary_choice == "y" and description:
                            row["description"] = description

            rows.append(row)

    with csv_path.open("w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="Update metadata for pages in a CSV or return metadata for a given URL.")
    parser.add_argument("--full", action="store_true", help="Include rows with existing titles/descriptions when updating the CSV.")
    parser.add_argument("--url", help="Fetch metadata for a single URL and return as JSON.")
    args = parser.parse_args()

    if args.url:
        metadata = fetch_page_metadata(args.url)
        print(json.dumps(metadata, indent=2))
    else:
        update_csv_metadata(full=args.full)

if __name__ == "__main__":
    main()
