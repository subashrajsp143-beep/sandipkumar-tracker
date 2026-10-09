# -*- coding: utf-8 -*-
"""
Script to patch templates/site_report.html with Cross-Site audit tagging and filter
"""
def patch_template():
    with open('templates/site_report.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Section 2 header to include Cross-Site filter button
    old_sec2_hdr = """    <!-- Section 2: Detailed Daily Usage Logs History -->
    <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
        <div class="flex items-center justify-between">
            <div>
                <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
                    <i class="fa-solid fa-clock-rotate-left text-emerald-600"></i>
                    Daily Usage Logs (Roj ka Item By Item Record)
                </h2>
                <p class="text-xs text-slate-500">Har tareekh ko koun sa material kitna use hua</p>
            </div>
            <span class="text-xs font-mono text-slate-400">{{ entries|length }} records found</span>
        </div>"""

    new_sec2_hdr = """    <!-- Section 2: Detailed Daily Usage Logs History -->
    <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
                <h2 class="text-base font-bold text-slate-800 flex items-center gap-2">
                    <i class="fa-solid fa-clock-rotate-left text-emerald-600"></i>
                    Daily Usage Logs (Roj ka Item By Item Record)
                </h2>
                <p class="text-xs text-slate-500">Har tareekh ko koun sa material kitna use hua aur kisne darj kiya</p>
            </div>
            <div class="flex items-center gap-2.5">
                <button type="button" id="btnToggleCrossSiteWeb" onclick="toggleWebCrossSiteFilter()" class="px-3.5 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold text-xs transition flex items-center gap-1.5 shadow-sm">
                    <i class="fa-solid fa-triangle-exclamation text-amber-600"></i> <span>🚨 Keval Cross-Site Entries Dekhein</span>
                </button>
                <span class="text-xs font-mono text-slate-400">{{ entries|length }} records</span>
            </div>
        </div>"""

    # 2. Update Table Header
    old_th = '<th class="py-3 px-3">Supervisor</th>'
    new_th = '<th class="py-3 px-3">Supervisor / Darj Karta (Audit Tag)</th>'

    # 3. Update Table Row and Supervisor Cell
    old_tr = """                    {% for entry in entries %}
                    <tr class="hover:bg-slate-50/80 transition" id="entry-row-{{ entry.id }}">
                        <td class="py-2.5 px-3 text-center text-slate-400 font-mono">{{ loop.index }}</td>
                        <td class="py-2.5 px-3 font-mono font-medium text-slate-700 whitespace-nowrap">{{ entry.usage_date }}</td>
                        <td class="py-2.5 px-3 font-semibold text-slate-800">{{ entry.material_name }}</td>
                        <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-900">{{ entry.quantity }}</td>
                        <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-slate-100 font-mono text-[10px]">{{ entry.material_unit }}</span></td>
                        <td class="py-2.5 px-3 text-right font-mono text-slate-500">₹{{ entry.rate }}</td>
                        <td class="py-2.5 px-3 text-right font-mono font-bold text-emerald-700">₹{{ "{:,.2f}".format(entry.total_amount) }}</td>
                        <td class="py-2.5 px-3 text-slate-600">
                            {{ entry.purpose or '-' }}
                            {% if entry.remarks %}<div class="text-[11px] text-slate-400 italic">{{ entry.remarks }}</div>{% endif %}
                        </td>
                        <td class="py-2.5 px-3 text-slate-500">{{ entry.entered_by or '-' }}</td>"""

    new_tr = """                    {% for entry in entries %}
                    {% set official_sup = (selected_site.supervisor if selected_site else (entry.site_supervisor or ''))|trim %}
                    {% set entered_name = (entry.entered_by or '')|trim %}
                    {% set is_cross = entered_name and official_sup and entered_name|lower != official_sup|lower and not (official_sup|lower in entered_name|lower) and not (entered_name|lower in official_sup|lower) %}
                    <tr class="hover:bg-slate-50/80 transition {{ 'bg-amber-50/40' if is_cross else '' }}" id="entry-row-{{ entry.id }}" data-cross-site="{{ '1' if is_cross else '0' }}">
                        <td class="py-2.5 px-3 text-center text-slate-400 font-mono">{{ loop.index }}</td>
                        <td class="py-2.5 px-3 font-mono font-medium text-slate-700 whitespace-nowrap">{{ entry.usage_date }}</td>
                        <td class="py-2.5 px-3 font-semibold text-slate-800">{{ entry.material_name }}</td>
                        <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-900">{{ entry.quantity }}</td>
                        <td class="py-2.5 px-3 text-center"><span class="px-2 py-0.5 rounded bg-slate-100 font-mono text-[10px]">{{ entry.material_unit }}</span></td>
                        <td class="py-2.5 px-3 text-right font-mono text-slate-500">₹{{ entry.rate }}</td>
                        <td class="py-2.5 px-3 text-right font-mono font-bold text-emerald-700">₹{{ "{:,.2f}".format(entry.total_amount) }}</td>
                        <td class="py-2.5 px-3 text-slate-600">
                            {{ entry.purpose or '-' }}
                            {% if entry.remarks %}<div class="text-[11px] text-slate-400 italic">{{ entry.remarks }}</div>{% endif %}
                        </td>
                        <td class="py-2.5 px-3">
                            {% if is_cross %}
                            <div class="inline-flex flex-col text-left">
                                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-black bg-amber-100 text-amber-900 border border-amber-300 shadow-sm animate-pulse">
                                    <i class="fa-solid fa-triangle-exclamation text-amber-600"></i> 🚨 Cross-Site Entry
                                </span>
                                <span class="text-xs font-bold text-slate-900 mt-0.5 flex items-center gap-1">
                                    <i class="fa-solid fa-user-pen text-amber-600"></i> By: {{ entered_name }}
                                </span>
                                <span class="text-[10px] text-slate-500 font-semibold">Site Incharge: {{ official_sup }}</span>
                            </div>
                            {% else %}
                            <div class="inline-flex items-center gap-1.5 text-slate-700 text-xs">
                                <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
                                <span class="font-bold text-slate-800">{{ entered_name or official_sup or '-' }}</span>
                                <span class="text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-1 py-0.2 rounded font-semibold">✓ Incharge</span>
                            </div>
                            {% endif %}
                        </td>"""

    # 4. JS Script for filter
    js_web = """
<script>
let webCrossSiteFilterActive = false;
function toggleWebCrossSiteFilter() {
    webCrossSiteFilterActive = !webCrossSiteFilterActive;
    const btn = document.getElementById('btnToggleCrossSiteWeb');
    const rows = document.querySelectorAll('tr[data-cross-site]');
    if (btn) {
        if (webCrossSiteFilterActive) {
            btn.className = "px-3.5 py-1.5 rounded-xl bg-amber-500 text-white font-black text-xs transition flex items-center gap-1.5 shadow-sm";
            btn.innerHTML = `<i class="fa-solid fa-filter"></i> <span>Cross-Site Filter ON (Sabhi Dekhein)</span>`;
        } else {
            btn.className = "px-3.5 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold text-xs transition flex items-center gap-1.5 shadow-sm";
            btn.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-amber-600"></i> <span>🚨 Keval Cross-Site Entries Dekhein</span>`;
        }
    }
    rows.forEach(r => {
        if (webCrossSiteFilterActive) {
            if (r.getAttribute('data-cross-site') === '1') {
                r.style.display = '';
            } else {
                r.style.display = 'none';
            }
        } else {
            r.style.display = '';
        }
    });
}
</script>
"""

    assert old_sec2_hdr in content, "old_sec2_hdr not found"
    assert old_th in content, "old_th not found"
    assert old_tr in content, "old_tr not found"

    content = content.replace(old_sec2_hdr, new_sec2_hdr, 1)
    content = content.replace(old_th, new_th, 1)
    content = content.replace(old_tr, new_tr, 1)
    content += js_web

    with open('templates/site_report.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("templates/site_report.html successfully patched!")

if __name__ == '__main__':
    patch_template()
