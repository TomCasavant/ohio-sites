import csv

input_file = "ohio.csv"
temp_file = "ohio.temp.csv"

with open(input_file, newline='', encoding='utf-8-sig') as infile, \
     open(temp_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        tags = row.get("category", "")
        if tags:
            sorted_tags = sorted(t.strip() for t in tags.split(",") if t.strip())
            row["category"] = ",".join(sorted_tags)
        writer.writerow(row)

# Overwrite the original file with the updated content
import os
os.replace(temp_file, input_file)

print(f"Tags in '{input_file}' have been sorted alphabetically.")
