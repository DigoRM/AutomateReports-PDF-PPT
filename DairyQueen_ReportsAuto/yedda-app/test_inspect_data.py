import os
import json
from parser import parse_franchise

xlsx_files = [
    ('ganfer.xlsx', 'Ganfer', 'Abril 2026'),
    ('Leva APRIL.xlsx', 'Leva', 'Abril 2026'),
    ('peninsula April.xlsx', 'Peninsula', 'Abril 2026'),
    ('zamabrands APRIL.xlsx', 'Zamabrands', 'Abril 2026'),
]

for filename, franchise, period in xlsx_files:
    path = f'c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/{filename}'
    if not os.path.exists(path):
        continue
    data = parse_franchise(path, franchise, period, f'01 – 30 {period}')
    
    print(f"\n=================== FRANCHISE: {franchise} ===================")
    print(f"has_drive_thru: {data.get('has_drive_thru')}")
    print(f"dt_stores_ranking length: {len(data.get('dt_stores_ranking', []))}")
    print(f"delivery_stores_ranking length: {len(data.get('delivery_stores_ranking', []))}")
    print(f"cam_stores length: {len(data.get('cam_stores', []))}")
    print(f"kbp1_alerts length: {len(data.get('kbp1_alerts', []))}")
    print(f"kbp2_alerts length: {len(data.get('kbp2_alerts', []))}")
    print(f"kbp3_alerts length: {len(data.get('kbp3_alerts', []))}")
    print(f"store_kbp_stacks length: {len(data.get('store_kbp_stacks', []))}")
    print(f"store_area_stacks length: {len(data.get('store_area_stacks', []))}")
