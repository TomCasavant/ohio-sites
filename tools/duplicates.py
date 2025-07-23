import csv
from collections import defaultdict
from pathlib import Path

def find_duplicate_urls():
    input_file = Path('ohio.csv')
    url_counts = defaultdict(list)

    with input_file.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # start=2 accounts for header line
            url = row.get('url', '').strip()
            if url:
                url_counts[url].append(idx)

    duplicates = {url: lines for url, lines in url_counts.items() if len(lines) > 1}

    if not duplicates:
        print("No duplicate URLs found.")
    else:
        print("Duplicate URLs found:")
        for url, lines in duplicates.items():
            print(f"  - {url} (lines: {', '.join(map(str, lines))})")

if __name__ == '__main__':
    find_duplicate_urls()
