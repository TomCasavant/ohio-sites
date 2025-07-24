import csv
import json
from collections import defaultdict
from pathlib import Path
import sys

CSV_FILE = 'ohio.csv'

def find_duplicate_urls(check_url=None, csv_file=CSV_FILE):
    input_file = Path(csv_file)
    url_counts = defaultdict(list)

    if not input_file.exists():
        return {
            "error": f"CSV file not found: {csv_file}",
            "url": check_url,
            "present": False,
            "lines": []
        }

    with input_file.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):  # start=2 for header line
            url = row.get('url', '').strip()
            if url:
                url_counts[url].append(idx)

    if check_url:
        lines = url_counts.get(check_url.strip())
        return {
            "url": check_url,
            "present": bool(lines),
            "lines": lines or []
        }
    else:
        duplicates = {url: lines for url, lines in url_counts.items() if len(lines) > 1}
        return {
            "has_duplicates": bool(duplicates),
            "duplicates": duplicates
        }

def main():
    check_url = sys.argv[1] if len(sys.argv) > 1 else None
    result = find_duplicate_urls(check_url)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
