import re

with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all id="..." or id='...'
ids = set(re.findall(r'id=[\"\']([a-zA-Z0-9_\-]+)[\"\']', html))

# Find all getElementById('...') or getElementById("...")
get_ids = set(re.findall(r'getElementById\([\'\"]([a-zA-Z0-9_\-]+)[\'\"]\)', html))

missing = []
for gid in get_ids:
    if gid not in ids:
        missing.append(gid)

print('IDs accessed but missing:', missing)
