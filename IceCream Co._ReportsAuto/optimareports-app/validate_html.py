import re

with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's remove script and style tags to only analyze HTML structure
content_clean = re.sub(r'<script[\s\S]*?</script>', '', content)
content_clean = re.sub(r'<style[\s\S]*?</style>', '', content_clean)

# Find all div opening and closing tags
divs = re.findall(r'<(div|/div)(?:\s+[^>]*?)?>', content_clean, re.IGNORECASE)

open_count = 0
close_count = 0
for d in divs:
    tag = d.lower().strip()
    if tag.startswith('/'):
        close_count += 1
    else:
        open_count += 1

print(f"Total open divs: {open_count}")
print(f"Total close divs: {close_count}")
print(f"Difference (open - close): {open_count - close_count}")
