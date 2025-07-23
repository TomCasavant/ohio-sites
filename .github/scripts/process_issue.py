import sys
import csv
import os
import re
import requests
from bs4 import BeautifulSoup

ISSUE_BODY = sys.argv[1]

FIELDS = ['title', 'link', 'description', 'url', 'url_type', 'category', 'location', 'alt_location']
CSV_PATH = 'ohio.csv'

def parse_issue(body):
    result = {}
    current_key = None

    for line in body.splitlines():
        line = line.strip()

        if line.startswith("### "):
            current_key = line[4:].lower().replace(" ", "_")
        elif current_key and line:
            result[current_key] = line
            current_key = None  # Reset after capturing one value

    return result

def fetch_metadata(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (GitHub Automation Script)'}
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        desc = ''
        tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if tag and tag.get("content"):
            desc = tag["content"].strip()
        return title, desc
    except Exception as e:
        print(f"Warning: Couldn't fetch metadata: {e}")
        return "", ""

def url_exists(url):
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        return any(row['url'] == url for row in csv.DictReader(f))

def add_row(data):
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({field: data.get(field, '') for field in FIELDS})

def main():
    parsed = parse_issue(ISSUE_BODY)
    if 'url' not in parsed:
        print("No URL provided in issue.")
        return

    if url_exists(parsed['url']):
        print("URL already exists.")
        return

    title, desc = fetch_metadata(parsed['url'])

    data = {
        'title': title,
        'link': parsed.get('link', title),
        'description': desc,
        'url': parsed['url'],
        'url_type': parsed.get('url_type', ''),
        'category': parsed.get('category', ''),
        'location': parsed.get('location', ''),
        'alt_location': parsed.get('alt_location', ''),
    }

    add_row(data)

    os.system("python tools/alphabetical_csv.py")
    os.system("python tools/alphabetical_tags.py")
    os.system("python tools/csv_to_json.py")
    os.system("python tools/opml.py")

if __name__ == "__main__":
    main()
