import re

with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

stack = []
in_script = False
in_style = False

for idx, line in enumerate(lines):
    line_num = idx + 1
    
    # Strip comments to avoid matching commented-out tags
    line_no_comments = re.sub(r'<!--[\s\S]*?-->', '', line)
    
    # Check for script and style tags
    if '<script' in line_no_comments:
        in_script = True
    if '</script>' in line_no_comments:
        in_script = False
        continue
    if '<style' in line_no_comments:
        in_style = True
    if '</style>' in line_no_comments:
        in_style = False
        continue
        
    if in_script or in_style:
        continue
        
    # Find all HTML tags in line
    line_tags = re.findall(r'<(/?[a-zA-Z0-9]+)(?:\s+[^>]*?)?>', line_no_comments)
    for tag in line_tags:
        tname = tag.lower().strip()
        # Skip self-closing tags
        if tname in ['img', 'br', 'hr', 'input', 'meta', 'link', '!doctype']:
            continue
        if tname.startswith('/'):
            tname = tname[1:]
            if not stack:
                print(f"Error: Closed tag </{tname}> at line {line_num} with empty stack")
            else:
                last_open = stack.pop()
                if last_open != tname:
                    print(f"Error: Mismatched tags, closed </{tname}> but last opened was <{last_open}> at line {line_num}")
        else:
            stack.append(tname)

if stack:
    print(f"Error: Unclosed tags left in stack: {stack}")
else:
    print("Success: Tags are perfectly balanced and matching!")
