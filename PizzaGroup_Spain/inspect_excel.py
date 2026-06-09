import os
from parser import read_xlsx

path = "All Metrics Data (28).xlsx"
if not os.path.exists(path):
    print(f"Error: {path} not found.")
    exit(1)

rows = read_xlsx(path)
print(f"Total rows: {len(rows)}")

# Print header row to see columns
if len(rows) > 5:
    header = rows[5]
    print(f"Row 5 Header: {header[:10]} ...")
    print(f"Stores extracted: {len(header) - 2} stores.")

for idx, r in enumerate(rows):
    if len(r) > 1:
        # Print non-empty row labels
        val_b = r[1] if len(r) > 1 else ''
        val_a = r[0] if len(r) > 0 else ''
        print(f"Row {idx}: Col A='{val_a}' | Col B='{val_b}'")
