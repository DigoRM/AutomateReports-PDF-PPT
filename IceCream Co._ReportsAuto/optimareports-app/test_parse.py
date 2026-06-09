import json
from parser import parse_franchise

try:
    data = parse_franchise('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/betafranchise.xlsx', 'BetaFranchise', 'Abril 2026', '01 – 30 Abril 2026')
    print("KEYS IN DATA:")
    print(list(data.keys()))
    with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/debug_betafranchise_parsed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("SUCCESSFUL PARSING!")
except Exception as e:
    import traceback
    print("ERROR DURING PARSING:")
    traceback.print_exc()
