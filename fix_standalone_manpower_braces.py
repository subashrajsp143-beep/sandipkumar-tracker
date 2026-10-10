# -*- coding: utf-8 -*-
"""
Fix f-string curly braces in the newly added manpower section of generate_standalone_package.py
"""

with open('generate_standalone_package.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_manpower = False
for i, line in enumerate(lines):
    if '// --- STANDALONE DAILY MANPOWER ATTENDANCE LOGIC ---' in line:
        in_manpower = True
    elif '// --- CROSS-SITE AUDIT & SUPERVISOR DETECTION ---' in line:
        in_manpower = False

    if in_manpower:
        # replace single { with {{ and single } with }}
        # but if already {{ or }}, leave it
        l = line
        # Replace {{ with temporary placeholder
        l = l.replace('{{', '__DBL_O__').replace('}}', '__DBL_C__')
        l = l.replace('{', '{{').replace('}', '}}')
        l = l.replace('__DBL_O__', '{{').replace('__DBL_C__', '}}')
        new_lines.append(l)
    else:
        new_lines.append(line)

with open('generate_standalone_package.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed manpower section braces in generate_standalone_package.py!")
