import sys
sys.stdout.reconfigure(errors='replace')

data = open('templates/dashboard.html', encoding='utf-8').read()
keywords = ['loja', 'Lojas', 'com', 'Melhores', 'Piores', 'Desempenho']

print("=== PORTUGUESE KEYWORDS SEARCH ===")
for i, line in enumerate(data.splitlines()):
    line_clean = line.strip()
    found_kws = [kw for kw in keywords if kw.lower() in line_clean.lower()]
    if found_kws:
        print(f"Line {i+1}: KWs={found_kws}")
        print(f"   Content: {line_clean}")
