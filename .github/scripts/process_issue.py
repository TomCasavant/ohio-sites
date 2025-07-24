import sys
import csv
import os
import sys
import pathlib

# Janky solution, I don't even know if I have to run process issue from within .github/scripts so I may move it back to the root directory
repo_root = pathlib.Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(repo_root))

from tools.duplicates import find_duplicate_urls
from tools.rss_cleanup import fetch_feed_metadata
from tools.url_cleanup import fetch_page_metadata

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

def url_exists(url):
    result = find_duplicate_urls(url)
    return result.get("present", False)

def add_row(data):
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({field: data.get(field, '') for field in FIELDS})

def main():
    parsed = parse_issue(ISSUE_BODY)
    url = parsed.get('url')
    url_type = parsed.get('url_type', '').lower()

    if not url:
        print("No URL provided in issue.")
        return

    if url_exists(url):
        print("URL already exists.")
        return

    title = ''
    description = ''

    # Only fetch metadata for url/rss/atom types
    if url_type == 'url':
        metadata = fetch_page_metadata(url)
        if metadata.get('success'):
            title = metadata.get('title', '')
            description = metadata.get('description', '')
    elif url_type in ('rss', 'atom'):
        title, description = fetch_feed_metadata(url)
        title = title or ''
        description = description or ''
    else:
        # For atproto or activitypub or any other types, do not fetch metadata
        pass

    data = {
        'title': title,
        'link': parsed.get('link', title or url),
        'description': description,
        'url': url,
        'url_type': url_type,
        'category': parsed.get('category', ''),
        'location': parsed.get('location', ''),
        'alt_location': parsed.get('alternate_location', ''),
    }

    add_row(data)

    # Run post-processing scripts
    os.system("python tools/alphabetical_csv.py")
    os.system("python tools/alphabetical_tags.py")
    os.system("python tools/csv_to_json.py")
    os.system("python tools/opml.py")

if __name__ == "__main__":
    main()
