import csv
import json

with open("ohio.csv", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

with open("ohio.json", "w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, indent=2)
