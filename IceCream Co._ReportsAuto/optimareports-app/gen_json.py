import json
import pandas as pd
from parser import OptimaReportsParser

df = pd.read_excel('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/betafranchise.xlsx')
parser = OptimaReportsParser()
metrics = parser.parse(df)

with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/debug_betafranchise_real.json', 'w', encoding='utf-8') as f:
    json.dump(metrics, f)
print('JSON dumped')
