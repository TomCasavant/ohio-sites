import csv
import os

input_file = "ohio.csv"
temp_file = "ohio.temp.csv"

sorted_rows = None
fieldnames = None

# Read and sort rows by the 'url' column
with open(input_file, newline='', encoding='utf-8-sig') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    sorted_rows = sorted(reader, key=lambda row: row.get("url", "").lower().replace("http://", "").replace("https://",""))

# Write sorted data to a temporary file
with open(temp_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sorted_rows)

# Replace original file with the sorted version
os.replace(temp_file, input_file)

print(f"Sorted '{input_file}' alphabetically by the 'url' column.")
