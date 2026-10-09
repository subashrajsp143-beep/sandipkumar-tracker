# -*- coding: utf-8 -*-
"""
Apply Owner-level upgrades:
1. Delete protection with Owner PIN (1234)
2. WhatsApp Share button on reports for the owner
3. Live Cross-Site check in daily_entry.html
"""
import sys

def patch_app_py_pin():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    old_del = '''@app.route("/api/entries/<int:entry_id>", methods=["DELETE", "OPTIONS"])
def delete_entry(entry_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        database.delete_consumption_entry(entry_id)'''

    new_del = '''@app.route("/api/entries/<int:entry_id>", methods=["DELETE", "OPTIONS"])
def delete_entry(entry_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        # Security: Require Owner PIN (Default: 1234) to delete financial logs
        data = request.get_json(silent=True) or {}
        pin = request.args.get("pin") or data.get("pin") or request.headers.get("X-Admin-PIN")
        if not pin or str(pin).strip() != "1234":
            return jsonify({"success": False, "message": "Ghalat ya missing Malik PIN! Record delete karne ke liye valid Malik PIN (1234) anivarya hai."}), 403

        database.delete_consumption_entry(entry_id)'''

    if old_del in content:
        content = content.replace(old_del, new_del, 1)
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("app.py delete route secured with Owner PIN 1234!")
    else:
        print("old_del not found in app.py (already patched or different)")

