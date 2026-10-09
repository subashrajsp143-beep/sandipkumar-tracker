# -*- coding: utf-8 -*-
with open('generate_standalone_package.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        window.addEventListener('DOMContentLoaded', () => {{
            initStore();
            initNewEntryTab();
        }});"""

replacement = """        window.addEventListener('DOMContentLoaded', () => {{
            initStore();
            initNewEntryTab();
            // Auto-fetch latest live entries from local server
            try {{
                fetch('http://127.0.0.1:5000/api/live-entries')
                    .then(r => r.json())
                    .then(data => {{
                        if (data && data.success && data.entries && data.entries.length > 0) {{
                            appEntries = data.entries;
                            localStorage.setItem('sandip_entries', JSON.stringify(appEntries));
                            renderRecentEntriesList();
                            renderSiteReport();
                        }}
                    }}).catch(() => {{}});
            }} catch(e) {{}}
        }});"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('generate_standalone_package.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("generate_standalone_package.py patched with automatic server poll!")
else:
    print("target not found in generate_standalone_package.py")
