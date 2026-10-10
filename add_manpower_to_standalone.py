# -*- coding: utf-8 -*-
"""
Add Manpower Attendance tab to generate_standalone_package.py
"""

def patch_standalone_manpower():
    with open('generate_standalone_package.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add nav tab
    old_nav = """            <button onclick="switchTab('materials')" id="tab-btn-materials" class="nav-tab px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:text-slate-900 transition flex items-center gap-1.5">
                <i class="fa-solid fa-list-check text-purple-600"></i> <span>Material Catalog</span>
            </button>"""

    new_nav = """            <button onclick="switchTab('materials')" id="tab-btn-materials" class="nav-tab px-4 py-2 rounded-xl text-xs font-bold text-slate-600 hover:text-slate-900 transition flex items-center gap-1.5">
                <i class="fa-solid fa-list-check text-purple-600"></i> <span>Material Catalog</span>
            </button>
            <button onclick="switchTab('manpower')" id="tab-btn-manpower" class="nav-tab px-4 py-2 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-700 hover:bg-indigo-100 transition flex items-center gap-1.5">
                <i class="fa-solid fa-users-gear text-indigo-600"></i> <span>हाजिरी (Manpower)</span>
            </button>"""

    if old_nav in content and 'tab-btn-manpower' not in content:
        content = content.replace(old_nav, new_nav, 1)

    # 2. Add Section right before section-materials or section-entry
    target_section = '<section id="section-materials"'
    manpower_section = """
        <!-- ========================================== -->
        <!-- TAB 8: DAILY MANPOWER ATTENDANCE           -->
        <!-- ========================================== -->
        <section id="section-manpower" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="px-2.5 py-1 rounded-lg bg-indigo-100 text-indigo-700 font-mono text-xs font-bold uppercase">Manpower Register</span>
                        <span class="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-semibold">21 Sites Sheet</span>
                    </div>
                    <h2 class="text-xl font-black text-slate-800 mt-1 flex items-center gap-2">
                        <i class="fa-solid fa-users-gear text-indigo-600"></i> Daily Manpower Attendance (दैनिक साइट हाजिरी)
                    </h2>
                    <p class="text-xs text-slate-500 mt-0.5">हर साइट पर रोज कितने मिस्त्री, प्लंबर, हेल्पर और स्टाफ आए</p>
                </div>

                <div class="flex flex-wrap items-center gap-2.5">
                    <div class="flex items-center gap-2 bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 shadow-sm">
                        <i class="fa-solid fa-calendar-days text-slate-400 text-xs"></i>
                        <label class="text-xs font-bold text-slate-700">तारीख:</label>
                        <input type="date" id="standaloneAttDate" onchange="loadStandaloneManpower(this.value)" class="bg-transparent text-xs font-bold text-slate-900 border-none focus:outline-none">
                    </div>
                    <button type="button" onclick="saveStandaloneManpower()" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-black shadow-md transition flex items-center gap-1.5">
                        <i class="fa-solid fa-floppy-disk"></i> <span>हाजिरी सेव करें</span>
                    </button>
                    <button type="button" onclick="downloadManpowerCSV()" class="px-3.5 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-300 text-xs font-bold transition flex items-center gap-1.5 shadow-sm">
                        <i class="fa-solid fa-file-excel text-emerald-600 text-sm"></i> <span>Excel डाउनलोड</span>
                    </button>
                </div>
            </div>

            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
                <div class="py-3 px-6 bg-slate-50 border-b border-slate-200 text-center">
                    <h3 id="standaloneAttRedTitle" class="text-xl sm:text-2xl font-black text-rose-600 tracking-wider">
                        DATE
                    </h3>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs border-collapse" id="standaloneManpowerTable">
                        <thead class="bg-slate-100 text-slate-800 font-black border-b border-slate-300 uppercase text-[11px] tracking-wider text-center">
                            <tr>
                                <th class="py-3 px-2 w-10 border-r border-slate-200">SL.NO</th>
                                <th class="py-3 px-3 text-left w-36 border-r border-slate-200">SITE NAME</th>
                                <th class="py-3 px-2 w-20 border-r border-slate-200">SITE INCHARGE</th>
                                <th class="py-3 px-2 w-20 border-r border-slate-200">SUPERVISOR</th>
                                <th class="py-3 px-2 w-20 border-r border-slate-200">ELECTRICIAN</th>
                                <th class="py-3 px-2 w-20 border-r border-slate-200">GI MISTRI</th>
                                <th class="py-3 px-2 w-16 border-r border-slate-200">D E O</th>
                                <th class="py-3 px-2 w-20 border-r border-slate-200">PLUMBER</th>
                                <th class="py-3 px-2 w-20 border-r border-slate-200">HELPER</th>
                                <th class="py-3 px-2 w-16 border-r border-slate-200">OTHER</th>
                                <th class="py-3 px-2 w-20 bg-slate-200 font-extrabold border-r border-slate-300">TOTAL</th>
                                <th class="py-3 px-3 text-left w-64">REMARKS</th>
                            </tr>
                        </thead>
                        <tbody id="standaloneManpowerTbody" class="divide-y divide-slate-200 text-slate-800">
                            <!-- Injected via JS -->
                        </tbody>
                        <tfoot id="standaloneManpowerTfoot" class="bg-slate-100 border-t-2 border-slate-300 font-black text-slate-900 text-center">
                            <!-- Injected via JS -->
                        </tfoot>
                    </table>
                </div>
            </div>
        </section>
"""

    if target_section in content and 'section-manpower' not in content:
        content = content.replace(target_section, manpower_section + '\n        ' + target_section, 1)

    # 3. Add JS functions for manpower in standalone
    js_manpower = """
        // --- STANDALONE DAILY MANPOWER ATTENDANCE LOGIC ---
        const MANPOWER_SITES = [
            "Madhubani", "Singhiya", "Sonpur", "Sheohar", "Jhanjharpur",
            "Ekma", "Siwan", "Chhapra", "Andar", "Mairwa",
            "Basantpur", "Hasanpura", "Kati", "Darbhanga", "Maharajganj",
            "Guthani", "Barhariya", "Sahebganj", "Mirganj", "Naubathpur", "Parsa"
        ];

        // Seeded sample matching photo for 2026-10-08
        const PHOTO_SAMPLE_MANPOWER = {
            "madhubani": { si: 1, sup: 1, elec: 1, gi: 0, deo: 1, plumb: 2, help: 3, oth: 0, rem: "RAINING" },
            "singhiya": { si: 1, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 2, help: 2, oth: 0, rem: "" },
            "sonpur": { si: 1, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 1, help: 3, oth: 0, rem: "" },
            "sheohar": { si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "NOT REACHABLE" },
            "jhanjharpur": { si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 1, oth: 0, rem: "RAINING" },
            "ekma": { si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" },
            "siwan": { si: 1, sup: 1, elec: 0, gi: 3, deo: 0, plumb: 0, help: 3, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" },
            "chhapra": { si: 1, sup: 2, elec: 0, gi: 4, deo: 0, plumb: 0, help: 0, oth: 0, rem: "" },
            "andar": { si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "SITE CLOSED DUE TO MANPOWER" },
            "mairwa": { si: 0, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 2, help: 1, oth: 0, rem: "" },
            "basantpur": { si: 0, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 1, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" },
            "hasanpura": { si: 0, sup: 1, elec: 0, gi: 3, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" },
            "kati": { si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "" },
            "darbhanga": { si: 1, sup: 1, elec: 0, gi: 0, deo: 1, plumb: 4, help: 4, oth: 0, rem: "" },
            "maharajganj": { si: 1, sup: 1, elec: 0, gi: 3, deo: 0, plumb: 0, help: 2, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" },
            "guthani": { si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" },
            "barhariya": { si: 0, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 2, help: 2, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" },
            "sahebganj": { si: 0, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" },
            "mirganj": { si: 1, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 4, help: 2, oth: 0, rem: "" },
            "naubathpur": { si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" },
            "parsa": { si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "" }
        };

        function initStandaloneManpower() {{
            const dateInp = document.getElementById('standaloneAttDate');
            if (dateInp && !dateInp.value) {{
                dateInp.value = "2026-10-08"; // Seeded photo date default
            }}
            loadStandaloneManpower(dateInp ? dateInp.value : "2026-10-08");
        }}

        function loadStandaloneManpower(dateStr) {{
            const redTitle = document.getElementById('standaloneAttRedTitle');
            if (redTitle) {{
                const parts = (dateStr || '').split('-');
                const fmt = parts.length === 3 ? `${{parts[2]}}/${{parts[1]}}/${{parts[0]}}` : dateStr;
                redTitle.textContent = `DATE ${{fmt}}`;
            }}

            const allStored = JSON.parse(localStorage.getItem('sandip_manpower_store') || '{}');
            let dayData = allStored[dateStr];
            if (!dayData && dateStr === "2026-10-08") {{
                dayData = PHOTO_SAMPLE_MANPOWER;
            }}
            if (!dayData) dayData = {{}};

            const tbody = document.getElementById('standaloneManpowerTbody');
            if (!tbody) return;

            tbody.innerHTML = MANPOWER_SITES.map((siteName, idx) => {{
                const sKey = siteName.toLowerCase();
                const d = dayData[sKey] || {{ si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "" }};
                const rowTot = (d.si||0) + (d.sup||0) + (d.elec||0) + (d.gi||0) + (d.deo||0) + (d.plumb||0) + (d.help||0) + (d.oth||0);

                const fmtVal = (v) => (v && v > 0) ? v : '';

                return `
                    <tr class="hover:bg-slate-50 transition man-site-row" data-site="${{sKey}}">
                        <td class="py-2 px-2 text-center text-slate-400 font-mono font-bold border-r border-slate-100">${{idx + 1}}</td>
                        <td class="py-2 px-3 font-bold text-slate-900 border-r border-slate-100 uppercase whitespace-nowrap">${{siteName}}</td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.si)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="si" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.sup)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="sup" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.elec)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="elec" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.gi)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="gi" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.deo)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="deo" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.plumb)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="plumb" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.help)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="help" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="p-1 border-r border-slate-100"><input type="number" min="0" value="${{fmtVal(d.oth)}}" class="man-inp w-full text-center py-1.5 rounded-lg border border-transparent hover:border-slate-300 font-bold text-xs bg-slate-50/50" data-role="oth" oninput="recalcStandaloneManRow(this)"></td>
                        <td class="py-2 px-2 text-center font-black text-slate-900 bg-slate-100/70 border-r border-slate-200 man-row-tot">${{rowTot > 0 ? rowTot : ''}}</td>
                        <td class="p-1"><input type="text" value="${{d.rem || ''}}" placeholder="REMARKS" class="man-rem w-full py-1.5 px-2.5 rounded-lg border border-transparent hover:border-slate-300 text-xs font-semibold uppercase text-slate-800 bg-slate-50/50"></td>
                    </tr>
                `;
            }}).join('');

            recalcStandaloneManFooter();
        }}

        function recalcStandaloneManRow(inp) {{
            const row = inp.closest('tr');
            if (!row) return;
            let sum = 0;
            row.querySelectorAll('.man-inp').forEach(i => {{
                sum += (parseInt(i.value) || 0);
            }});
            const totCell = row.querySelector('.man-row-tot');
            if (totCell) totCell.textContent = sum > 0 ? sum : '';
            recalcStandaloneManFooter();
        }}

        function recalcStandaloneManFooter() {{
            const roles = ["si", "sup", "elec", "gi", "deo", "plumb", "help", "oth"];
            const tots = {{}};
            roles.forEach(r => tots[r] = 0);
            let grand = 0;

            document.querySelectorAll('.man-site-row').forEach(row => {{
                roles.forEach(r => {{
                    const inp = row.querySelector(`[data-role="${{r}}"]`);
                    if (inp) {{
                        const val = parseInt(inp.value) || 0;
                        tots[r] += val;
                        grand += val;
                    }}
                }});
            }});

            const tfoot = document.getElementById('standaloneManpowerTfoot');
            if (!tfoot) return;

            const fmtVal = (v) => (v && v > 0) ? v : '';

            tfoot.innerHTML = `
                <tr>
                    <td class="py-3 px-2 border-r border-slate-200"></td>
                    <td class="py-3 px-3 text-center border-r border-slate-200">TOTAL</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.si)}}</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.sup)}}</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.elec)}}</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.gi)}}</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.deo)}}</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.plumb)}}</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.help)}}</td>
                    <td class="py-3 px-1 border-r border-slate-200">${{fmtVal(tots.oth)}}</td>
                    <td class="py-3 px-2 bg-slate-200 text-indigo-700 text-sm border-r border-slate-300 font-extrabold">${{fmtVal(grand)}}</td>
                    <td class="py-3 px-3 text-left text-slate-400 text-[11px]">Auto-Calculated Totals</td>
                </tr>
            `;
        }}

        function saveStandaloneManpower() {{
            const dateInp = document.getElementById('standaloneAttDate');
            const dateStr = dateInp ? dateInp.value : '';
            if (!dateStr) {{ alert("Kripya date chunein!"); return; }}

            const allStored = JSON.parse(localStorage.getItem('sandip_manpower_store') || '{{}}');
            const dayData = {{}};

            document.querySelectorAll('.man-site-row').forEach(row => {{
                const sKey = row.getAttribute('data-site');
                const getV = (r) => parseInt(row.querySelector(`[data-role="${{r}}"]`)?.value) || 0;
                const rem = row.querySelector('.man-rem')?.value.trim() || '';

                dayData[sKey] = {{
                    si: getV('si'),
                    sup: getV('sup'),
                    elec: getV('elec'),
                    gi: getV('gi'),
                    deo: getV('deo'),
                    plumb: getV('plumb'),
                    help: getV('help'),
                    oth: getV('oth'),
                    rem: rem
                }};
            }});

            allStored[dateStr] = dayData;
            localStorage.setItem('sandip_manpower_store', JSON.stringify(allStored));
            alert(`✅ ${{dateStr}} ki Daily Manpower safalta-purvak save ho gayi!`);
        }}

        function downloadManpowerCSV() {{
            const dateInp = document.getElementById('standaloneAttDate');
            const dateStr = dateInp ? dateInp.value : '2026-10-08';
            let csv = `DATE,${{dateStr}}\\n`;
            csv += `SL.NO,SITE NAME,SITE INCHARGE,SUPERVISOR,ELECTRICIAN,GI MISTRI,D E O,PLUMBER,HELPER,OTHER,TOTAL,REMARKS\\n`;

            document.querySelectorAll('.man-site-row').forEach((row, idx) => {{
                const name = row.children[1].textContent.trim();
                const si = row.querySelector('[data-role="si"]')?.value || '';
                const sup = row.querySelector('[data-role="sup"]')?.value || '';
                const elec = row.querySelector('[data-role="elec"]')?.value || '';
                const gi = row.querySelector('[data-role="gi"]')?.value || '';
                const deo = row.querySelector('[data-role="deo"]')?.value || '';
                const plumb = row.querySelector('[data-role="plumb"]')?.value || '';
                const help = row.querySelector('[data-role="help"]')?.value || '';
                const oth = row.querySelector('[data-role="oth"]')?.value || '';
                const tot = row.querySelector('.man-row-tot')?.textContent || '';
                const rem = (row.querySelector('.man-rem')?.value || '').replace(/,/g, ' ');

                csv += `${{idx+1}},${{name}},${{si}},${{sup}},${{elec}},${{gi}},${{deo}},${{plumb}},${{help}},${{oth}},${{tot}},${{rem}}\\n`;
            }});

            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `MANPOWER_${{dateStr}}.csv`;
            link.click();
        }}
"""

    # Hook initStandaloneManpower in switchTab('manpower') and DOMContentLoaded
    old_switch = "if (tabId === 'entry') renderRecentEntriesList();"
    new_switch = "if (tabId === 'entry') renderRecentEntriesList();\n            if (tabId === 'manpower') initStandaloneManpower();"

    old_dom = "initNewEntryTab();"
    new_dom = "initNewEntryTab();\n            initStandaloneManpower();"

    if old_switch in content:
        content = content.replace(old_switch, new_switch, 1)
    if old_dom in content:
        content = content.replace(old_dom, new_dom, 1)

    # Insert JS right before </script>
    target_js_end = '// --- CROSS-SITE AUDIT & SUPERVISOR DETECTION ---'
    if target_js_end in content:
        content = content.replace(target_js_end, js_manpower + '\n        ' + target_js_end, 1)

    with open('generate_standalone_package.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("generate_standalone_package.py patched with Manpower tab and logic!")

if __name__ == '__main__':
    patch_standalone_manpower()
