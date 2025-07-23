import csv
import xml.etree.ElementTree as ET
from pathlib import Path

def generate_opml():
    input_file = 'ohio.csv'
    output_file = 'ohio.opml'

    root = ET.Element('opml', version="2.0")
    head = ET.SubElement(root, 'head')
    ET.SubElement(head, 'title').text = 'Ohio Feeds'

    body = ET.SubElement(root, 'body')
    with open("ohio.csv", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        print(reader.fieldnames)
        for row in reader:
            url_type = row.get('url_type', '').lower()
            if url_type in {'rss', 'atom'}:
                ET.SubElement(
                    body,
                    'outline',
                    type=url_type,
                    text=row['title'],
                    title=row['title'],
                    xmlUrl=row['url'],
                    htmlUrl=row['link']
                )

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Generated {output_file}")

if __name__ == '__main__':
    generate_opml()
