import csv
import argparse
import requests
from bs4 import BeautifulSoup

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
        title = soup.title.string.strip() if soup.title else ""
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"].strip() if description_tag and description_tag.get("content") else ""
        return title, description
    except Exception as e:
        print(f"Failed to fetch metadata from {url}: {e}")
        return "", ""

def update_url_metadata(full=False):
    rows = []

    with open(CSV_FILE, newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["url_type"] == "url":
                if full or not row["title"].strip():
                    title, description = fetch_page_metadata(row["url"])

                    if title or description:
                        print(f"\nPage: {row['url']}")
                        print(f"Current title:    {row['title']}")
                        print(f"Fetched title:    {title}")
                        print(f"Current summary:  {row['description']}")
                        print(f"Fetched summary:  {description}")

                        title_choice = "y" if not row['title'] else input("Use new title? (y/N): ").strip().lower()
                        summary_choice = "y" if not row['description'] else input("Use new summary? (y/N): ").strip().lower()

                        if title_choice == "y" and title:
                            row["title"] = title
                        if summary_choice == "y" and description:
                            row["description"] = description

            rows.append(row)

    with open(CSV_FILE, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update page metadata for url-type rows.")
    parser.add_argument("--full", action="store_true", help="Include rows with existing titles")
    args = parser.parse_args()
    update_url_metadata(full=args.full)
