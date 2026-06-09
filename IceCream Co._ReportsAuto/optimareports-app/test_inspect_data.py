import os
import json
from parser import parse_franchise

xlsx_files = [
    ('betafranchise.xlsx', 'BetaFranchise', 'Abril 2026'),
    ('GammaFranchise APRIL.xlsx', 'GammaFranchise', 'Abril 2026'),
    ('deltafranchise April.xlsx', 'DeltaFranchise', 'Abril 2026'),
    ('alphafranchise APRIL.xlsx', 'AlphaFranchise', 'Abril 2026'),
]

for filename, franchise, period in xlsx_files:
    path = f'c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/{filename}'
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
