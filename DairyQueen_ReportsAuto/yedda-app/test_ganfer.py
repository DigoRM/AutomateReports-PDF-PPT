import sys
import json
import os

try:
    import pandas as pd
    from parser import YeddaParser

    df = pd.read_excel('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/ganfer.xlsx')
    parser = YeddaParser()
    metrics = parser.parse(df)

    with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/debug_ganfer_real.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f)
    print('SUCCESS')
except Exception as e:
    print('ERROR:', str(e))
