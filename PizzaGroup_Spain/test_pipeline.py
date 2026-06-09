import json
from parser import parse_franchise

try:
    xlsx_path = "All Metrics Data (28).xlsx"
    data = parse_franchise(xlsx_path, "PizzaGroup España", "Mayo 2026", "01 – 31 Mayo 2026")
    print("SUCCESS: parse_franchise completed successfully!")
    print(f"Franchise: {data['franchise']}")
    print(f"Period: {data['period']}")
    print(f"Total stores: {data['n_stores']}")
    print(f"Total alerts (all_alerts): {data['all_alerts']}")
    print(f"KBP total alerts: {data['kbp']}")
    print(f"CE alerts: {data['ce']} ({data['ce_pct']}% of KBP)")
    print(f"RC alerts: {data['rc']} ({data['rc_pct']}% of KBP)")
    print(f"CO alerts: {data['co']} ({data['co_pct']}% of KBP)")
    print(f"Kitchen total alerts: {data['kitchen_total']}")
    print(f"Has Drive Thru: {data['has_drive_thru']}")
    
    # Save a debug JSON so we can use it to test JS if we want
    with open("debug_pg_spain.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved debug_pg_spain.json successfully!")
    
except Exception as e:
    import traceback
    print("ERROR in pipeline:")
    traceback.print_exc()
