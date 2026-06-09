import sys
import re

with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/parser.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'\[:5\]', '[:10]', content)
content = content.replace('ce_top5', 'ce_top10')
content = content.replace('rc_top5', 'rc_top10')
content = content.replace('co_top5', 'co_top10')
content = content.replace('dt_pin_top5', 'dt_pin_top10')
content = content.replace('dt_outside_top5', 'dt_outside_top10')
content = content.replace('dt_cash_top5', 'dt_cash_top10')
content = content.replace('dt_mobile_top5', 'dt_mobile_top10')
content = content.replace('dt_receipt_top5', 'dt_receipt_top10')
content = content.replace('top5_alert_types', 'top10_alert_types')

with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/parser.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('ce_top5', 'ce_top10')
html = html.replace('rc_top5', 'rc_top10')
html = html.replace('co_top5', 'co_top10')
html = html.replace('dt_pin_top5', 'dt_pin_top10')
html = html.replace('dt_outside_top5', 'dt_outside_top10')
html = html.replace('dt_cash_top5', 'dt_cash_top10')
html = html.replace('dt_mobile_top5', 'dt_mobile_top10')
html = html.replace('dt_receipt_top5', 'dt_receipt_top10')
html = html.replace('top5_alert_types', 'top10_alert_types')
html = html.replace('id="top5tipos"', 'id="top10tipos"')
html = html.replace('id="top5tiendas"', 'id="top10tiendas"')
html = html.replace("getElementById('top5tipos')", "getElementById('top10tipos')")
html = html.replace("getElementById('top5tiendas')", "getElementById('top10tiendas')")
html = html.replace('kbp_top5', 'all_top10')
html = html.replace('const top5 = cs.rank<=5;', 'const top5 = cs.rank<=10;')

with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
