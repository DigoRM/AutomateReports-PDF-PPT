import re

def update():
    with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/parser.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Change top5_types to top10
    content = content.replace("][:5]", "][:10]")

    # In the return dict:
    content = content.replace("'kbp_top5':", "'kbp_top10':")
    content = content.replace("store_int_rank('KBP')[:5]", "store_int_rank('KBP')[:10]")

    content = content.replace("'top5_alert_types':", "'top10_alert_types':")

    # Add all_top10
    all_top10_inj = r"""
        'all_top10': [[s, v, round(v/max(sir('all_alerts'),1)*100, 1)] for s, v in all_ranked[:10]],"""
    content = content.replace("        'kbp_worst':", all_top10_inj + "\n        'kbp_worst':")

    # The rest is fine. KBP stacked by area will be handled in frontend.

    with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/parser.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update()