def patch_site_report_html():
    with open('templates/site_report.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add WhatsApp Share Button in Export Buttons (Section header)
    old_btn_group = '''        <!-- Export Buttons -->
        <div class="flex items-center gap-3 no-print">
            <a href="{{ url_for('daily_entry') }}?site_id={{ selected_site.id }}" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-sm transition flex items-center gap-2">
                <i class="fa-solid fa-plus"></i> Add Usage
            </a>
            <a href="{{ url_for('export_site_excel', site_id=selected_site.id, from_date=from_date, to_date=to_date) }}" class="px-4 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-300 text-xs font-bold transition flex items-center gap-2">
                <i class="fa-solid fa-file-excel text-emerald-600 text-sm"></i> Download Excel
            </a>'''

    new_btn_group = '''        <!-- Export Buttons -->
        <div class="flex flex-wrap items-center gap-2.5 no-print">
            <a href="{{ url_for('daily_entry') }}?site_id={{ selected_site.id }}" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5">
                <i class="fa-solid fa-plus"></i> Add Usage
            </a>
            <a href="{{ url_for('export_site_excel', site_id=selected_site.id, from_date=from_date, to_date=to_date) }}" class="px-3.5 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-300 text-xs font-bold transition flex items-center gap-1.5">
                <i class="fa-solid fa-file-excel text-emerald-600 text-sm"></i> Download Excel
            </a>
            <button type="button" onclick="shareSiteReportWhatsApp()" class="px-3.5 py-2 rounded-xl bg-green-600 hover:bg-green-700 text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5">
                <i class="fa-brands fa-whatsapp text-sm"></i> WhatsApp Share
            </button>'''

    if old_btn_group in content:
        content = content.replace(old_btn_group, new_btn_group, 1)

    # 2. Update deleteEntry JS to prompt for Owner PIN
    old_delete_fn = """    function deleteEntry(id) {
        if (!confirm('Kya aap sach me yeh record hatana chahte hain?')) return;

        fetch(`/api/entries/${id}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const row = document.getElementById(`entry-row-${id}`);
                    if (row) row.remove();
                    alert('✅ Entry delete ho gayi!');
                } else {
                    alert('❌ Error: ' + data.message);
                }
            })
            .catch(err => alert('Request failed: ' + err));
    }"""

    new_delete_fn = """    function deleteEntry(id) {
        const pin = prompt('🚨 SURAKSHA CHEK (Malik Authorization):\\n\\nKeval Malik hi record delete kar sakte hain.\\nKripya Malik PIN dalein:');
        if (!pin) return;

        fetch(`/api/entries/${id}?pin=${encodeURIComponent(pin)}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const row = document.getElementById(`entry-row-${id}`);
                    if (row) row.remove();
                    alert('✅ Entry safalta-purvak delete ho gayi!');
                } else {
                    alert('❌ ' + data.message);
                }
            })
            .catch(err => alert('Request failed: ' + err));
    }

    function shareSiteReportWhatsApp() {
        const siteName = '{{ selected_site.name }}';
        const siteCode = '{{ selected_site.code }}';
        const sup = '{{ selected_site.supervisor }}';
        const grandTotal = '₹{{ "{:,.2f}".format(grand_total) }}';
        const entriesCount = '{{ entries|length }}';
        const currentUrl = window.location.href;

        const text = `📋 *M/S SANDIP KUMAR - SITE MATERIAL REPORT*\\n` +
                     `🏗️ *Site:* ${siteName} (${siteCode})\\n` +
                     `👤 *Incharge:* ${sup}\\n` +
                     `📦 *Kul Entries:* ${entriesCount}\\n` +
                     `💰 *Kul Kharcha:* ${grandTotal}\\n\\n` +
                     `🔗 *Puri Report Dekhein:*\\n${currentUrl}`;

        const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
        window.open(url, '_blank');
    }"""

    if old_delete_fn in content:
        content = content.replace(old_delete_fn, new_delete_fn, 1)

    with open('templates/site_report.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("templates/site_report.html patched with Owner PIN and WhatsApp share!")

def patch_daily_entry_supervisor_check():
    with open('templates/daily_entry.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add live Cross-Site warning in daily_entry.html
    old_entered_by_block = '''            <!-- Purpose & Entered By -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                        Karye ka Vivaran (Purpose)
                    </label>
                    <input type="text" name="purpose" id="purposeInput" placeholder="e.g. Boring work, main pipeline extension" class="w-full rounded-xl border border-slate-300 py-2.5 px-3 text-xs text-slate-800 bg-white shadow-sm focus:border-blue-600 focus:outline-none">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                        Entry Karne Wale Ka Naam
                    </label>
                    <input type="text" name="entered_by" id="enteredByInput" placeholder="Aapka naam (e.g. Ramesh)" class="w-full rounded-xl border border-slate-300 py-2.5 px-3 text-xs text-slate-800 bg-white shadow-sm focus:border-blue-600 focus:outline-none">
                </div>
            </div>'''

    new_entered_by_block = '''            <!-- Purpose & Entered By -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                        Karye ka Vivaran (Purpose)
                    </label>
                    <input type="text" name="purpose" id="purposeInput" placeholder="e.g. Boring work, main pipeline extension" class="w-full rounded-xl border border-slate-300 py-2.5 px-3 text-xs text-slate-800 bg-white shadow-sm focus:border-blue-600 focus:outline-none">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                        Entry Karne Wale Ka Naam (Worker / Munshi)
                    </label>
                    <input type="text" name="entered_by" id="enteredByInput" oninput="checkWebSupervisorCrossSite()" placeholder="Aapka naam (e.g. Ramesh)" class="w-full rounded-xl border border-slate-300 py-2.5 px-3 text-xs text-slate-800 bg-white shadow-sm focus:border-blue-600 focus:outline-none">
                </div>
            </div>
            <!-- Live Cross-Site Warning in Web Entry -->
            <div id="webCrossSiteWarning" class="hidden p-3.5 rounded-xl bg-amber-50 border-2 border-amber-400 text-amber-950 text-xs font-semibold flex items-center gap-3 animate-pulse">
                <i class="fa-solid fa-triangle-exclamation text-amber-600 text-xl flex-shrink-0"></i>
                <div>
                    <strong class="uppercase text-amber-900">⚠️ Cross-Site Chetavani:</strong>
                    Aap is chuni hui site ke incharge (<span id="webOfficialSupName" class="font-bold underline text-slate-900"></span>) nahi hain.
                    Yeh entry Malik ke paas <strong>🚨 Cross-Site Entry (Dusre Worker Dwara)</strong> ke roop me dikhegi.
                </div>
            </div>'''

    if old_entered_by_block in content:
        content = content.replace(old_entered_by_block, new_entered_by_block, 1)

    # Add checkWebSupervisorCrossSite function right before </script>
    js_cross_web = '''
    function checkWebSupervisorCrossSite() {
        const siteSelect = document.getElementById('siteSelect');
        const selectedOpt = siteSelect ? siteSelect.options[siteSelect.selectedIndex] : null;
        const officialSup = selectedOpt ? selectedOpt.getAttribute('data-supervisor') || '' : '';
        const entered = (document.getElementById('enteredByInput')?.value || '').trim();
        const alertBox = document.getElementById('webCrossSiteWarning');
        const supSpan = document.getElementById('webOfficialSupName');

        if (alertBox && supSpan) {
            if (entered && officialSup && entered.toLowerCase() !== officialSup.toLowerCase() && !officialSup.toLowerCase().includes(entered.toLowerCase()) && !entered.toLowerCase().includes(officialSup.toLowerCase())) {
                supSpan.textContent = officialSup;
                alertBox.classList.remove('hidden');
            } else {
                alertBox.classList.add('hidden');
            }
        }
    }
    '''

    if 'function checkWebSupervisorCrossSite' not in content:
        content = content.replace('// Make functions globally available as fallback', js_cross_web + '\n    // Make functions globally available as fallback', 1)

    with open('templates/daily_entry.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("templates/daily_entry.html patched with live cross-site warning!")

if __name__ == '__main__':
    patch_app_py_pin()
    patch_site_report_html()
    patch_daily_entry_supervisor_check()
