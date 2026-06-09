import os
import traceback
from parser import parse_franchise

xlsx_files = [
    ('ganfer.xlsx', 'Ganfer', 'Abril 2026'),
    ('ganfer APRIL.xlsx', 'Ganfer', 'Abril 2026'),
    ('Leva APRIL.xlsx', 'Leva', 'Abril 2026'),
    ('peninsula April.xlsx', 'Peninsula', 'Abril 2026'),
    ('zamabrands APRIL.xlsx', 'Zamabrands', 'Abril 2026'),
    ('March_leva.xlsx', 'Leva', 'Marzo 2026'),
    ('March_Peninsula.xlsx', 'Peninsula', 'Marzo 2026'),
    ('March_zamabrand.xlsx', 'Zamabrands', 'Marzo 2026'),
]

for filename, franchise, period in xlsx_files:
    path = f'c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/{filename}'
    if not os.path.exists(path):
        print(f"Skipping {filename} (not found)")
        continue
    try:
        data = parse_franchise(path, franchise, period, f'01 – 30 {period}')
        print(f"SUCCESS: {filename} parsed successfully!")
    except Exception as e:
        print(f"FAILED: {filename} failed to parse!")
        traceback.print_exc()
