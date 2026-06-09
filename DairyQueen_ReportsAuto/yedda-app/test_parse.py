import json
from parser import parse_franchise

try:
    data = parse_franchise('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/ganfer.xlsx', 'Ganfer', 'Abril 2026', '01 – 30 Abril 2026')
    print("KEYS IN DATA:")
    print(list(data.keys()))
    with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/debug_ganfer_parsed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("SUCCESSFUL PARSING!")
except Exception as e:
    import traceback
    print("ERROR DURING PARSING:")
    traceback.print_exc()
