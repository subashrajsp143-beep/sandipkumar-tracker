# -*- coding: utf-8 -*-
with open('generate_standalone_package.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        function deleteStandaloneEntry(entryId) {{
            const entry = appEntries.find(e => e.id == entryId);
            if (!entry) return;"""

replacement = """        function deleteStandaloneEntry(entryId) {{
            const entry = appEntries.find(e => e.id == entryId);
            if (!entry) return;

            const pin = prompt("🚨 SURAKSHA CHECK (मालिक केवल):\\n\\nएंट्री केवल मालिक ही हटा सकते हैं।\\nकृपया मालिक PIN (7808) डालें:");
            if (!pin || pin.trim() !== '7808') {{
                alert("❌ गलत पिन! केवल मालिक ही एंट्री डिलीट कर सकते हैं।");
                return;
            }}"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('generate_standalone_package.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("generate_standalone_package.py patched with PIN 7808!")
else:
    print("target not found in generate_standalone_package.py")
