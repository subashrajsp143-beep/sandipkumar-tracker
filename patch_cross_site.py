# -*- coding: utf-8 -*-
"""
Script to patch generate_standalone_package.py and templates/site_report.html
with Cross-Site Entry detection, visual badges, and filtering.
"""
import sys

def patch_standalone():
    with open('generate_standalone_package.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Tab 3 filter buttons: Add Cross-Site filter button
    old_site_filter = """                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">To Date (Optional)</label>
                        <input type="date" id="reportToDate" onchange="renderSiteReport()" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-semibold text-slate-800 bg-white">
                    </div>
                </div>"""

    new_site_filter = """                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">To Date (Optional)</label>
                        <input type="date" id="reportToDate" onchange="renderSiteReport()" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-semibold text-slate-800 bg-white">
                    </div>
                </div>
                <div class="flex items-center justify-between pt-2">
                    <button type="button" id="btnToggleCrossSite" onclick="toggleCrossSiteFilter()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 transition flex items-center gap-2 shadow-sm">
                        <i class="fa-solid fa-triangle-exclamation text-amber-600 text-sm"></i> <span>🚨 Keval Cross-Site / Dusre Supervisor Ki Entries Filter Karein</span>
                    </button>
                    <span id="crossSiteBadgeCount" class="text-xs text-slate-500 font-semibold"></span>
                </div>"""

    # 2. Tab 3 Table thead: Add Supervisor / Darj Karta (Audit Tag) column
    old_thead = """                                <th class="p-3 text-right">Amount (₹)</th>
                                <th class="p-3">Purpose / Vivaran</th>
                                <th class="p-3 text-center w-28">Action</th>"""

    new_thead = """                                <th class="p-3 text-right">Amount (₹)</th>
                                <th class="p-3">Purpose / Vivaran</th>
                                <th class="p-3">Darj Karta (Audit Tag)</th>
                                <th class="p-3 text-center w-28">Action</th>"""

    # 3. Tab 6: Add live mismatch alert box below newEntryEnteredBy
    old_entered_by = """                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Entry Karne Wale Ka Naam</label>
                            <input type="text" id="newEntryEnteredBy" placeholder="Aapka naam" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs text-slate-800 bg-white">
                        </div>
                    </div>"""

    new_entered_by = """                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Entry Karne Wale Ka Naam</label>
                            <input type="text" id="newEntryEnteredBy" oninput="checkSupervisorMismatch()" placeholder="Aapka naam (e.g. Ramesh)" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs text-slate-800 bg-white">
                        </div>
                    </div>
                    <!-- Live Cross-Site Warning Banner -->
                    <div id="supervisorMismatchAlert" class="hidden p-3 rounded-xl bg-amber-50 border-2 border-amber-400 text-amber-900 text-xs font-semibold flex items-center gap-3 animate-pulse">
                        <i class="fa-solid fa-triangle-exclamation text-amber-600 text-xl flex-shrink-0"></i>
                        <div>
                            <span class="font-black text-amber-950 uppercase tracking-wide">⚠️ Cross-Site Entry Chetavani:</span>
                            Aap is chuni hui site ke official supervisor (<span id="alertOfficialSupervisor" class="font-black underline"></span>) nahi hain.
                            Yeh entry audit log me <strong>🚨 Cross-Site Entry (Dusre Supervisor Dwara)</strong> ke roop me hamesha ke liye highlight hogi!
                        </div>
                    </div>"""

    # 4. In JS renderSiteReport: Add cross site filtering and badge column in logs table
    old_logs_tbody = """            // Render Logs Table
            const logsTbody = document.getElementById('siteReportLogsTbody');
            if (filtered.length === 0) {{
                logsTbody.innerHTML = `<tr><td colspan="9" class="py-6 text-center text-slate-400">Koi log uplabdh nahi hai.</td></tr>`;
            }} else {{
                logsTbody.innerHTML = filtered.map((e, idx) => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-3 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                        <td class="p-3 font-mono font-bold text-slate-700">${{e.usage_date}}</td>
                        <td class="p-3 font-bold text-slate-800">${{e.material_name}}</td>
                        <td class="p-3 text-right font-mono font-bold text-blue-600">${{e.quantity}}</td>
                        <td class="p-3 text-center font-mono text-slate-500">${{e.material_unit}}</td>
                        <td class="p-3 text-right font-mono text-slate-600">₹${{(e.rate || 0).toFixed(2)}}</td>
                        <td class="p-3 text-right font-mono font-bold text-emerald-600">₹${{(e.total_amount || 0).toFixed(2)}}</td>
                        <td class="p-3 text-slate-500 text-[11px]">${{e.purpose || '-'}}</td>
                        <td class="p-3 text-center">"""

    new_logs_tbody = """            // Cross-Site filtering if active
            const totalSiteEntries = filtered.length;
            const crossSiteCount = filtered.filter(e => isCrossSiteMismatch(e)).length;
            const badgeCountEl = document.getElementById('crossSiteBadgeCount');
            if (badgeCountEl) {
                badgeCountEl.innerHTML = crossSiteCount > 0 
                    ? `<span class="text-amber-700 font-bold bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">⚠️ Is site me ${crossSiteCount} Cross-Site entries mili hain</span>`
                    : `<span class="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded-lg">✓ Sabhi entries authorised incharge dwara hain</span>`;
            }

            if (isCrossSiteFilterActive) {
                filtered = filtered.filter(e => isCrossSiteMismatch(e));
            }

            // Render Logs Table
            const logsTbody = document.getElementById('siteReportLogsTbody');
            if (filtered.length === 0) {{
                logsTbody.innerHTML = `<tr><td colspan="10" class="py-6 text-center text-slate-400">Koi log uplabdh nahi hai.</td></tr>`;
            }} else {{
                logsTbody.innerHTML = filtered.map((e, idx) => `
                    <tr class="hover:bg-slate-50 transition ${isCrossSiteMismatch(e) ? 'bg-amber-50/40' : ''}">
                        <td class="p-3 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                        <td class="p-3 font-mono font-bold text-slate-700">${{e.usage_date}}</td>
                        <td class="p-3 font-bold text-slate-800">${{e.material_name}}</td>
                        <td class="p-3 text-right font-mono font-bold text-blue-600">${{e.quantity}}</td>
                        <td class="p-3 text-center font-mono text-slate-500">${{e.material_unit}}</td>
                        <td class="p-3 text-right font-mono text-slate-600">₹${{(e.rate || 0).toFixed(2)}}</td>
                        <td class="p-3 text-right font-mono font-bold text-emerald-600">₹${{(e.total_amount || 0).toFixed(2)}}</td>
                        <td class="p-3 text-slate-500 text-[11px]">${{e.purpose || '-'}}</td>
                        <td class="p-3">${{getSupervisorAuditBadge(e)}}</td>
                        <td class="p-3 text-center">"""

    # 5. JS helper functions for audit badge, cross site filter, and mismatch check
    js_helpers = """
        // --- CROSS-SITE AUDIT & SUPERVISOR DETECTION ---
        let isCrossSiteFilterActive = false;

        function isCrossSiteMismatch(e) {
            const sObj = siteMap[e.site_id];
            const officialSupervisor = (sObj && sObj.supervisor ? sObj.supervisor : (e.site_supervisor || '')).trim().toLowerCase();
            const enteredBy = (e.entered_by || '').trim().toLowerCase();
            if (!enteredBy || !officialSupervisor) return false;
            return enteredBy !== officialSupervisor && !officialSupervisor.includes(enteredBy) && !enteredBy.includes(officialSupervisor);
        }

        function getSupervisorAuditBadge(e) {
            const sObj = siteMap[e.site_id];
            const officialSupervisor = (sObj && sObj.supervisor ? sObj.supervisor : (e.site_supervisor || '')).trim();
            const enteredBy = (e.entered_by || '').trim();

            if (!enteredBy && !officialSupervisor) {
                return '<span class="text-slate-400 text-xs">-</span>';
            }

            if (isCrossSiteMismatch(e)) {
                return `
                    <div class="inline-flex flex-col text-left">
                        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-black bg-amber-100 text-amber-900 border border-amber-300 shadow-sm">
                            <i class="fa-solid fa-triangle-exclamation text-amber-600"></i> 🚨 Cross-Site Entry
                        </span>
                        <span class="text-xs font-black text-slate-900 mt-0.5 flex items-center gap-1">
                            <i class="fa-solid fa-user-pen text-amber-600"></i> By: ${enteredBy}
                        </span>
                        <span class="text-[10px] text-slate-500 font-semibold">Site Incharge: ${officialSupervisor}</span>
                    </div>
                `;
            } else {
                const name = enteredBy || officialSupervisor;
                return `
                    <div class="inline-flex items-center gap-1.5 text-slate-700 text-xs">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
                        <span class="font-bold text-slate-800">${name}</span>
                        <span class="text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-1 rounded font-semibold">✓ Incharge</span>
                    </div>
                `;
            }
        }

        function toggleCrossSiteFilter() {
            isCrossSiteFilterActive = !isCrossSiteFilterActive;
            const btn = document.getElementById('btnToggleCrossSite');
            if (btn) {
                if (isCrossSiteFilterActive) {
                    btn.className = "px-3.5 py-2 rounded-xl text-xs font-black bg-amber-500 text-white shadow-md flex items-center gap-2 transition";
                    btn.innerHTML = `<i class="fa-solid fa-filter"></i> <span>Cross-Site Filter: ON (Sabhi Entries Dekhne Ke Liye Click Karein)</span>`;
                } else {
                    btn.className = "px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 transition flex items-center gap-2 shadow-sm";
                    btn.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-amber-600 text-sm"></i> <span>🚨 Keval Cross-Site / Dusre Supervisor Ki Entries Filter Karein</span>`;
                }
            }
            renderSiteReport();
        }

        function checkSupervisorMismatch() {
            const siteSelect = document.getElementById('newEntrySite');
            const siteId = siteSelect ? siteSelect.value : null;
            const sObj = siteMap[siteId];
            const official = sObj && sObj.supervisor ? sObj.supervisor.trim() : '';
            const entered = (document.getElementById('newEntryEnteredBy')?.value || '').trim();
            const alertBox = document.getElementById('supervisorMismatchAlert');
            const alertOfficial = document.getElementById('alertOfficialSupervisor');

            if (alertBox && alertOfficial) {
                if (entered && official && entered.toLowerCase() !== official.toLowerCase() && !official.toLowerCase().includes(entered.toLowerCase()) && !entered.toLowerCase().includes(official.toLowerCase())) {
                    alertOfficial.textContent = `${official} (${sObj.name || 'Site'})`;
                    alertBox.classList.remove('hidden');
                } else {
                    alertBox.classList.add('hidden');
                }
            }
        }
"""

    # Check and apply replacements
    assert old_site_filter in content, "old_site_filter not found"
    assert old_thead in content, "old_thead not found"
    assert old_entered_by in content, "old_entered_by not found"
    assert old_logs_tbody in content, "old_logs_tbody not found"

    content = content.replace(old_site_filter, new_site_filter, 1)
    content = content.replace(old_thead, new_thead, 1)
    content = content.replace(old_entered_by, new_entered_by, 1)
    content = content.replace(old_logs_tbody, new_logs_tbody, 1)

    # Insert JS helpers right before renderSiteReport
    target_fn = "function renderSiteReport() {{"
    assert target_fn in content, "target_fn not found"
    content = content.replace(target_fn, js_helpers + "\n        " + target_fn, 1)

    # Also hook checkSupervisorMismatch into onchange of newEntrySite
    old_site_change = "document.getElementById('newEntrySupervisor').value = s ? (s.supervisor || '-') : '';"
    new_site_change = "document.getElementById('newEntrySupervisor').value = s ? (s.supervisor || '-') : '';\n            checkSupervisorMismatch();"
    if old_site_change in content:
        content = content.replace(old_site_change, new_site_change, 1)

    with open('generate_standalone_package.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("generate_standalone_package.py successfully patched!")

if __name__ == '__main__':
    patch_standalone()
