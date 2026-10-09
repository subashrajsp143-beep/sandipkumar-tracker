# -*- coding: utf-8 -*-
"""
Script to fix f-string syntax in generate_standalone_package.py
Ensuring all JS curly braces are doubled {{ }}
"""

def fix_fstring_in_standalone():
    with open('generate_standalone_package.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # The block that has single braces:
    bad_block = """        // --- CROSS-SITE AUDIT & SUPERVISOR DETECTION ---
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
        }"""

    # Properly doubled braces for python f-string:
    good_block = """        // --- CROSS-SITE AUDIT & SUPERVISOR DETECTION ---
        let isCrossSiteFilterActive = false;

        function isCrossSiteMismatch(e) {{
            const sObj = siteMap[e.site_id];
            const officialSupervisor = (sObj && sObj.supervisor ? sObj.supervisor : (e.site_supervisor || '')).trim().toLowerCase();
            const enteredBy = (e.entered_by || '').trim().toLowerCase();
            if (!enteredBy || !officialSupervisor) return false;
            return enteredBy !== officialSupervisor && !officialSupervisor.includes(enteredBy) && !enteredBy.includes(officialSupervisor);
        }}

        function getSupervisorAuditBadge(e) {{
            const sObj = siteMap[e.site_id];
            const officialSupervisor = (sObj && sObj.supervisor ? sObj.supervisor : (e.site_supervisor || '')).trim();
            const enteredBy = (e.entered_by || '').trim();

            if (!enteredBy && !officialSupervisor) {{
                return '<span class=\"text-slate-400 text-xs\">-</span>';
            }}

            if (isCrossSiteMismatch(e)) {{
                return `
                    <div class=\"inline-flex flex-col text-left\">
                        <span class=\"inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-black bg-amber-100 text-amber-900 border border-amber-300 shadow-sm\">
                            <i class=\"fa-solid fa-triangle-exclamation text-amber-600\"></i> 🚨 Cross-Site Entry
                        </span>
                        <span class=\"text-xs font-black text-slate-900 mt-0.5 flex items-center gap-1\">
                            <i class=\"fa-solid fa-user-pen text-amber-600\"></i> By: ${{enteredBy}}
                        </span>
                        <span class=\"text-[10px] text-slate-500 font-semibold\">Site Incharge: ${{officialSupervisor}}</span>
                    </div>
                `;
            }} else {{
                const name = enteredBy || officialSupervisor;
                return `
                    <div class=\"inline-flex items-center gap-1.5 text-slate-700 text-xs\">
                        <span class=\"w-2 h-2 rounded-full bg-emerald-500 inline-block\"></span>
                        <span class=\"font-bold text-slate-800\">${{name}}</span>
                        <span class=\"text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-1 rounded font-semibold\">✓ Incharge</span>
                    </div>
                `;
            }}
        }}

        function toggleCrossSiteFilter() {{
            isCrossSiteFilterActive = !isCrossSiteFilterActive;
            const btn = document.getElementById('btnToggleCrossSite');
            if (btn) {{
                if (isCrossSiteFilterActive) {{
                    btn.className = \"px-3.5 py-2 rounded-xl text-xs font-black bg-amber-500 text-white shadow-md flex items-center gap-2 transition\";
                    btn.innerHTML = `<i class=\"fa-solid fa-filter\"></i> <span>Cross-Site Filter: ON (Sabhi Entries Dekhne Ke Liye Click Karein)</span>`;
                }} else {{
                    btn.className = \"px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 transition flex items-center gap-2 shadow-sm\";
                    btn.innerHTML = `<i class=\"fa-solid fa-triangle-exclamation text-amber-600 text-sm\"></i> <span>🚨 Keval Cross-Site / Dusre Supervisor Ki Entries Filter Karein</span>`;
                }}
            }}
            renderSiteReport();
        }}

        function checkSupervisorMismatch() {{
            const siteSelect = document.getElementById('newEntrySite');
            const siteId = siteSelect ? siteSelect.value : null;
            const sObj = siteMap[siteId];
            const official = sObj && sObj.supervisor ? sObj.supervisor.trim() : '';
            const entered = (document.getElementById('newEntryEnteredBy')?.value || '').trim();
            const alertBox = document.getElementById('supervisorMismatchAlert');
            const alertOfficial = document.getElementById('alertOfficialSupervisor');

            if (alertBox && alertOfficial) {{
                if (entered && official && entered.toLowerCase() !== official.toLowerCase() && !official.toLowerCase().includes(entered.toLowerCase()) && !entered.toLowerCase().includes(official.toLowerCase())) {{
                    alertOfficial.textContent = `${{official}} (${{sObj ? sObj.name : 'Site'}})`;
                    alertBox.classList.remove('hidden');
                }} else {{
                    alertBox.classList.add('hidden');
                }}
            }}
        }}"""

    # Also check the other block inside renderSiteReport:
    bad_tbody_block = """            // Cross-Site filtering if active
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

    good_tbody_block = """            // Cross-Site filtering if active
            const totalSiteEntries = filtered.length;
            const crossSiteCount = filtered.filter(e => isCrossSiteMismatch(e)).length;
            const badgeCountEl = document.getElementById('crossSiteBadgeCount');
            if (badgeCountEl) {{
                badgeCountEl.innerHTML = crossSiteCount > 0 
                    ? `<span class=\"text-amber-700 font-bold bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200\">⚠️ Is site me ${{crossSiteCount}} Cross-Site entries mili hain</span>`
                    : `<span class=\"text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded-lg\">✓ Sabhi entries authorised incharge dwara hain</span>`;
            }}

            if (isCrossSiteFilterActive) {{
                filtered = filtered.filter(e => isCrossSiteMismatch(e));
            }}

            // Render Logs Table
            const logsTbody = document.getElementById('siteReportLogsTbody');
            if (filtered.length === 0) {{
                logsTbody.innerHTML = `<tr><td colspan=\"10\" class=\"py-6 text-center text-slate-400\">Koi log uplabdh nahi hai.</td></tr>`;
            }} else {{
                logsTbody.innerHTML = filtered.map((e, idx) => `
                    <tr class=\"hover:bg-slate-50 transition ${{isCrossSiteMismatch(e) ? 'bg-amber-50/40' : ''}}\">
                        <td class=\"p-3 text-center text-slate-400 font-mono\">${{idx + 1}}</td>
                        <td class=\"p-3 font-mono font-bold text-slate-700\">${{e.usage_date}}</td>
                        <td class=\"p-3 font-bold text-slate-800\">${{e.material_name}}</td>
                        <td class=\"p-3 text-right font-mono font-bold text-blue-600\">${{e.quantity}}</td>
                        <td class=\"p-3 text-center font-mono text-slate-500\">${{e.material_unit}}</td>
                        <td class=\"p-3 text-right font-mono text-slate-600\">₹${{(e.rate || 0).toFixed(2)}}</td>
                        <td class=\"p-3 text-right font-mono font-bold text-emerald-600\">₹${{(e.total_amount || 0).toFixed(2)}}</td>
                        <td class=\"p-3 text-slate-500 text-[11px]\">${{e.purpose || '-'}}</td>
                        <td class=\"p-3\">${{getSupervisorAuditBadge(e)}}</td>
                        <td class=\"p-3 text-center\">"""

    assert bad_block in content, "bad_block not found in content"
    assert bad_tbody_block in content, "bad_tbody_block not found in content"

    content = content.replace(bad_block, good_block, 1)
    content = content.replace(bad_tbody_block, good_tbody_block, 1)

    with open('generate_standalone_package.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed f-string braces successfully!")

if __name__ == '__main__':
    fix_fstring_in_standalone()
