import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import re

def sanitize_filename(name: str) -> str:
    return re.sub(r'[^a-z0-9_]', '', name.lower().replace(" ", "_"))

def generate_opml_files():
    input_file = 'ohio.csv'
    output_dir = Path('.')
    output_dir.mkdir(exist_ok=True)

    # Load all rows
    with open(input_file, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row.get('url_type', '').lower() in {'rss', 'atom'}]

    # Group rows by alt_location
    grouped = {}
    for row in rows:
        alt_loc = row.get('alt_location', 'Ohio').strip()
        grouped.setdefault(alt_loc, []).append(row)

    # Function to create OPML
    def create_opml(filename, title, feeds):
        root = ET.Element('opml', version="2.0")
        head = ET.SubElement(root, 'head')
        ET.SubElement(head, 'title').text = title
        body = ET.SubElement(root, 'body')

        for row in feeds:
            ET.SubElement(
                body,
                'outline',
                type=row['url_type'].lower(),
                text=row['title'],
                title=row['title'],
                xmlUrl=row['url'],
                htmlUrl=row['link']
            )

        tree = ET.ElementTree(root)
        ET.indent(tree, space="\t", level=0)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Generated {filename}")

    # Create one OPML per alt_location
    for alt_loc, feeds in grouped.items():
        filename = output_dir / f"{sanitize_filename(alt_loc)}.opml"
        create_opml(filename, f"{alt_loc} Feeds", feeds)

    # Create all.opml with everything
    create_opml(output_dir / "all.opml", "All Ohio Feeds", rows)

if __name__ == '__main__':
    generate_opml_files()
