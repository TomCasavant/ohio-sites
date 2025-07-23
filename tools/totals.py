import csv
from collections import Counter
from pathlib import Path

def count_url_types():
    input_file = Path('ohio.csv')
    counts = Counter()

    with input_file.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url_type = (row.get('url_type') or '').strip().lower()
            if url_type == 'url':
                counts['url'] += 1
            elif url_type in {'rss', 'atom'}:
                counts['rss_or_atom'] += 1
            elif url_type in {'ical', 'ics'}:
                counts['ical'] += 1
            elif url_type == 'activitypub':
                counts['ap'] += 1
            elif url_type == 'atproto':
                counts['at'] += 1

    print("# Totals")
    print(f"{counts['url']} sites")
    print(f"{counts['rss_or_atom']} feeds (rss/atom)")
    print(f"{counts['ical']} calendars (ical/ics)")
    print(f"{counts['ap']} ActivityPub accounts")
    print(f"{counts['at']} AtProto accounts")

if __name__ == '__main__':
    count_url_types()
