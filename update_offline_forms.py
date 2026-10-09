# -*- coding: utf-8 -*-
"""
Patch templates/daily_entry.html and templates/store.html with offline form submission fallback.
"""

def patch_daily_entry():
    with open('templates/daily_entry.html', 'r', encoding='utf-8') as f:
        content = f.read()

    old_submit = """        try {
            const res = await fetch('/api/entries', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    site_id: siteId,
                    usage_date: usageDate,
                    purpose: purpose,
                    entered_by: enteredByName,
                    items: items
                })
            });

            const result = await res.json();
            if (result.success) {
                alert("Shaandaar! " + result.message);
                window.location.href = `/reports/sites?site_id=${siteId}`;
            } else {
                alert("Error: " + result.message);
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Entry Save Karein';
            }
        } catch (err) {
            alert("Request failed: " + err);
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Entry Save Karein';
        }"""

    new_submit = """        const payload = {
            site_id: siteId,
            usage_date: usageDate,
            purpose: purpose,
            entered_by: enteredByName,
            items: items,
            created_at: new Date().toISOString()
        };

        // If explicitly offline, save to offline queue immediately
        if (!navigator.onLine) {
            const queue = JSON.parse(localStorage.getItem('sandip_offline_queue') || '[]');
            queue.push(payload);
            localStorage.setItem('sandip_offline_queue', JSON.stringify(queue));
            alert("🕒 OFFLINE SAVED (नेटवर्क नहीं है):\n\nEntry आपके फोन में सुरक्षित सेव हो गई है!\nजैसे ही थोड़ा सा भी इंटरनेट मिलेगा, यह अपने आप मुख्य सर्वर पर सिंक हो जाएगी और बाकी 20-30 सुपरवाइजर्स को दिखने लगेगी।");
            window.location.href = `/reports/sites?site_id=${siteId}`;
            return;
        }

        try {
            const res = await fetch('/api/entries', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await res.json();
            if (result.success) {
                alert("Shaandaar! " + result.message);
                window.location.href = `/reports/sites?site_id=${siteId}`;
            } else {
                alert("Error: " + result.message);
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> Entry Save Karein';
            }
        } catch (err) {
            console.warn("Network fetch failed, saving to offline queue:", err);
            const queue = JSON.parse(localStorage.getItem('sandip_offline_queue') || '[]');
            queue.push(payload);
            localStorage.setItem('sandip_offline_queue', JSON.stringify(queue));
            alert("🕒 OFFLINE SAVED (नेटवर्क कमजोर है):\n\nEntry आपके फोन में सुरक्षित सेव हो गई है!\nइंटरनेट कनेक्ट होते ही यह अपने आप सर्वर पर सिंक हो जाएगी।");
            window.location.href = `/reports/sites?site_id=${siteId}`;
        }"""

    if old_submit in content:
        content = content.replace(old_submit, new_submit, 1)
        with open('templates/daily_entry.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("templates/daily_entry.html patched with offline fallback!")
    else:
        print("old_submit not found in daily_entry.html (already patched or modified).")

def patch_store():
    with open('templates/store.html', 'r', encoding='utf-8') as f:
        content = f.read()

    old_store_submit = """        try {
            const res = await fetch('/api/entries', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.success) {
                alert('✅ Materials successfully issued to site!');
                clearCart();
                closeIssueModal();
                window.location.href = `/reports/sites?site_id=${siteId}`;
            } else {
                alert('❌ Error: ' + (data.message || 'Failed to issue materials'));
                btn.disabled = false;
                btn.innerHTML = `<i class=\"fa-solid fa-check\"></i> Confirm & Issue Materials`;
            }
        } catch (err) {
            console.error('Issue error:', err);
            alert('❌ Network error. Please try again.');
            btn.disabled = false;
            btn.innerHTML = `<i class=\"fa-solid fa-check\"></i> Confirm & Issue Materials`;
        }"""

    new_store_submit = """        if (!navigator.onLine) {
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
            const res = await fetch('/api/entries', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.success) {
                alert('✅ Materials successfully issued to site!');
                clearCart();
                closeIssueModal();
                window.location.href = `/reports/sites?site_id=${siteId}`;
            } else {
                alert('❌ Error: ' + (data.message || 'Failed to issue materials'));
                btn.disabled = false;
                btn.innerHTML = `<i class=\"fa-solid fa-check\"></i> Confirm & Issue Materials`;
            }
        } catch (err) {
            console.warn('Store network error, queuing offline:', err);
            const queue = JSON.parse(localStorage.getItem('sandip_offline_queue') || '[]');
            queue.push(payload);
            localStorage.setItem('sandip_offline_queue', JSON.stringify(queue));
            alert('🕒 OFFLINE SAVED: Network kamjor hai, par issue slip aapke phone me save ho gayi hai! Net aate hi auto-sync ho jayegi.');
            clearCart();
            closeIssueModal();
            window.location.href = `/reports/sites?site_id=${siteId}`;
        }"""

    if old_store_submit in content:
        content = content.replace(old_store_submit, new_store_submit, 1)
        with open('templates/store.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("templates/store.html patched with offline fallback!")
    else:
        print("old_store_submit not found in store.html (already patched or modified).")

if __name__ == '__main__':
    patch_daily_entry()
    patch_store()
