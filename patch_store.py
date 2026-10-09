# -*- coding: utf-8 -*-
with open('templates/store.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "        try {\n            const res = await fetch('/api/entries', {"
replacement = """        if (!navigator.onLine) {
            const queue = JSON.parse(localStorage.getItem('sandip_offline_queue') || '[]');
            queue.push(payload);
            localStorage.setItem('sandip_offline_queue', JSON.stringify(queue));
            alert('🕒 OFFLINE SAVED: Network nahi hai, par materials issue slip aapke phone me surakshit save ho gayi hai! Internet aate hi yeh server par chadh jayegi.');
            clearCart();
            closeIssueModal();
            window.location.href = `/reports/sites?site_id=${siteId}`;
            return;
        }

        try {
            const res = await fetch('/api/entries', {"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open('templates/store.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("store.html patched successfully!")
else:
    print("target not found in store.html")
