import os
import io
import json
import sqlite3
import shutil
import base64
import zipfile
from PIL import Image

def generate_base64_images(src_dir):
    """
    Compresses all images to crisp WebP/JPEG thumbnails (max 380x380)
    and returns a dict of { filename: data:image/jpeg;base64,... }
    """
    b64_dict = {}
    if not os.path.exists(src_dir):
        return b64_dict

    for fname in sorted(os.listdir(src_dir)):
        fpath = os.path.join(src_dir, fname)
        if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            try:
                im = Image.open(fpath)
                im = im.convert('RGB')
                im.thumbnail((380, 380), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, format='JPEG', quality=75, optimize=True)
                b64_str = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode('ascii')
                b64_dict[fname] = b64_str
                b64_dict[os.path.basename(fname)] = b64_str
            except Exception as e:
                print(f"Error converting {fname} to base64: {e}")

    return b64_dict

def build_standalone_package():
    # 1. Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "material_tracker.db")
    uploads_materials_dir = os.path.join(base_dir, "uploads", "materials")
    
    onedrive_desktop = r"C:\Users\Subhash Kumar\OneDrive\Desktop"
    standard_desktop = r"C:\Users\Subhash Kumar\Desktop"
    
    dest_desktops = []
    if os.path.exists(onedrive_desktop):
        dest_desktops.append(onedrive_desktop)
    if os.path.exists(standard_desktop):
        dest_desktops.append(standard_desktop)
    if not dest_desktops:
        dest_desktops.append(os.path.expanduser("~/Desktop"))

    print(f"Target Desktop Directories: {dest_desktops}")

    # Generate Base64 dictionary (once)
    b64_images = generate_base64_images(uploads_materials_dir)
    print(f"Generated {len(b64_images)} Base64 embedded images.")

    # 2. Extract Data from SQLite
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM sites ORDER BY id ASC")
    sites_raw = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM materials ORDER BY id ASC")
    materials_raw = [dict(r) for r in c.fetchall()]

    c.execute("""
        SELECT d.id, d.site_id, d.material_id, d.quantity, d.rate, d.total_amount, d.usage_date, d.purpose, d.entered_by, d.remarks,
               s.name as site_name, s.code as site_code, s.supervisor as site_supervisor,
               m.name as material_name, m.unit as material_unit, m.category as material_category, m.image_url as material_image
        FROM daily_consumption d
        LEFT JOIN sites s ON d.site_id = s.id
        LEFT JOIN materials m ON d.material_id = m.id
        ORDER BY d.usage_date DESC, d.id DESC
    """)
    entries_raw = [dict(r) for r in c.fetchall()]
    conn.close()

    # Link material image keys (keeps JSON compact)
    for m in materials_raw:
        img_url = m.get("image_url", "")
        fname = os.path.basename(img_url) if img_url else "fittings.jpg"
        m["image_key"] = fname

    for e in entries_raw:
        img_url = e.get("material_image", "")
        fname = os.path.basename(img_url) if img_url else "fittings.jpg"
        e["image_key"] = fname

    sites_json = json.dumps(sites_raw, ensure_ascii=False)
    materials_json = json.dumps(materials_raw, ensure_ascii=False)
    entries_json = json.dumps(entries_raw, ensure_ascii=False)
    b64_json = json.dumps(b64_images, ensure_ascii=False)

    # 3. HTML Content Generator
    html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>M/S Sandip Kumar - 19 Sites Material Management System & Material Store</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Google Fonts Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}
        @media print {{
            .no-print {{ display: none !important; }}
            .print-only {{ display: block !important; }}
            body {{ background: white !important; color: black !important; padding: 0 !important; }}
            .shadow-sm, .shadow-md, .shadow-lg, .shadow-2xl {{ shadow: none !important; box-shadow: none !important; }}
            .border {{ border-color: #cbd5e1 !important; }}
        }}
    </style>
</head>
<body class="bg-slate-100 text-slate-800 min-h-screen flex flex-col pb-24">

    <!-- Top Navigation Header -->
    <header class="bg-slate-900 text-white border-b border-slate-800 shadow-xl sticky top-0 z-50 no-print">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-amber-400 to-amber-200 text-slate-950 flex items-center justify-center font-black text-xl shadow-lg shadow-amber-500/20">
                    <i class="fa-solid fa-layer-group"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-base sm:text-lg font-black tracking-tight text-white">M/S SANDIP KUMAR</span>
                        <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold uppercase tracking-wider">
                            100% Embedded Offline App
                        </span>
                    </div>
                    <p class="text-xs text-slate-400">19 Sites Material Management, Daily Entry & Material Store</p>
                </div>
            </div>

            <!-- Header Quick Action Buttons -->
            <div class="flex flex-wrap items-center gap-2">
                <button onclick="downloadEntriesBackup()" class="px-3 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5" title="Sabhi entries aur photos ka backup download karein">
                    <i class="fa-solid fa-cloud-arrow-down"></i> Backup Download
                </button>
                <button onclick="openRestoreModal()" class="px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold shadow-sm transition flex items-center gap-1.5" title="Purana backup restore karein">
                    <i class="fa-solid fa-cloud-arrow-up"></i> Backup Restore
                </button>
                <button onclick="window.print()" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-print"></i> Print / PDF
                </button>
                <button onclick="exportAllCSV()" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 text-xs font-semibold border border-slate-700 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-file-excel"></i> Export Excel
                </button>
                <button onclick="resetToFactoryData()" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-rose-900/60 text-slate-400 hover:text-rose-300 text-xs font-semibold border border-slate-700 transition flex items-center gap-1" title="Reset factory data">
                    <i class="fa-solid fa-rotate-left"></i> Reset
                </button>
            </div>
        </div>

        <!-- Main Navigation Bar -->
        <div class="bg-slate-950/90 border-t border-slate-800/80 px-4">
            <div class="max-w-7xl mx-auto flex items-center gap-1 sm:gap-2 overflow-x-auto py-2 text-xs font-bold scrollbar-none">
                <button onclick="switchTab('store')" id="tab-btn-store" class="nav-tab px-4 py-2 rounded-xl bg-amber-400 text-slate-950 flex items-center gap-2 shadow-sm whitespace-nowrap transition">
                    <i class="fa-solid fa-cart-shopping"></i> Material Store
                </button>
                <button onclick="switchTab('sites')" id="tab-btn-sites" class="nav-tab px-4 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/70 flex items-center gap-2 whitespace-nowrap transition">
                    <i class="fa-solid fa-building-flag"></i> 19 Sites Directory
                </button>
                <button onclick="switchTab('site-report')" id="tab-btn-site-report" class="nav-tab px-4 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/70 flex items-center gap-2 whitespace-nowrap transition">
                    <i class="fa-solid fa-chart-pie"></i> Site-wise Report
                </button>
                <button onclick="switchTab('daily-report')" id="tab-btn-daily-report" class="nav-tab px-4 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/70 flex items-center gap-2 whitespace-nowrap transition">
                    <i class="fa-solid fa-calendar-day"></i> Roj Ka Hisab
                </button>
                <button onclick="switchTab('monthly-report')" id="tab-btn-monthly-report" class="nav-tab px-4 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/70 flex items-center gap-2 whitespace-nowrap transition">
                    <i class="fa-solid fa-calendar-days"></i> Mahina-war Hisab
                </button>
                <button onclick="switchTab('materials')" id="tab-btn-materials" class="nav-tab px-4 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/70 flex items-center gap-2 whitespace-nowrap transition">
                    <i class="fa-solid fa-boxes-stacked"></i> 271 Materials Catalog
                </button>
                <button onclick="switchTab('entry')" id="tab-btn-entry" class="nav-tab px-4 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/70 flex items-center gap-2 whitespace-nowrap transition">
                    <i class="fa-solid fa-pen-to-square"></i> + Naya Entry Karein
                </button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-6 w-full flex-grow">

        <!-- ========================================== -->
        <!-- TAB 1: MATERIAL STORE & CATALOG           -->
        <!-- ========================================== -->
        <section id="section-store" class="tab-content space-y-6">
            
            <!-- Store Hero Banner -->
            <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 sm:p-8 shadow-xl">
                <div class="relative z-10 max-w-2xl">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-400 text-slate-950 text-xs font-black uppercase tracking-wider mb-3 shadow">
                        <i class="fa-solid fa-boxes-stacked"></i> M/S SANDIP KUMAR
                    </div>
                    <h1 class="text-2xl sm:text-3xl font-black tracking-tight leading-tight">
                        Material Store & Catalog
                    </h1>
                    <p class="text-xs sm:text-sm text-blue-200 mt-2">
                        Sabhi 271 construction & plumbing materials original photos aur rates ke sath uplabdh hain. Samaan chunein aur direct 19 me se kisi bhi site par issue karein!
                    </p>
                </div>
                <div class="absolute -right-8 -bottom-10 opacity-15 pointer-events-none">
                    <i class="fa-solid fa-cart-flatbed text-[220px]"></i>
                </div>
            </div>

            <!-- Search & Filters -->
            <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 space-y-3">
                <div class="flex flex-col sm:flex-row gap-3 items-center justify-between">
                    <div class="relative w-full sm:w-96">
                        <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3 text-slate-400 text-xs"></i>
                        <input type="text" id="storeSearchInput" oninput="filterStore()" placeholder="Material ka naam ya category khojein..." class="w-full rounded-xl border border-slate-300 pl-9 pr-4 py-2 text-xs text-slate-800 focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600">
                    </div>
                    <div class="text-xs text-slate-500 font-medium self-end sm:self-center">
                        <span id="storeVisibleCount" class="font-black text-blue-600 font-mono">0</span> materials dikh rahe hain
                    </div>
                </div>

                <!-- Category Pills -->
                <div id="categoryPillsContainer" class="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
                    <!-- Injected via JS -->
                </div>
            </div>

            <!-- Products Grid -->
            <div id="productsGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 sm:gap-4">
                <!-- Injected via JS -->
            </div>

            <div id="noStoreResults" class="hidden text-center py-16 bg-white rounded-3xl border border-slate-200">
                <i class="fa-solid fa-magnifying-glass text-4xl text-slate-300 mb-3 block"></i>
                <h3 class="text-base font-bold text-slate-700">Koi material match nahi hua</h3>
                <p class="text-xs text-slate-400 mt-1">Alag keyword ya category select karke dekhein.</p>
            </div>

        </section>

        <!-- ========================================== -->
        <!-- TAB 2: 19 SITES DIRECTORY                  -->
        <!-- ========================================== -->
        <section id="section-sites" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold text-blue-600 uppercase tracking-wider block mb-1">
                        <i class="fa-solid fa-building-flag"></i> Project Master
                    </span>
                    <h2 class="text-2xl font-black text-slate-800">19 Sites Master Directory</h2>
                    <p class="text-xs text-slate-500 mt-1">Sabhi 19 sites ke supervisors, contact numbers, aur locations ki list</p>
                </div>
                <div class="flex items-center gap-2">
                    <span class="px-3 py-1.5 rounded-xl bg-blue-50 text-blue-700 font-bold text-xs border border-blue-100">
                        Total Sites: 19
                    </span>
                </div>
            </div>

            <div id="sitesGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <!-- Injected via JS -->
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 3: SITE-WISE REPORT                    -->
        <!-- ========================================== -->
        <section id="section-site-report" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                        <h2 class="text-xl font-black text-slate-800">Site-wise Material Consumption Report</h2>
                        <p class="text-xs text-slate-500">Kisi bhi site par koun sa material kitna use hua aur kab use hua</p>
                    </div>
                    <button onclick="window.print()" class="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition flex items-center gap-2 self-start sm:self-auto">
                        <i class="fa-solid fa-print"></i> Report Print Karein
                    </button>
                </div>

                <!-- Site Selector & Filters -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-slate-100">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Site Chunein</label>
                        <select id="reportSiteSelect" onchange="renderSiteReport()" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-bold text-slate-800 focus:border-blue-600 bg-white">
                            <!-- Injected via JS -->
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">From Date (Optional)</label>
                        <input type="date" id="reportFromDate" onchange="renderSiteReport()" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-semibold text-slate-800 bg-white">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">To Date (Optional)</label>
                        <input type="date" id="reportToDate" onchange="renderSiteReport()" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-semibold text-slate-800 bg-white">
                    </div>
                </div>
                <div class="flex items-center justify-between pt-2">
                    <button type="button" id="btnToggleCrossSite" onclick="toggleCrossSiteFilter()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 transition flex items-center gap-2 shadow-sm">
                        <i class="fa-solid fa-triangle-exclamation text-amber-600 text-sm"></i> <span>🚨 Keval Cross-Site / Dusre Supervisor Ki Entries Filter Karein</span>
                    </button>
                    <span id="crossSiteBadgeCount" class="text-xs text-slate-500 font-semibold"></span>
                </div>
            </div>

            <!-- Site Summary Cards -->
            <div id="siteReportSummaryCards" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <!-- Injected via JS -->
            </div>

            <!-- Site Materials Summary Table -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-boxes-packing text-blue-600"></i> Is Site Par Total Kitna Saman Laga (Summary)
                </h3>
                <div class="overflow-x-auto border border-slate-200 rounded-xl">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase text-[10px]">
                            <tr>
                                <th class="p-3 w-12 text-center">#</th>
                                <th class="p-3">Material Name</th>
                                <th class="p-3">Category</th>
                                <th class="p-3 text-center">Unit</th>
                                <th class="p-3 text-right">Total Quantity</th>
                                <th class="p-3 text-right">Avg Rate (₹)</th>
                                <th class="p-3 text-right">Total Cost (₹)</th>
                            </tr>
                        </thead>
                        <tbody id="siteReportSummaryTbody" class="divide-y divide-slate-100 text-slate-700">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Site Detailed Log Table -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <h3 class="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-clock-rotate-left text-indigo-600"></i> Tarikh-war Daily Entry Log (Date-wise Details)
                </h3>
                <div class="overflow-x-auto border border-slate-200 rounded-xl">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase text-[10px]">
                            <tr>
                                <th class="p-3 w-12 text-center">#</th>
                                <th class="p-3">Tareekh (Date)</th>
                                <th class="p-3">Material</th>
                                <th class="p-3 text-right">Qty</th>
                                <th class="p-3 text-center">Unit</th>
                                <th class="p-3 text-right">Rate (₹)</th>
                                <th class="p-3 text-right">Amount (₹)</th>
                                <th class="p-3">Purpose / Vivaran</th>
                                <th class="p-3">Darj Karta (Audit Tag)</th>
                                <th class="p-3 text-center w-28">Action</th>
                            </tr>
                        </thead>
                        <tbody id="siteReportLogsTbody" class="divide-y divide-slate-100 text-slate-700">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 4: DAILY DATE REPORT                   -->
        <!-- ========================================== -->
        <section id="section-daily-report" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h2 class="text-xl font-black text-slate-800">Roj Ka Hisab (Daily Date-wise Report)</h2>
                    <p class="text-xs text-slate-500">Kisi bhi khaas tareekh ko koun se site par kya samaan use hua</p>
                </div>
                <div class="flex items-center gap-2">
                    <label class="text-xs font-bold text-slate-700 whitespace-nowrap">Tareekh Chunein:</label>
                    <input type="date" id="dailyReportDateInput" onchange="renderDailyReport()" class="rounded-xl border border-slate-300 py-1.5 px-3 text-xs font-bold text-slate-800 bg-white">
                </div>
            </div>

            <!-- Daily Summary Cards -->
            <div id="dailyReportSummaryCards" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <!-- Injected via JS -->
            </div>

            <!-- Daily Entries Container -->
            <div id="dailyReportEntriesContainer" class="space-y-4">
                <!-- Injected via JS -->
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB: MAHINA-WAR (MONTHLY) REPORT           -->
        <!-- ========================================== -->
        <section id="section-monthly-report" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold text-blue-600 uppercase tracking-wider block mb-1">
                        <i class="fa-solid fa-calendar-days"></i> Monthly Consolidated Summary
                    </span>
                    <h2 class="text-xl sm:text-2xl font-black text-slate-800">Mahina-war Expense Report (Monthly Hisab)</h2>
                    <p class="text-xs text-slate-500 mt-1">Sabhi 19 sites par pure mahine me kitna kharch hua aur koun se material sabse zyada lage</p>
                </div>
                <div class="flex flex-wrap items-center gap-2">
                    <div class="flex items-center gap-1.5">
                        <label class="text-xs font-bold text-slate-700 whitespace-nowrap">Mahina:</label>
                        <input type="month" id="monthlyReportMonthInput" onchange="renderMonthlyReport()" class="rounded-xl border border-slate-300 py-1.5 px-3 text-xs font-bold text-slate-800 bg-white">
                    </div>
                    <button onclick="shareMonthlyWhatsApp()" class="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5" title="WhatsApp par mahine ka hisab share karein">
                        <i class="fa-brands fa-whatsapp text-sm"></i> WhatsApp Share
                    </button>
                    <button onclick="exportMonthlyCSV()" class="px-3.5 py-1.5 rounded-xl bg-blue-50 text-blue-700 hover:bg-blue-100 font-bold text-xs transition border border-blue-200 flex items-center gap-1.5">
                        <i class="fa-solid fa-file-excel"></i> Export CSV
                    </button>
                    <button onclick="window.print()" class="px-3.5 py-1.5 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition flex items-center gap-1.5">
                        <i class="fa-solid fa-print"></i> Print
                    </button>
                </div>
            </div>

            <!-- Monthly Summary Cards -->
            <div id="monthlyReportSummaryCards" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <!-- Injected via JS -->
            </div>

            <!-- 19 Sites Monthly Breakdown -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="text-sm sm:text-base font-bold text-slate-800 flex items-center gap-2">
                            <i class="fa-solid fa-building-flag text-blue-600"></i> 19 Sites Monthly Consumption Breakdown
                        </h3>
                        <p class="text-xs text-slate-400">Har site par kitne items lage aur kul kitna bill bana</p>
                    </div>
                    <span class="text-xs font-mono font-bold text-slate-400">19 Sites Directory</span>
                </div>
                <div class="overflow-x-auto border border-slate-200 rounded-xl">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase text-[10px]">
                            <tr>
                                <th class="p-3 w-10 text-center">#</th>
                                <th class="p-3 w-24">Site Code</th>
                                <th class="p-3">Site Name</th>
                                <th class="p-3">Supervisor & Contact</th>
                                <th class="p-3 text-right">Items Used</th>
                                <th class="p-3 text-right">Total Monthly Amount (₹)</th>
                                <th class="p-3 w-36">% of Month</th>
                                <th class="p-3 text-center w-24">Action</th>
                            </tr>
                        </thead>
                        <tbody id="monthlySitesTableBody" class="divide-y divide-slate-100 text-slate-700">
                            <!-- Injected via JS -->
                        </tbody>
                        <tfoot id="monthlySitesTableFoot" class="bg-slate-50 font-bold border-t-2 border-slate-200 text-slate-800">
                            <!-- Injected via JS -->
                        </tfoot>
                    </table>
                </div>
            </div>

            <!-- Top Materials This Month Grid -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm sm:text-base font-bold text-slate-800 flex items-center gap-2">
                        <i class="fa-solid fa-boxes-stacked text-amber-500"></i> Is Mahine Sabse Zyada Lagne Wale Materials (Top 10)
                    </h3>
                    <span class="text-xs text-slate-400">Ranked by Value</span>
                </div>
                <div id="monthlyTopMaterialsGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                    <!-- Injected via JS -->
                </div>
            </div>

            <!-- Day-by-Day Daily Trend Table -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-sm sm:text-base font-bold text-slate-800 flex items-center gap-2">
                        <i class="fa-solid fa-chart-line text-emerald-600"></i> Din-war Daily Expense Breakdown (Kis Tareekh Ko Kitna Laga)
                    </h3>
                    <span id="monthlyActiveDaysCount" class="text-xs text-slate-400 font-mono">0 Active Days</span>
                </div>
                <div class="overflow-x-auto border border-slate-200 rounded-xl">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase text-[10px]">
                            <tr>
                                <th class="p-2.5">Date (Tareekh)</th>
                                <th class="p-2.5 text-center">Active Sites</th>
                                <th class="p-2.5 text-right">Items Issued</th>
                                <th class="p-2.5 text-right">Day Total Amount (₹)</th>
                                <th class="p-2.5 text-center w-28">Action</th>
                            </tr>
                        </thead>
                        <tbody id="monthlyDailyTrendTbody" class="divide-y divide-slate-100 text-slate-700">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Detailed Monthly Transactions Log Table -->
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="text-sm sm:text-base font-bold text-slate-800 flex items-center gap-2">
                            <i class="fa-solid fa-list-check text-blue-600"></i> Is Mahine Ka Pura Transaction Log (All Monthly Entries)
                        </h3>
                        <p class="text-xs text-slate-400">Har entry ko yahan se bhi Edit ya Delete kiya ja sakta hai</p>
                    </div>
                    <span id="monthlyEntriesCountDisplay" class="text-xs font-mono font-bold text-slate-400">0 records</span>
                </div>
                <div class="overflow-x-auto border border-slate-200 rounded-xl">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200 uppercase text-[10px]">
                            <tr>
                                <th class="p-2.5 w-10 text-center">#</th>
                                <th class="p-2.5">Date</th>
                                <th class="p-2.5">Site Name</th>
                                <th class="p-2.5">Material Description</th>
                                <th class="p-2.5 text-right">Qty</th>
                                <th class="p-2.5 text-center">Unit</th>
                                <th class="p-2.5 text-right">Rate (₹)</th>
                                <th class="p-2.5 text-right">Amount (₹)</th>
                                <th class="p-2.5">Purpose / Supervisor</th>
                                <th class="p-2.5 text-center w-28">Action</th>
                            </tr>
                        </thead>
                        <tbody id="monthlyTransactionsTbody" class="divide-y divide-slate-100 text-slate-700">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 5: 271 MATERIALS CATALOG               -->
        <!-- ========================================== -->
        
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

        <section id="section-materials" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold text-blue-600 uppercase tracking-wider block mb-1">
                        <i class="fa-solid fa-list-check"></i> Master Inventory
                    </span>
                    <h2 class="text-2xl font-black text-slate-800">271 Materials Master Catalog</h2>
                    <p class="text-xs text-slate-500 mt-1">Sabhi materials standard rates, units aur category ke sath</p>
                </div>
                <div class="relative w-full sm:w-72">
                    <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400 text-xs"></i>
                    <input type="text" id="catalogSearchInput" oninput="filterCatalog()" placeholder="Material khojein..." class="w-full rounded-xl border border-slate-300 pl-8 pr-3 py-1.5 text-xs text-slate-800">
                </div>
            </div>

            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse">
                    <thead class="bg-slate-50 text-slate-600 font-bold border-y border-slate-200 uppercase text-[10px]">
                        <tr>
                            <th class="p-3 w-10 text-center">#</th>
                            <th class="p-3 w-14 text-center">Photo</th>
                            <th class="p-3">Material Description</th>
                            <th class="p-3">Category</th>
                            <th class="p-3 text-center">Unit</th>
                            <th class="p-3 text-right">Standard Rate (₹)</th>
                            <th class="p-3 text-center">Photo Badlein</th>
                        </tr>
                    </thead>
                    <tbody id="catalogTableBody" class="divide-y divide-slate-100 text-slate-700">
                        <!-- Injected via JS -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 6: NEW ENTRY (OFFLINE LOCAL STORAGE)   -->
        <!-- ========================================== -->
        <section id="section-entry" class="tab-content hidden space-y-6">
            <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-4">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center font-black">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </div>
                    <div>
                        <h2 class="text-xl font-black text-slate-800">Roj Ka Entry (Daily Consumption Entry)</h2>
                        <p class="text-xs text-slate-500">Yahan nayi entry save karein - browser memory (LocalStorage) me save ho jayega!</p>
                    </div>
                </div>

                <!-- Form -->
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-3">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Koun Se Site Par? <span class="text-rose-500">*</span></label>
                            <select id="newEntrySite" onchange="onNewEntrySiteChange()" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-bold text-slate-800 bg-white">
                                <!-- Injected via JS -->
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Tareekh (Date) <span class="text-rose-500">*</span></label>
                            <input type="date" id="newEntryDate" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-bold text-slate-800 bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Supervisor (Auto)</label>
                            <input type="text" id="newEntrySupervisor" readonly class="w-full rounded-xl border border-slate-200 py-2 px-3 text-xs text-slate-600 bg-slate-100">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Karye ka Vivaran (Purpose)</label>
                            <input type="text" id="newEntryPurpose" placeholder="e.g. Pipeline extension, boring work" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs text-slate-800 bg-white">
                        </div>
                        <div>
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
                    </div>
                </div>

                <!-- Items Selector Table -->
                <div class="space-y-2">
                    <div class="flex items-center justify-between">
                        <h4 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Materials List:</h4>
                        <button type="button" onclick="addNewEntryRow()" class="px-3 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition flex items-center gap-1.5">
                            <i class="fa-solid fa-plus"></i> + Item Jodein
                        </button>
                    </div>

                    <div class="border border-slate-200 rounded-xl overflow-hidden">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                                <tr>
                                    <th class="p-2.5 w-10 text-center">#</th>
                                    <th class="p-2.5">Material Description</th>
                                    <th class="p-2.5 w-24 text-center">Unit</th>
                                    <th class="p-2.5 w-28 text-right">Qty</th>
                                    <th class="p-2.5 w-28 text-right">Rate (₹)</th>
                                    <th class="p-2.5 w-32 text-right">Amount (₹)</th>
                                    <th class="p-2.5 w-12 text-center">Hatao</th>
                                </tr>
                            </thead>
                            <tbody id="newEntryTableBody" class="divide-y divide-slate-100">
                                <!-- Injected via JS -->
                            </tbody>
                            <tfoot class="bg-slate-50 border-t border-slate-200 font-bold text-slate-800">
                                <tr>
                                    <td colspan="5" class="p-3 text-right">Grand Total:</td>
                                    <td id="newEntryGrandTotal" class="p-3 text-right font-mono text-emerald-600 text-sm">₹0.00</td>
                                    <td></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>

                <div class="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
                    <button type="button" onclick="saveNewEntryRecord()" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition flex items-center gap-2">
                        <i class="fa-solid fa-check-double"></i> Save Karein Aur Report Me Dekhein
                    </button>
                </div>

                <!-- Recent Entries & Quick Edit/Delete Table in Tab 6 -->
                <div class="mt-8 pt-6 border-t border-slate-200 space-y-3">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                                <i class="fa-solid fa-clock-rotate-left text-blue-600"></i> Haal Hi Ki Entries (Recent Records - Edit / Delete)
                            </h3>
                            <p class="text-[11px] text-slate-400">Yahan se aap kisi bhi entry ko Edit kar sakte hain ya Delete kar sakte hain</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <button type="button" onclick="downloadEntriesBackup()" class="px-3 py-1.5 rounded-xl bg-blue-50 text-blue-700 hover:bg-blue-100 font-bold text-xs transition flex items-center gap-1.5">
                                <i class="fa-solid fa-cloud-arrow-down"></i> Backup Le Lo
                            </button>
                        </div>
                    </div>
                    <div class="border border-slate-200 rounded-2xl overflow-hidden">
                        <table class="w-full text-left text-xs border-collapse">
                            <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                                <tr>
                                    <th class="p-2.5 w-10 text-center">#</th>
                                    <th class="p-2.5">Date</th>
                                    <th class="p-2.5">Site Name</th>
                                    <th class="p-2.5">Material</th>
                                    <th class="p-2.5 text-right">Qty</th>
                                    <th class="p-2.5 text-center">Unit</th>
                                    <th class="p-2.5 text-right">Amount (₹)</th>
                                    <th class="p-2.5 text-center w-28">Action</th>
                                </tr>
                            </thead>
                            <tbody id="recentEntriesTableBody" class="divide-y divide-slate-100 text-slate-700">
                                <!-- Injected via JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- Sticky Material Issue Floating Cart Bar -->
    <div id="floatingCartBar" class="hidden fixed bottom-0 left-0 right-0 z-40 bg-slate-900/95 backdrop-blur-md text-white border-t border-slate-800 shadow-2xl py-3 px-4 sm:px-8 no-print">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-amber-400 text-slate-900 flex items-center justify-center text-lg font-black shadow-md">
                    <i class="fa-solid fa-cart-shopping"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs text-slate-300">Selected Materials:</span>
                        <span id="barCartCount" class="px-2 py-0.5 rounded-full bg-blue-500/30 text-blue-300 font-mono text-xs font-bold">0 Items</span>
                    </div>
                    <div class="flex items-baseline gap-1 mt-0.5">
                        <span class="text-xs text-slate-400">Total Bill:</span>
                        <span id="barCartTotal" class="text-base sm:text-lg font-black text-amber-300 font-mono">₹0.00</span>
                    </div>
                </div>
            </div>

            <div class="flex items-center gap-2 sm:gap-3">
                <button onclick="clearCart()" class="hidden sm:inline-flex px-3 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition">
                    Clear Cart
                </button>
                <button onclick="openCartDrawer()" class="px-5 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-900 text-xs sm:text-sm font-black shadow-lg transition flex items-center gap-2 active:scale-95">
                    <span>Cart Dekhein & Site Par Issue Karein</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        </div>
    </div>

    <!-- Requisition Cart Modal -->
    <div id="cartModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 no-print">
        <div class="bg-white rounded-3xl max-w-3xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden">
            <div class="px-6 py-4 bg-gradient-to-r from-blue-900 to-indigo-900 text-white flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-400 text-slate-900 flex items-center justify-center font-black text-lg">
                        <i class="fa-solid fa-boxes-packing"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-black">Site Material Issue / Requisition Cart</h3>
                        <p class="text-xs text-blue-200">Chune gaye materials ko kisi bhi site par record karein</p>
                    </div>
                </div>
                <button onclick="closeCartDrawer()" class="w-8 h-8 rounded-lg text-white/80 hover:text-white hover:bg-white/10 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <div class="p-6 overflow-y-auto space-y-5 flex-grow">
                <div class="bg-blue-50/70 p-4 rounded-2xl border border-blue-100 space-y-3">
                    <h4 class="text-xs font-bold text-blue-900 uppercase tracking-wider flex items-center gap-1.5">
                        <i class="fa-solid fa-location-dot text-rose-500"></i> Step 1: Site aur Tareekh Chunein
                    </h4>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Koun Se Site Par? <span class="text-rose-500">*</span></label>
                            <select id="checkoutSite" onchange="onCheckoutSiteSelect()" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-bold text-slate-800 bg-white">
                                <!-- Injected via JS -->
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Tareekh (Date) <span class="text-rose-500">*</span></label>
                            <input type="date" id="checkoutDate" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs font-bold text-slate-800 bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Supervisor (Auto)</label>
                            <input type="text" id="checkoutSupervisor" readonly class="w-full rounded-xl border border-slate-200 py-2 px-3 text-xs text-slate-600 bg-slate-100">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Purpose / Work</label>
                            <input type="text" id="checkoutPurpose" placeholder="e.g. Main line work" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs text-slate-800 bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-700 mb-1">Entered By</label>
                            <input type="text" id="checkoutEnteredBy" placeholder="Aapka naam" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs text-slate-800 bg-white">
                        </div>
                    </div>
                </div>

                <div>
                    <h4 class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center justify-between">
                        <span>Step 2: Selected Materials List (<span id="cartModalCount">0</span>)</span>
                        <button onclick="clearCart()" class="text-[11px] text-rose-600 hover:underline font-semibold">Khali Karein</button>
                    </h4>
                    <div class="border border-slate-200 rounded-2xl overflow-hidden">
                        <table class="w-full text-xs text-left">
                            <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                                <tr>
                                    <th class="p-3">Material</th>
                                    <th class="p-3 text-right">Rate</th>
                                    <th class="p-3 text-center">Qty</th>
                                    <th class="p-3 text-right">Total</th>
                                    <th class="p-3 text-center">Hatao</th>
                                </tr>
                            </thead>
                            <tbody id="cartTableBody" class="divide-y divide-slate-100">
                                <!-- Injected via JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="p-4 bg-slate-50 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3">
                <div>
                    <span class="text-xs text-slate-500 block">Kul Bill (Grand Total):</span>
                    <span id="checkoutGrandTotal" class="text-xl font-black text-emerald-600 font-mono">₹0.00</span>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="closeCartDrawer()" class="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-200 transition">Radd Karein</button>
                    <button onclick="confirmCartRequisition()" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-black shadow-md transition flex items-center gap-2">
                        <i class="fa-solid fa-check"></i> Site Par Issue Karein
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Photo Manager Modal (Online View, Search & Upload) -->
    <div id="photoModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 no-print">
        <div class="bg-white rounded-3xl max-w-xl w-full p-6 shadow-2xl border border-slate-200 max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
                <div class="flex items-center gap-2.5">
                    <div class="w-9 h-9 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center font-bold">
                        <i class="fa-solid fa-camera"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-800">Material Photo Badlein / Online Dekhein</h3>
                        <p class="text-[11px] text-slate-400" id="photoModalMatName">Item Name</p>
                    </div>
                </div>
                <button onclick="closePhotoModal()" class="w-8 h-8 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 flex items-center justify-center">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <div class="space-y-4">
                <!-- Live Preview -->
                <div class="flex items-center gap-4 bg-slate-50 p-3.5 rounded-2xl border border-slate-200">
                    <div class="w-24 h-24 rounded-xl bg-slate-200 overflow-hidden flex-shrink-0 border border-slate-300">
                        <img id="modalPreviewImg" src="" alt="Preview" class="w-full h-full object-cover" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src=(window.B64_IMAGES && B64_IMAGES['fittings.jpg']) ? B64_IMAGES['fittings.jpg'] : '';">
                    </div>
                    <div class="text-xs space-y-1">
                        <span class="font-bold text-slate-700 block">Current Photo Preview</span>
                        <span class="text-[11px] text-slate-400 block" id="photoModalCategory">Category</span>
                        <div id="photoStatusNotice" class="text-[11px] leading-tight"></div>
                    </div>
                </div>

                <!-- 1-Click Smart Match for this specific material -->
                <div id="modalSmartSuggested"></div>

                <!-- Option 1: Google Images Search -->
                <div class="p-3.5 rounded-2xl bg-indigo-50/70 border border-indigo-100 flex items-center justify-between">
                    <div>
                        <span class="text-xs font-bold text-indigo-900 block">Google Images Me Dekhein</span>
                        <p class="text-[11px] text-indigo-700 mt-0.5">Online photo search karke link copy karein</p>
                    </div>
                    <a id="googleSearchBtn" href="#" target="_blank" class="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition">
                        <i class="fa-brands fa-google"></i> Search Photo
                    </a>
                </div>

                <!-- Option 2: Paste Online Image URL -->
                <div class="space-y-1.5">
                    <label class="block text-xs font-bold text-slate-700">Online Photo Link (URL) Paste Karein</label>
                    <div class="flex gap-2">
                        <input type="url" id="modalUrlInput" oninput="onModalUrlInput(this.value)" placeholder="Google ya kisi bhi website ka photo link paste karein" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-xs text-slate-800 focus:border-blue-500">
                        <button type="button" onclick="applyModalUrlPreview()" class="px-3 py-2 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold whitespace-nowrap border border-blue-200">Auto Preview</button>
                    </div>
                </div>

                <!-- Option 3: Standard Presets -->
                <div class="space-y-1.5">
                    <label class="block text-xs font-bold text-slate-700">Sabhi Stock Photos (1-Click Instant)</label>
                    <div class="grid grid-cols-4 sm:grid-cols-7 gap-2 text-center text-[10px]">
                        <button type="button" onclick="setPresetPhoto('upvc_pipe.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-lines-leaning text-blue-500 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">UPVC Pipe</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('hdpe_pipe.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-lines-leaning text-slate-800 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">HDPE Pipe</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('submersible_motor.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-water-ladder text-emerald-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Motor</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('starter_panel.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-bolt text-amber-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Starter</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('brass_gate_valve.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-faucet-drip text-rose-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Gate Valve</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('upvc_ball_valve.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-circle-dot text-indigo-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Ball Valve</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('sintex_water_tank.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-oil-well text-cyan-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Sintex Tank</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('cable.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-plug text-purple-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Cable Wire</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('fittings.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-wrench text-slate-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Fittings</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('mat_160_7ba622.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-link text-teal-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Jointers</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('teflon_tape.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-tape text-rose-500 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Teflon Tape</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('hardware_consumables.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-flask text-amber-700 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Solvent</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('water_tap.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-faucet text-sky-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Nal (Tap)</span>
                        </button>
                        <button type="button" onclick="setPresetPhoto('tools.jpg')" class="p-1.5 rounded-xl border border-slate-200 hover:border-blue-500 hover:bg-blue-50 transition">
                            <i class="fa-solid fa-hammer text-orange-600 text-base block mb-0.5"></i>
                            <span class="font-medium text-slate-700">Breaker</span>
                        </button>
                    </div>
                </div>

                <!-- Option 4: Local Upload (Compressed Canvas) -->
                <div class="space-y-1.5 pt-2 border-t border-slate-100">
                    <label class="block text-xs font-bold text-slate-700">Mobile / Computer Se Upload Karein</label>
                    <input type="file" id="modalFileInput" accept="image/*" onchange="onModalFileSelected(this)" class="w-full text-xs text-slate-600 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-blue-50 file:text-blue-700">
                    <p class="text-[10px] text-slate-400">Camera se photo khinchein ya gallery se select karein (Automatic compress ho kar offline save hogi)</p>
                </div>

                <div class="flex items-center justify-between pt-4 border-t border-slate-100">
                    <button type="button" onclick="resetMaterialPhoto()" class="px-3.5 py-2 rounded-xl text-xs font-bold text-rose-600 hover:bg-rose-50 border border-rose-200 transition flex items-center gap-1.5">
                        <i class="fa-solid fa-rotate-left"></i> Default Wapas Layein
                    </button>
                    <div class="flex items-center gap-2">
                        <button type="button" onclick="closePhotoModal()" class="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100">Cancel</button>
                        <button type="button" onclick="saveCustomPhoto()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5">
                            <i class="fa-solid fa-check"></i> Photo Save Karein
                        </button>
                    </div>
                </div>
            </div>
        </div>
    <!-- ========================================== -->
    <!-- EDIT ENTRY MODAL                           -->
    <!-- ========================================== -->
    <div id="editEntryModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm no-print">
        <div class="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                <div class="flex items-center gap-2">
                    <div class="w-9 h-9 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center font-black">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-800">Entry Edit Karein</h3>
                        <p class="text-[11px] text-slate-400">Material consumption record modify karein</p>
                    </div>
                </div>
                <button type="button" onclick="closeEditEntryModal()" class="w-8 h-8 rounded-full hover:bg-slate-100 text-slate-400 hover:text-slate-600 flex items-center justify-center">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <input type="hidden" id="editEntryId">

            <div class="space-y-3 text-xs">
                <div>
                    <label class="block font-bold text-slate-700 mb-1">Site Chunein</label>
                    <select id="editEntrySiteSelect" class="w-full rounded-xl border border-slate-300 py-2 px-3 font-semibold text-slate-800 bg-white">
                        <!-- Injected via JS -->
                    </select>
                </div>

                <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 uppercase font-bold block">Material Description</span>
                        <span id="editEntryMaterialName" class="font-bold text-slate-800 text-sm">Material Name</span>
                    </div>
                    <span id="editEntryUnit" class="px-2 py-0.5 rounded bg-blue-100 text-blue-700 font-mono font-bold text-xs">Unit</span>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block font-bold text-slate-700 mb-1">Tareekh (Date)</label>
                        <input type="date" id="editEntryDate" class="w-full rounded-xl border border-slate-300 py-2 px-3 font-mono font-semibold text-slate-800 bg-white">
                    </div>
                    <div>
                        <label class="block font-bold text-slate-700 mb-1">Quantity (Matra)</label>
                        <input type="number" step="any" id="editEntryQty" oninput="updateEditEntryTotal()" class="w-full rounded-xl border border-slate-300 py-2 px-3 font-mono font-bold text-blue-600 bg-white">
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block font-bold text-slate-700 mb-1">Rate (₹ per unit)</label>
                        <input type="number" step="any" id="editEntryRate" oninput="updateEditEntryTotal()" class="w-full rounded-xl border border-slate-300 py-2 px-3 font-mono font-semibold text-slate-800 bg-white">
                    </div>
                    <div>
                        <label class="block font-bold text-slate-700 mb-1">Total Bill (Auto)</label>
                        <div id="editEntryTotalDisplay" class="w-full rounded-xl border border-slate-200 py-2 px-3 font-mono font-black text-emerald-600 bg-slate-100 text-sm">₹0.00</div>
                    </div>
                </div>

                <div>
                    <label class="block font-bold text-slate-700 mb-1">Kaam / Purpose</label>
                    <input type="text" id="editEntryPurpose" placeholder="e.g. Pipeline fitting, Submersible installation" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-slate-800 bg-white">
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block font-bold text-slate-700 mb-1">Entered By / Supervisor</label>
                        <input type="text" id="editEntryEnteredBy" placeholder="Supervisor Name" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-slate-800 bg-white">
                    </div>
                    <div>
                        <label class="block font-bold text-slate-700 mb-1">Remarks</label>
                        <input type="text" id="editEntryRemarks" placeholder="Optional remarks" class="w-full rounded-xl border border-slate-300 py-2 px-3 text-slate-800 bg-white">
                    </div>
                </div>
            </div>

            <div class="flex items-center justify-end gap-2 pt-3 border-t border-slate-100">
                <button type="button" onclick="closeEditEntryModal()" class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100">Cancel</button>
                <button type="button" onclick="saveEditedEntry()" class="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow transition flex items-center gap-1.5">
                    <i class="fa-solid fa-check"></i> Badlaav Save Karein
                </button>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- RESTORE BACKUP MODAL                       -->
    <!-- ========================================== -->
    <div id="restoreBackupModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm no-print">
        <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                <div class="flex items-center gap-2">
                    <div class="w-9 h-9 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center font-black">
                        <i class="fa-solid fa-cloud-arrow-up"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-slate-800">Backup Restore Karein</h3>
                        <p class="text-[11px] text-slate-400">Purani JSON backup file upload karein</p>
                    </div>
                </div>
                <button type="button" onclick="closeRestoreModal()" class="w-8 h-8 rounded-full hover:bg-slate-100 text-slate-400 hover:text-slate-600 flex items-center justify-center">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <div class="p-4 bg-amber-50 rounded-2xl border border-amber-200 text-amber-900 text-xs space-y-2">
                <div class="font-bold flex items-center gap-1.5">
                    <i class="fa-solid fa-circle-info text-amber-600"></i> Backup File Kaise Restore Karein:
                </div>
                <p class="text-[11px] leading-relaxed">
                    Aapne pehle jo <strong>'Backup Download'</strong> button dabakar JSON file save ki thi, us file ko yahan select karein. Saari entries aur photos dobara load ho jayengi!
                </p>
            </div>

            <div class="space-y-2">
                <label class="block text-xs font-bold text-slate-700">Backup File Chunein (.json):</label>
                <input type="file" id="backupFileInput" accept=".json" onchange="handleBackupFileRestore(this)" class="w-full text-xs text-slate-600 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer">
            </div>

            <div class="flex items-center justify-between pt-3 border-t border-slate-100">
                <button type="button" onclick="undoLastDelete()" class="px-3.5 py-1.5 rounded-xl text-xs font-bold text-indigo-600 hover:bg-indigo-50 border border-indigo-200 transition flex items-center gap-1" title="Aakhiri delete ki hui entry wapas layein">
                    <i class="fa-solid fa-rotate-left"></i> Aakhiri Delete Undo Karein
                </button>
                <button type="button" onclick="closeRestoreModal()" class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100">Band Karein</button>
            </div>
        </div>
    </div>

    <!-- Datalist for fast material autocomplete -->
    <datalist id="allMaterialsDatalist">
        <!-- Injected via JS -->
    </datalist>

    <!-- Embedded Master Data & Full Offline Engine -->
    <script>
        const DEFAULT_SITES = {sites_json};
        const DEFAULT_MATERIALS = {materials_json};
        const DEFAULT_ENTRIES = {entries_json};
        const B64_IMAGES = {b64_json};

        // Reset old local material caches to ensure latest embedded images are active
        localStorage.removeItem('sandip_materials');
        localStorage.removeItem('sandip_sites');

        let appSites = DEFAULT_SITES;
        let appMaterials = DEFAULT_MATERIALS;
        let appEntries = JSON.parse(localStorage.getItem('sandip_entries')) || DEFAULT_ENTRIES;

        // Dual Persistence Storage for Photos (LocalStorage + IndexedDB)
        let customImages = {{}};
        try {{
            customImages = JSON.parse(localStorage.getItem('sandip_custom_images')) || {{}};
        }} catch(e) {{
            customImages = {{}};
        }}

        // IndexedDB Permanent Storage (Immune to browser quota limits, 100% persistent)
        const IDB_NAME = 'SandipMaterialTrackerDB';
        const IDB_STORE = 'custom_photos';
        let idbInstance = null;

        function getPhotoDB() {{
            if (idbInstance) return Promise.resolve(idbInstance);
            return new Promise((resolve) => {{
                if (!window.indexedDB) return resolve(null);
                const req = indexedDB.open(IDB_NAME, 1);
                req.onupgradeneeded = (e) => {{
                    const db = e.target.result;
                    if (!db.objectStoreNames.contains(IDB_STORE)) {{
                        db.createObjectStore(IDB_STORE);
                    }}
                }};
                req.onsuccess = (e) => {{
                    idbInstance = e.target.result;
                    resolve(idbInstance);
                }};
                req.onerror = () => resolve(null);
            }});
        }}

        async function idbSavePhoto(matId, imgData) {{
            try {{
                const db = await getPhotoDB();
                if (!db) return false;
                return new Promise((resolve) => {{
                    const tx = db.transaction(IDB_STORE, 'readwrite');
                    tx.objectStore(IDB_STORE).put(imgData, String(matId));
                    tx.oncomplete = () => resolve(true);
                    tx.onerror = () => resolve(false);
                }});
            }} catch(e) {{
                return false;
            }}
        }}

        async function idbRemovePhoto(matId) {{
            try {{
                const db = await getPhotoDB();
                if (!db) return false;
                return new Promise((resolve) => {{
                    const tx = db.transaction(IDB_STORE, 'readwrite');
                    tx.objectStore(IDB_STORE).delete(String(matId));
                    tx.oncomplete = () => resolve(true);
                    tx.onerror = () => resolve(false);
                }});
            }} catch(e) {{
                return false;
            }}
        }}

        async function idbLoadAllPhotos() {{
            try {{
                const db = await getPhotoDB();
                if (!db) return {{}};
                return new Promise((resolve) => {{
                    const tx = db.transaction(IDB_STORE, 'readonly');
                    const store = tx.objectStore(IDB_STORE);
                    const req = store.openCursor();
                    const result = {{}};
                    req.onsuccess = (e) => {{
                        const cursor = e.target.result;
                        if (cursor) {{
                            result[cursor.key] = cursor.value;
                            cursor.continue();
                        }} else {{
                            resolve(result);
                        }}
                    }};
                    req.onerror = () => resolve({{}});
                }});
            }} catch(e) {{
                return {{}};
            }}
        }}

        // Seamless Dual Storage Sync on Load
        async function syncPhotoStorageOnLoad() {{
            try {{
                const idbPhotos = await idbLoadAllPhotos();
                let needUpdateUI = false;

                // 1. Merge photos from IndexedDB
                for (const [id, val] of Object.entries(idbPhotos)) {{
                    if (val && !customImages[id]) {{
                        customImages[id] = val;
                        needUpdateUI = true;
                    }}
                }}

                // 2. Mirror localStorage photos to IndexedDB
                for (const [id, val] of Object.entries(customImages)) {{
                    if (val && !idbPhotos[id]) {{
                        await idbSavePhoto(id, val);
                    }}
                }}

                // 3. Keep localStorage updated
                try {{
                    localStorage.setItem('sandip_custom_images', JSON.stringify(customImages));
                }} catch(quotaErr) {{}}

                // 4. Update UI if IndexedDB restored photos
                if (needUpdateUI) {{
                    for (const [id, val] of Object.entries(customImages)) {{
                        const cardImg = document.getElementById(`card-img-${{id}}`);
                        if (cardImg && val) cardImg.src = val;
                        const catImg = document.getElementById(`catalog-img-${{id}}`);
                        if (catImg && val) catImg.src = val;
                        if (materialMap[id]) materialMap[id].image_url = val;
                    }}
                }}
            }} catch(err) {{
                console.warn('IDB Sync Error:', err);
            }}
        }}
        if (typeof window !== 'undefined') {{
            setTimeout(syncPhotoStorageOnLoad, 60);
        }}

        // Crisp offline stock image resolver
        function getStockFallbackImg(m) {{
            if (!m) return B64_IMAGES['fittings.jpg'] || '';
            if (m.image_key && B64_IMAGES[m.image_key]) return B64_IMAGES[m.image_key];
            const lower = (m.name || '').toLowerCase();
            if (lower.includes('hdpe')) return B64_IMAGES['hdpe_pipe.jpg'] || '';
            if (lower.includes('submersible') || lower.includes('motor') || lower.includes('pump')) return B64_IMAGES['submersible_motor.jpg'] || '';
            if (lower.includes('starter') || lower.includes('panel')) return B64_IMAGES['starter_panel.jpg'] || '';
            if (lower.includes('gate valve') || lower.includes('brass')) return B64_IMAGES['brass_gate_valve.jpg'] || '';
            if (lower.includes('ball valve')) return B64_IMAGES['upvc_ball_valve.jpg'] || '';
            if (lower.includes('tank') || lower.includes('sintex')) return B64_IMAGES['sintex_water_tank.jpg'] || '';
            if (lower.includes('cable') || lower.includes('wire')) return B64_IMAGES['cable.jpg'] || '';
            if (lower.includes('teflon')) return B64_IMAGES['teflon_tape.jpg'] || '';
            if (lower.includes('tap') || lower.includes('nal')) return B64_IMAGES['water_tap.jpg'] || '';
            if (lower.includes('upvc') || lower.includes('cpvc') || lower.includes('gi pipe')) return B64_IMAGES['upvc_pipe.jpg'] || '';
            if (lower.includes('union')) return B64_IMAGES['mat_160_7ba622.jpg'] || B64_IMAGES['mat_160_gi_union.jpg'] || B64_IMAGES['fittings.jpg'] || '';
            return B64_IMAGES['fittings.jpg'] || '';
        }}

        // SMART IMAGE RESOLVER: Custom image -> fallback stock image
        function getMatImg(m) {{
            if (!m) return B64_IMAGES['fittings.jpg'] || '';
            if (customImages[m.id]) return customImages[m.id];
            return getStockFallbackImg(m);
        }}

        // Non-destructive fallback: Only displays stock fallback, NEVER deletes user's saved photo
        function handleCardImgError(imgEl, matId) {{
            imgEl.onerror = null;
            const m = materialMap[matId];
            imgEl.src = getStockFallbackImg(m);
        }}

        let cart = {{}}; // {{ materialId: {{ id, name, rate, unit, img, qty }} }}
        let activeCategory = 'ALL';

        // Helper Maps
        const materialMap = {{}};
        appMaterials.forEach(m => {{ materialMap[m.id] = m; }});

        const siteMap = {{}};
        appSites.forEach(s => {{ siteMap[s.id] = s; }});

        // Today's date
        const todayStr = new Date().toISOString().split('T')[0];

        // Tab Switching
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.nav-tab').forEach(btn => {{
                btn.classList.remove('bg-amber-400', 'text-slate-950');
                btn.classList.add('text-slate-300');
            }});

            const sec = document.getElementById(`section-${{tabId}}`);
            if (sec) sec.classList.remove('hidden');

            const btn = document.getElementById(`tab-btn-${{tabId}}`);
            if (btn) {{
                btn.classList.remove('text-slate-300');
                btn.classList.add('bg-amber-400', 'text-slate-950');
            }}

            if (tabId === 'sites') renderSitesDirectory();
            if (tabId === 'site-report') renderSiteReport();
            if (tabId === 'daily-report') renderDailyReport();
            if (tabId === 'monthly-report') renderMonthlyReport();
            if (tabId === 'materials') renderMaterialsCatalog();
            if (tabId === 'entry') renderRecentEntriesList();
            if (tabId === 'manpower') initStandaloneManpower();
        }}

        // --- TAB 1: STORE FUNCTIONS ---
        function initStore() {{
            const categories = Array.from(new Set(appMaterials.map(m => m.category || 'General'))).sort();
            const pillsContainer = document.getElementById('categoryPillsContainer');
            pillsContainer.innerHTML = `
                <button onclick="selectCategory('ALL')" class="cat-pill px-3 py-1.5 rounded-xl font-bold whitespace-nowrap bg-blue-600 text-white shadow-sm transition" data-cat="ALL">
                    Sabhi (${{appMaterials.length}})
                </button>
            ` + categories.map(cat => {{
                const cnt = appMaterials.filter(m => m.category === cat).length;
                return `
                    <button onclick="selectCategory('${{cat}}')" class="cat-pill px-3 py-1.5 rounded-xl font-bold whitespace-nowrap bg-slate-100 text-slate-700 hover:bg-slate-200 transition" data-cat="${{cat}}">
                        ${{cat}} (${{cnt}})
                    </button>
                `;
            }}).join('');

            renderProducts();
        }}

        function selectCategory(cat) {{
            activeCategory = cat;
            document.querySelectorAll('.cat-pill').forEach(btn => {{
                if (btn.dataset.cat === cat) {{
                    btn.className = "cat-pill px-3 py-1.5 rounded-xl font-bold whitespace-nowrap bg-blue-600 text-white shadow-sm transition";
                }} else {{
                    btn.className = "cat-pill px-3 py-1.5 rounded-xl font-bold whitespace-nowrap bg-slate-100 text-slate-700 hover:bg-slate-200 transition";
                }}
            }});
            filterStore();
        }}

        function renderProducts() {{
            const grid = document.getElementById('productsGrid');
            grid.innerHTML = appMaterials.map(m => {{
                const img = getMatImg(m);
                return `
                    <div class="product-card bg-white rounded-2xl border border-slate-200/90 hover:border-blue-400 hover:shadow-lg transition flex flex-col justify-between overflow-hidden" 
                         data-id="${{m.id}}" 
                         data-name="${{m.name.toLowerCase()}}" 
                         data-category="${{m.category || 'General'}}"
                         data-rate="${{m.rate}}"
                         data-unit="${{m.unit}}">
                        
                        <div class="relative bg-slate-100 aspect-[4/3] overflow-hidden flex items-center justify-center">
                            <img src="${{img}}" alt="${{m.name}}" id="card-img-${{m.id}}" class="w-full h-full object-cover" referrerpolicy="no-referrer" onerror="handleCardImgError(this, ${{m.id}})">
                            <span class="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/60 text-white text-[10px] font-semibold">
                                ${{m.category || 'General'}}
                            </span>
                            <span class="absolute top-2 right-2 px-2 py-0.5 rounded-md bg-blue-600 text-white text-[10px] font-mono font-bold shadow">
                                ${{m.unit}}
                            </span>
                            <button onclick="openStandalonePhotoModal(${{m.id}})" title="Photo Badlein" class="absolute bottom-2 right-2 px-2.5 py-1 rounded-lg bg-white/95 hover:bg-white text-slate-800 text-[10px] font-bold shadow-md backdrop-blur-sm transition flex items-center gap-1 opacity-90 hover:opacity-100">
                                <i class="fa-solid fa-camera text-blue-600"></i> Photo
                            </button>
                        </div>

                        <div class="p-3.5 flex flex-col justify-between flex-grow">
                            <div>
                                <div class="flex items-center gap-1 text-[9px] font-bold text-amber-600 uppercase mb-1">
                                    <i class="fa-solid fa-certificate text-amber-500"></i> SANDIP KUMAR ASSURED
                                </div>
                                <h3 class="text-xs font-bold text-slate-800 line-clamp-2 leading-tight" title="${{m.name}}">
                                    ${{m.name}}
                                </h3>
                            </div>

                            <div class="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between">
                                <div>
                                    <span class="text-[9px] text-slate-400 block font-medium">Standard Rate</span>
                                    <div class="flex items-baseline gap-0.5">
                                        <span class="text-sm sm:text-base font-black text-emerald-600 font-mono">₹${{m.rate.toFixed(2)}}</span>
                                        <span class="text-[9px] text-slate-500">/${{m.unit}}</span>
                                    </div>
                                </div>

                                <div id="action-container-${{m.id}}">
                                    <button onclick="addToCart(${{m.id}})" class="px-3 py-1 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-sm transition flex items-center gap-1">
                                        <i class="fa-solid fa-plus text-[10px]"></i> ADD
                                    </button>
                                </div>
                            </div>
                        </div>

                    </div>
                `;
            }}).join('');

            filterStore();
        }}

        function filterStore() {{
            const query = (document.getElementById('storeSearchInput').value || '').toLowerCase().trim();
            const cards = document.querySelectorAll('.product-card');
            let visible = 0;

            cards.forEach(card => {{
                const name = card.dataset.name;
                const cat = card.dataset.category;
                const matchesCat = (activeCategory === 'ALL' || cat === activeCategory);
                const matchesQuery = (!query || name.includes(query) || cat.toLowerCase().includes(query));

                if (matchesCat && matchesQuery) {{
                    card.style.display = '';
                    visible++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            document.getElementById('storeVisibleCount').textContent = visible;
            const noRes = document.getElementById('noStoreResults');
            if (visible === 0) noRes.classList.remove('hidden');
            else noRes.classList.add('hidden');
        }}

        // Cart Stepper & Actions
        function addToCart(id) {{
            const m = materialMap[id];
            if (!m) return;
            const img = getMatImg(m);
            if (!cart[id]) {{
                cart[id] = {{ id: m.id, name: m.name, rate: m.rate, unit: m.unit, img: img, qty: 1 }};
            }} else {{
                cart[id].qty += 1;
            }}
            updateCardStepper(id);
            updateCartUI();
        }}

        function decreaseCart(id) {{
            if (cart[id]) {{
                cart[id].qty -= 1;
                if (cart[id].qty <= 0) delete cart[id];
            }}
            updateCardStepper(id);
            updateCartUI();
        }}

        function setCartQty(id, qty) {{
            qty = parseFloat(qty) || 0;
            if (qty <= 0) {{
                delete cart[id];
            }} else {{
                if (cart[id]) cart[id].qty = qty;
            }}
            updateCardStepper(id);
            updateCartUI();
        }}

        function updateCardStepper(id) {{
            const container = document.getElementById(`action-container-${{id}}`);
            if (!container) return;

            if (cart[id] && cart[id].qty > 0) {{
                const it = cart[id];
                container.innerHTML = `
                    <div class="flex items-center rounded-xl border border-blue-600 bg-white overflow-hidden text-xs">
                        <button onclick="decreaseCart(${{id}})" class="px-2 py-1 bg-blue-50 text-blue-700 font-bold hover:bg-blue-100">-</button>
                        <input type="number" step="any" min="0" value="${{it.qty}}" onchange="setCartQty(${{id}}, this.value)" class="w-10 text-center font-bold text-slate-800 text-xs py-0.5 focus:outline-none">
                        <button onclick="addToCart(${{id}})" class="px-2 py-1 bg-blue-50 text-blue-700 font-bold hover:bg-blue-100">+</button>
                    </div>
                `;
            }} else {{
                container.innerHTML = `
                    <button onclick="addToCart(${{id}})" class="px-3 py-1 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-sm transition flex items-center gap-1">
                        <i class="fa-solid fa-plus text-[10px]"></i> ADD
                    </button>
                `;
            }}
        }}

        function updateCartUI() {{
            const items = Object.values(cart);
            let count = items.length;
            let grandTotal = items.reduce((sum, it) => sum + (it.qty * it.rate), 0);

            const bar = document.getElementById('floatingCartBar');
            if (count > 0) {{
                bar.classList.remove('hidden');
                document.getElementById('barCartCount').textContent = `${{count}} Items`;
                document.getElementById('barCartTotal').textContent = `₹${{grandTotal.toLocaleString('en-IN', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}`;
            }} else {{
                bar.classList.add('hidden');
            }}
        }}

        function clearCart() {{
            const ids = Object.keys(cart);
            cart = {{}};
            ids.forEach(id => updateCardStepper(id));
            updateCartUI();
        }}

        function openCartDrawer() {{
            renderCartModal();
            document.getElementById('cartModal').classList.remove('hidden');
        }}

        function closeCartDrawer() {{
            document.getElementById('cartModal').classList.add('hidden');
        }}

        function renderCartModal() {{
            const items = Object.values(cart);
            document.getElementById('cartModalCount').textContent = items.length;

            const tbody = document.getElementById('cartTableBody');
            let grandTotal = 0;

            if (items.length === 0) {{
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" class="py-6 text-center text-slate-400">
                            Cart khali hai. Store se '+ ADD' karein!
                        </td>
                    </tr>
                `;
            }} else {{
                tbody.innerHTML = items.map(it => {{
                    const total = it.qty * it.rate;
                    grandTotal += total;
                    return `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-3">
                                <span class="font-bold text-slate-800 block text-xs">${{it.name}}</span>
                                <span class="text-[10px] text-slate-400 font-mono">Unit: ${{it.unit}}</span>
                            </td>
                            <td class="p-3 text-right font-mono text-slate-600">₹${{it.rate.toFixed(2)}}</td>
                            <td class="p-3 text-center">
                                <input type="number" step="any" min="0" value="${{it.qty}}" onchange="setCartQty(${{it.id}}, this.value); renderCartModal();" class="w-14 text-center font-bold text-slate-800 border rounded py-0.5">
                            </td>
                            <td class="p-3 text-right font-mono font-bold text-emerald-600">₹${{total.toFixed(2)}}</td>
                            <td class="p-3 text-center">
                                <button onclick="setCartQty(${{it.id}}, 0); renderCartModal();" class="text-rose-500 hover:text-rose-700">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </td>
                        </tr>
                    `;
                }}).join('');
            }}

            document.getElementById('checkoutGrandTotal').textContent = `₹${{grandTotal.toLocaleString('en-IN', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}`;

            // Setup Sites Select in Checkout
            const select = document.getElementById('checkoutSite');
            if (select.children.length === 0) {{
                select.innerHTML = `<option value="">-- Site Chunein (1 to 19) --</option>` + appSites.map(s => `
                    <option value="${{s.id}}" data-supervisor="${{s.supervisor || ''}}">${{s.code}} - ${{s.name}}</option>
                `).join('');
                document.getElementById('checkoutDate').value = todayStr;
            }}
        }}

        function onCheckoutSiteSelect() {{
            const select = document.getElementById('checkoutSite');
            const opt = select.options[select.selectedIndex];
            document.getElementById('checkoutSupervisor').value = opt ? (opt.dataset.supervisor || '') : '';
        }}

        function confirmCartRequisition() {{
            const siteId = document.getElementById('checkoutSite').value;
            const date = document.getElementById('checkoutDate').value;
            const purpose = document.getElementById('checkoutPurpose').value.trim();
            const enteredBy = document.getElementById('checkoutEnteredBy').value.trim();
            const items = Object.values(cart);

            if (!siteId) {{ alert("Kripya Site chunein!"); return; }}
            if (!date) {{ alert("Kripya Date select karein!"); return; }}
            if (items.length === 0) {{ alert("Cart khali hai!"); return; }}

            const siteObj = siteMap[siteId];

            items.forEach(it => {{
                appEntries.unshift({{
                    id: Date.now() + Math.floor(Math.random() * 1000),
                    site_id: parseInt(siteId),
                    material_id: it.id,
                    quantity: it.qty,
                    rate: it.rate,
                    total_amount: it.qty * it.rate,
                    usage_date: date,
                    purpose: purpose,
                    entered_by: enteredBy,
                    remarks: "Issued from Store Cart",
                    site_name: siteObj ? siteObj.name : "Site",
                    site_code: siteObj ? siteObj.code : "",
                    site_supervisor: siteObj ? siteObj.supervisor : "",
                    material_name: it.name,
                    material_unit: it.unit,
                    material_image: it.img
                }});
            }});

            // Save to LocalStorage
            localStorage.setItem('sandip_entries', JSON.stringify(appEntries));

            alert(`✅ Safalta se save ho gaya!\n${{items.length}} materials ${{siteObj ? siteObj.name : ''}} par issue darj ho gaye hain.`);
            clearCart();
            closeCartDrawer();

            // Switch to site report to show results
            document.getElementById('reportSiteSelect').value = siteId;
            switchTab('site-report');
        }}

        // --- TAB 2: 19 SITES DIRECTORY ---
        function renderSitesDirectory() {{
            const grid = document.getElementById('sitesGrid');
            grid.innerHTML = appSites.map(s => {{
                const siteEntries = appEntries.filter(e => e.site_id == s.id);
                const totalCost = siteEntries.reduce((sum, e) => sum + (e.total_amount || 0), 0);

                return `
                    <div class="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-sm hover:border-blue-400 hover:shadow-md transition space-y-3">
                        <div class="flex items-start justify-between">
                            <div>
                                <span class="px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-700 font-mono text-[10px] font-bold">
                                    ${{s.code}}
                                </span>
                                <h3 class="text-base font-black text-slate-800 mt-1">${{s.name}}</h3>
                                <p class="text-[11px] text-slate-400"><i class="fa-solid fa-map-pin text-rose-500 mr-1"></i>${{s.location || 'Location Not Set'}}</p>
                            </div>
                            <span class="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 text-[10px] font-bold">Active</span>
                        </div>

                        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100 space-y-1.5 text-xs">
                            <div class="flex items-center justify-between">
                                <span class="text-slate-500"><i class="fa-solid fa-user-tie text-blue-500 mr-1.5"></i>Supervisor:</span>
                                <span class="font-bold text-slate-800">${{s.supervisor || 'N/A'}}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span class="text-slate-500"><i class="fa-solid fa-phone text-emerald-500 mr-1.5"></i>Contact:</span>
                                <a href="tel:${{s.contact || ''}}" class="font-mono font-bold text-blue-600 hover:underline">${{s.contact || 'N/A'}}</a>
                            </div>
                        </div>

                        <div class="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                            <div>
                                <span class="text-[10px] text-slate-400 block">Total Expenditure</span>
                                <span class="font-mono font-black text-emerald-600">₹${{totalCost.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</span>
                            </div>
                            <button onclick="viewSiteSpecificReport(${{s.id}})" class="px-3 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold transition flex items-center gap-1">
                                <span>Report</span> <i class="fa-solid fa-arrow-right text-[10px]"></i>
                            </button>
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        function viewSiteSpecificReport(siteId) {{
            document.getElementById('reportSiteSelect').value = siteId;
            switchTab('site-report');
        }}

        // --- TAB 3: SITE-WISE REPORT ---
        
        
        // --- STANDALONE DAILY MANPOWER ATTENDANCE LOGIC ---
        const MANPOWER_SITES = [
            "Madhubani", "Singhiya", "Sonpur", "Sheohar", "Jhanjharpur",
            "Ekma", "Siwan", "Chhapra", "Andar", "Mairwa",
            "Basantpur", "Hasanpura", "Kati", "Darbhanga", "Maharajganj",
            "Guthani", "Barhariya", "Sahebganj", "Mirganj", "Naubathpur", "Parsa"
        ];

        // Seeded sample matching photo for 2026-10-08
        const PHOTO_SAMPLE_MANPOWER = {{
            "madhubani": {{ si: 1, sup: 1, elec: 1, gi: 0, deo: 1, plumb: 2, help: 3, oth: 0, rem: "RAINING" }},
            "singhiya": {{ si: 1, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 2, help: 2, oth: 0, rem: "" }},
            "sonpur": {{ si: 1, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 1, help: 3, oth: 0, rem: "" }},
            "sheohar": {{ si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "NOT REACHABLE" }},
            "jhanjharpur": {{ si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 1, oth: 0, rem: "RAINING" }},
            "ekma": {{ si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" }},
            "siwan": {{ si: 1, sup: 1, elec: 0, gi: 3, deo: 0, plumb: 0, help: 3, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" }},
            "chhapra": {{ si: 1, sup: 2, elec: 0, gi: 4, deo: 0, plumb: 0, help: 0, oth: 0, rem: "" }},
            "andar": {{ si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "SITE CLOSED DUE TO MANPOWER" }},
            "mairwa": {{ si: 0, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 2, help: 1, oth: 0, rem: "" }},
            "basantpur": {{ si: 0, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 1, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" }},
            "hasanpura": {{ si: 0, sup: 1, elec: 0, gi: 3, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" }},
            "kati": {{ si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "" }},
            "darbhanga": {{ si: 1, sup: 1, elec: 0, gi: 0, deo: 1, plumb: 4, help: 4, oth: 0, rem: "" }},
            "maharajganj": {{ si: 1, sup: 1, elec: 0, gi: 3, deo: 0, plumb: 0, help: 2, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" }},
            "guthani": {{ si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" }},
            "barhariya": {{ si: 0, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 2, help: 2, oth: 0, rem: "SITE CLOSED(WORKERS IN OWNER HOME)" }},
            "sahebganj": {{ si: 0, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" }},
            "mirganj": {{ si: 1, sup: 1, elec: 0, gi: 0, deo: 0, plumb: 4, help: 2, oth: 0, rem: "" }},
            "naubathpur": {{ si: 1, sup: 1, elec: 0, gi: 1, deo: 0, plumb: 0, help: 2, oth: 0, rem: "" }},
            "parsa": {{ si: 0, sup: 0, elec: 0, gi: 0, deo: 0, plumb: 0, help: 0, oth: 0, rem: "" }}
        }};

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

            const allStored = JSON.parse(localStorage.getItem('sandip_manpower_store') || '{{}}');
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
            let csv = `DATE,${{dateStr}}\n`;
            csv += `SL.NO,SITE NAME,SITE INCHARGE,SUPERVISOR,ELECTRICIAN,GI MISTRI,D E O,PLUMBER,HELPER,OTHER,TOTAL,REMARKS\n`;

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

                csv += `${{idx+1}},${{name}},${{si}},${{sup}},${{elec}},${{gi}},${{deo}},${{plumb}},${{help}},${{oth}},${{tot}},${{rem}}\n`;
            }});

            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `MANPOWER_${{dateStr}}.csv`;
            link.click();
        }}

        // --- CROSS-SITE AUDIT & SUPERVISOR DETECTION ---
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
                return '<span class="text-slate-400 text-xs">-</span>';
            }}

            if (isCrossSiteMismatch(e)) {{
                return `
                    <div class="inline-flex flex-col text-left">
                        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-black bg-amber-100 text-amber-900 border border-amber-300 shadow-sm">
                            <i class="fa-solid fa-triangle-exclamation text-amber-600"></i> 🚨 Cross-Site Entry
                        </span>
                        <span class="text-xs font-black text-slate-900 mt-0.5 flex items-center gap-1">
                            <i class="fa-solid fa-user-pen text-amber-600"></i> By: ${{enteredBy}}
                        </span>
                        <span class="text-[10px] text-slate-500 font-semibold">Site Incharge: ${{officialSupervisor}}</span>
                    </div>
                `;
            }} else {{
                const name = enteredBy || officialSupervisor;
                return `
                    <div class="inline-flex items-center gap-1.5 text-slate-700 text-xs">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
                        <span class="font-bold text-slate-800">${{name}}</span>
                        <span class="text-[10px] text-emerald-700 bg-emerald-50 border border-emerald-200 px-1 rounded font-semibold">✓ Incharge</span>
                    </div>
                `;
            }}
        }}

        function toggleCrossSiteFilter() {{
            isCrossSiteFilterActive = !isCrossSiteFilterActive;
            const btn = document.getElementById('btnToggleCrossSite');
            if (btn) {{
                if (isCrossSiteFilterActive) {{
                    btn.className = "px-3.5 py-2 rounded-xl text-xs font-black bg-amber-500 text-white shadow-md flex items-center gap-2 transition";
                    btn.innerHTML = `<i class="fa-solid fa-filter"></i> <span>Cross-Site Filter: ON (Sabhi Entries Dekhne Ke Liye Click Karein)</span>`;
                }} else {{
                    btn.className = "px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 transition flex items-center gap-2 shadow-sm";
                    btn.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-amber-600 text-sm"></i> <span>🚨 Keval Cross-Site / Dusre Supervisor Ki Entries Filter Karein</span>`;
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
        }}

        function renderSiteReport() {{
            const select = document.getElementById('reportSiteSelect');
            if (select.children.length === 0) {{
                select.innerHTML = appSites.map(s => `
                    <option value="${{s.id}}">${{s.code}} - ${{s.name}}</option>
                `).join('');
            }}

            const siteId = select.value || appSites[0].id;
            const fromDate = document.getElementById('reportFromDate').value;
            const toDate = document.getElementById('reportToDate').value;

            const site = siteMap[siteId];

            let filtered = appEntries.filter(e => e.site_id == siteId);
            if (fromDate) filtered = filtered.filter(e => e.usage_date >= fromDate);
            if (toDate) filtered = filtered.filter(e => e.usage_date <= toDate);

            // Summary calculations
            const grandTotal = filtered.reduce((sum, e) => sum + (e.total_amount || 0), 0);
            const totalQtySum = filtered.reduce((sum, e) => sum + (e.quantity || 0), 0);

            // Aggregated by material
            const agg = {{}};
            filtered.forEach(e => {{
                if (!agg[e.material_id]) {{
                    agg[e.material_id] = {{
                        id: e.material_id,
                        name: e.material_name,
                        unit: e.material_unit,
                        category: e.material_category || 'General',
                        quantity: 0,
                        total_amount: 0
                    }};
                }}
                agg[e.material_id].quantity += (e.quantity || 0);
                agg[e.material_id].total_amount += (e.total_amount || 0);
            }});
            const summaryList = Object.values(agg).sort((a,b) => b.total_amount - a.total_amount);

            // Render Stat Cards
            document.getElementById('siteReportSummaryCards').innerHTML = `
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Chuni Hui Site</span>
                    <span class="text-lg font-black text-slate-800 block">${{site ? site.name : ''}} (${{site ? site.code : ''}})</span>
                    <span class="text-xs text-blue-600 mt-1 block">Supervisor: ${{site ? site.supervisor : 'N/A'}} (${{site ? site.contact : ''}})</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Kul Materials / Entries</span>
                    <span class="text-2xl font-black text-slate-800 font-mono block">${{summaryList.length}} Materials</span>
                    <span class="text-xs text-slate-500 mt-1 block">${{filtered.length}} alag-alag issue slips</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Is Site Ka Kul Kharcha (Bill)</span>
                    <span class="text-2xl font-black text-emerald-600 font-mono block">₹${{grandTotal.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</span>
                    <span class="text-xs text-emerald-600 mt-1 block font-medium">Auto-Calculated Total</span>
                </div>
            `;

            // Render Summary Table
            const sumTbody = document.getElementById('siteReportSummaryTbody');
            if (summaryList.length === 0) {{
                sumTbody.innerHTML = `<tr><td colspan="7" class="py-6 text-center text-slate-400">Is date range me koi record nahi mila.</td></tr>`;
            }} else {{
                sumTbody.innerHTML = summaryList.map((item, idx) => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-3 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                        <td class="p-3 font-bold text-slate-800">${{item.name}}</td>
                        <td class="p-3"><span class="px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 text-[10px]">${{item.category}}</span></td>
                        <td class="p-3 text-center font-mono font-bold text-slate-600">${{item.unit}}</td>
                        <td class="p-3 text-right font-mono font-bold text-blue-600">${{item.quantity.toFixed(2)}}</td>
                        <td class="p-3 text-right font-mono text-slate-600">₹${{(item.quantity > 0 ? (item.total_amount / item.quantity) : 0).toFixed(2)}}</td>
                        <td class="p-3 text-right font-mono font-bold text-emerald-600">₹${{item.total_amount.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
                    </tr>
                `).join('') + `
                    <tr class="bg-slate-50 font-black text-slate-900 border-t-2 border-slate-200">
                        <td colspan="4" class="p-3 text-right uppercase">Grand Total:</td>
                        <td class="p-3 text-right font-mono text-blue-700">${{totalQtySum.toFixed(2)}}</td>
                        <td></td>
                        <td class="p-3 text-right font-mono text-emerald-700 text-sm">₹${{grandTotal.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
                    </tr>
                `;
            }}

            // Cross-Site filtering if active
            const totalSiteEntries = filtered.length;
            const crossSiteCount = filtered.filter(e => isCrossSiteMismatch(e)).length;
            const badgeCountEl = document.getElementById('crossSiteBadgeCount');
            if (badgeCountEl) {{
                badgeCountEl.innerHTML = crossSiteCount > 0 
                    ? `<span class="text-amber-700 font-bold bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">⚠️ Is site me ${{crossSiteCount}} Cross-Site entries mili hain</span>`
                    : `<span class="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded-lg">✓ Sabhi entries authorised incharge dwara hain</span>`;
            }}

            if (isCrossSiteFilterActive) {{
                filtered = filtered.filter(e => isCrossSiteMismatch(e));
            }}

            // Render Logs Table
            const logsTbody = document.getElementById('siteReportLogsTbody');
            if (filtered.length === 0) {{
                logsTbody.innerHTML = `<tr><td colspan="10" class="py-6 text-center text-slate-400">Koi log uplabdh nahi hai.</td></tr>`;
            }} else {{
                logsTbody.innerHTML = filtered.map((e, idx) => `
                    <tr class="hover:bg-slate-50 transition ${{isCrossSiteMismatch(e) ? 'bg-amber-50/40' : ''}}">
                        <td class="p-3 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                        <td class="p-3 font-mono font-bold text-slate-700">${{e.usage_date}}</td>
                        <td class="p-3 font-bold text-slate-800">${{e.material_name}}</td>
                        <td class="p-3 text-right font-mono font-bold text-blue-600">${{e.quantity}}</td>
                        <td class="p-3 text-center font-mono text-slate-500">${{e.material_unit}}</td>
                        <td class="p-3 text-right font-mono text-slate-600">₹${{(e.rate || 0).toFixed(2)}}</td>
                        <td class="p-3 text-right font-mono font-bold text-emerald-600">₹${{(e.total_amount || 0).toFixed(2)}}</td>
                        <td class="p-3 text-slate-500 text-[11px]">${{e.purpose || '-'}}</td>
                        <td class="p-3">${{getSupervisorAuditBadge(e)}}</td>
                        <td class="p-3 text-center">
                            <div class="flex items-center justify-center gap-1.5">
                                <button onclick="openEditEntryModal(${{e.id}})" class="px-2 py-1 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 font-bold text-[11px] transition flex items-center gap-1" title="Edit Karein">
                                    <i class="fa-solid fa-pen-to-square"></i> Edit
                                </button>
                                <button onclick="deleteStandaloneEntry(${{e.id}})" class="px-2 py-1 rounded-lg bg-rose-50 text-rose-600 hover:bg-rose-100 font-bold text-[11px] transition flex items-center gap-1" title="Delete Karein">
                                    <i class="fa-solid fa-trash-can"></i> Hatao
                                </button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            }}
        }}

        // --- TAB 4: DAILY REPORT ---
        function renderDailyReport() {{
            let dateInput = document.getElementById('dailyReportDateInput');
            if (!dateInput.value) dateInput.value = todayStr;
            const chosenDate = dateInput.value;

            const dayEntries = appEntries.filter(e => e.usage_date === chosenDate);
            const dayGrandTotal = dayEntries.reduce((sum, e) => sum + (e.total_amount || 0), 0);

            // Group by site
            const siteGroups = {{}};
            dayEntries.forEach(e => {{
                if (!siteGroups[e.site_id]) siteGroups[e.site_id] = [];
                siteGroups[e.site_id].push(e);
            }});

            const activeSiteCount = Object.keys(siteGroups).length;

            document.getElementById('dailyReportSummaryCards').innerHTML = `
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Chuni Hui Tareekh</span>
                    <span class="text-xl font-black text-slate-800 font-mono block">${{chosenDate}}</span>
                    <span class="text-xs text-blue-600 mt-1 block">Daily Material Consumption</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Active Sites on this Date</span>
                    <span class="text-2xl font-black text-slate-800 font-mono block">${{activeSiteCount}} Sites</span>
                    <span class="text-xs text-slate-500 mt-1 block">${{dayEntries.length}} materials consumed</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Is Din Ka Kul Kharcha (Day Total)</span>
                    <span class="text-2xl font-black text-emerald-600 font-mono block">₹${{dayGrandTotal.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</span>
                    <span class="text-xs text-emerald-600 mt-1 block">Calculated across all sites</span>
                </div>
            `;

            const container = document.getElementById('dailyReportEntriesContainer');
            if (activeSiteCount === 0) {{
                container.innerHTML = `
                    <div class="bg-white rounded-2xl p-12 text-center border border-slate-200">
                        <i class="fa-solid fa-calendar-xmark text-4xl text-slate-300 mb-3 block"></i>
                        <h4 class="text-base font-bold text-slate-700">${{chosenDate}} ko koi entry darj nahi hai</h4>
                        <p class="text-xs text-slate-400 mt-1">Upar se doosri date select karein ya 'Material Store' se naya issue karein.</p>
                    </div>
                `;
                return;
            }}

            container.innerHTML = Object.entries(siteGroups).map(([sId, items]) => {{
                const sObj = siteMap[sId];
                const sTotal = items.reduce((sum, it) => sum + (it.total_amount || 0), 0);
                return `
                    <div class="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-sm space-y-3">
                        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
                            <div>
                                <span class="px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 font-mono text-[10px] font-bold">${{sObj ? sObj.code : ''}}</span>
                                <h3 class="text-base font-black text-slate-800 mt-0.5">${{sObj ? sObj.name : 'Site'}}</h3>
                                <p class="text-[11px] text-slate-400">Supervisor: ${{sObj ? sObj.supervisor : 'N/A'}} (${{sObj ? sObj.contact : ''}})</p>
                            </div>
                            <div class="text-right">
                                <span class="text-[10px] text-slate-400 block font-medium">Site Total</span>
                                <span class="text-base font-black text-emerald-600 font-mono">₹${{sTotal.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</span>
                            </div>
                        </div>

                        <div class="overflow-x-auto border border-slate-200 rounded-xl">
                            <table class="w-full text-left text-xs border-collapse">
                                <thead class="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                                    <tr>
                                        <th class="p-2.5 w-10 text-center">#</th>
                                        <th class="p-2.5">Material</th>
                                        <th class="p-2.5 text-right">Qty</th>
                                        <th class="p-2.5 text-center">Unit</th>
                                        <th class="p-2.5 text-right">Rate (₹)</th>
                                        <th class="p-2.5 text-right">Amount (₹)</th>
                                        <th class="p-2.5">Remarks / Purpose</th>
                                        <th class="p-2.5 text-center w-28">Action</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100 text-slate-700">
                                    ${{items.map((it, idx) => `
                                        <tr>
                                            <td class="p-2.5 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                                            <td class="p-2.5 font-bold text-slate-800">${{it.material_name}}</td>
                                            <td class="p-2.5 text-right font-mono font-bold text-blue-600">${{it.quantity}}</td>
                                            <td class="p-2.5 text-center font-mono text-slate-500">${{it.material_unit}}</td>
                                            <td class="p-2.5 text-right font-mono text-slate-600">₹${{(it.rate || 0).toFixed(2)}}</td>
                                            <td class="p-2.5 text-right font-mono font-bold text-emerald-600">₹${{(it.total_amount || 0).toFixed(2)}}</td>
                                            <td class="p-2.5 text-slate-500 text-[11px]">${{it.purpose || it.remarks || '-'}}</td>
                                            <td class="p-2.5 text-center">
                                                <div class="flex items-center justify-center gap-1.5">
                                                    <button onclick="openEditEntryModal(${{it.id}})" class="px-2 py-1 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 font-bold text-[11px] transition flex items-center gap-1" title="Edit Karein">
                                                        <i class="fa-solid fa-pen-to-square"></i> Edit
                                                    </button>
                                                    <button onclick="deleteStandaloneEntry(${{it.id}})" class="px-2 py-1 rounded-lg bg-rose-50 text-rose-600 hover:bg-rose-100 font-bold text-[11px] transition flex items-center gap-1" title="Delete Karein">
                                                        <i class="fa-solid fa-trash-can"></i> Hatao
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    `).join('')}}
                                </tbody>
                            </table>
                        </div>
                    </div>
                `;
            }}).join('');
        }}

        // --- TAB: MAHINA-WAR (MONTHLY) REPORT ---
        function renderMonthlyReport() {{
            let monthInput = document.getElementById('monthlyReportMonthInput');
            if (!monthInput.value) {{
                monthInput.value = todayStr.slice(0, 7);
            }}
            const chosenMonth = monthInput.value; // e.g. "2026-10"

            const monthEntries = appEntries.filter(e => (e.usage_date || '').startsWith(chosenMonth));
            const monthTotalCost = monthEntries.reduce((sum, e) => sum + (e.total_amount || 0), 0);

            // 19 Sites breakdown
            const siteBreakdown = appSites.map(s => {{
                const sEntries = monthEntries.filter(e => e.site_id == s.id);
                const sTotal = sEntries.reduce((sum, e) => sum + (e.total_amount || 0), 0);
                const sQty = sEntries.reduce((sum, e) => sum + (e.quantity || 0), 0);
                return {{
                    site: s,
                    entries: sEntries,
                    items_count: sEntries.length,
                    total_qty: sQty,
                    total_cost: sTotal
                }};
            }});

            // Sort sites by highest spending first
            siteBreakdown.sort((a, b) => b.total_cost - a.total_cost);

            const activeSites = siteBreakdown.filter(s => s.total_cost > 0);
            const topSite = activeSites.length > 0 ? activeSites[0] : null;

            // Monthly Summary Cards
            document.getElementById('monthlyReportSummaryCards').innerHTML = `
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Chuna Hua Mahina</span>
                    <span class="text-xl font-black text-slate-800 font-mono block">${{chosenMonth}}</span>
                    <span class="text-xs text-blue-600 mt-1 block">Monthly Consolidated</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Kul Mahine Ka Kharch</span>
                    <span class="text-xl font-black text-emerald-600 font-mono block">₹${{monthTotalCost.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</span>
                    <span class="text-xs text-emerald-600 mt-1 block">19 Sites Grand Total</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Active Sites This Month</span>
                    <span class="text-xl font-black text-indigo-700 font-mono block">${{activeSites.length}} / 19 Sites</span>
                    <span class="text-xs text-indigo-600 mt-1 block">Jahan saman issue hua</span>
                </div>
                <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
                    <span class="text-xs text-slate-400 font-bold block mb-1">Sabse Zyada Kharch</span>
                    <span class="text-base font-black text-slate-800 truncate block" title="${{topSite ? topSite.site.name : 'Koi Nahi'}}">${{topSite ? topSite.site.name : 'Koi Nahi'}}</span>
                    <span class="text-xs text-emerald-600 font-mono font-bold mt-1 block">${{topSite ? ('₹' + topSite.total_cost.toLocaleString('en-IN', {{minimumFractionDigits: 2}})) : '₹0.00'}}</span>
                </div>
            `;

            // Render 19 Sites Breakdown Table
            const sitesTbody = document.getElementById('monthlySitesTableBody');
            sitesTbody.innerHTML = siteBreakdown.map((sb, idx) => {{
                const pct = monthTotalCost > 0 ? (sb.total_cost / monthTotalCost * 100) : 0;
                return `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-3 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                        <td class="p-3 font-mono font-bold text-blue-700">
                            <span class="px-2 py-0.5 rounded bg-blue-100 text-blue-800 text-[11px]">${{sb.site.code}}</span>
                        </td>
                        <td class="p-3 font-bold text-slate-800">
                            ${{sb.site.name}}
                            ${{sb.site.location ? `<div class="text-[10px] text-slate-400 font-normal"><i class="fa-solid fa-map-pin text-rose-500 mr-0.5"></i>${{sb.site.location}}</div>` : ''}}
                        </td>
                        <td class="p-3">
                            <div class="font-medium text-slate-700">${{sb.site.supervisor || 'N/A'}}</div>
                            ${{sb.site.contact ? `<div class="text-[11px] font-mono text-slate-400">${{sb.site.contact}}</div>` : ''}}
                        </td>
                        <td class="p-3 text-right font-mono font-bold text-blue-600">${{sb.items_count}} items</td>
                        <td class="p-3 text-right font-mono font-black text-emerald-700 text-sm">
                            ₹${{sb.total_cost.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}
                        </td>
                        <td class="p-3">
                            <div class="flex items-center gap-2">
                                <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden border border-slate-200">
                                    <div class="bg-blue-600 h-2 rounded-full" style="width: ${{pct}}%"></div>
                                </div>
                                <span class="font-mono text-[10px] font-bold text-slate-600 whitespace-nowrap">${{pct.toFixed(1)}}%</span>
                            </div>
                        </td>
                        <td class="p-3 text-center">
                            <button onclick="viewSiteSpecificReport(${{sb.site.id}})" class="px-2.5 py-1 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold text-[11px] transition inline-flex items-center gap-1">
                                <span>Report</span> <i class="fa-solid fa-arrow-right text-[9px]"></i>
                            </button>
                        </td>
                    </tr>
                `;
            }}).join('');

            document.getElementById('monthlySitesTableFoot').innerHTML = `
                <tr>
                    <td colspan="4" class="p-3 text-right uppercase text-xs">Month Grand Total:</td>
                    <td class="p-3 text-right font-mono text-blue-700">${{monthEntries.length}} items</td>
                    <td class="p-3 text-right font-mono text-emerald-800 text-base">₹${{monthTotalCost.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
                    <td colspan="2" class="p-3 text-slate-500 font-mono text-xs">100.0%</td>
                </tr>
            `;

            // Calculate Top 10 Materials Consumed in this Month
            const matTotals = {{}};
            monthEntries.forEach(e => {{
                const key = e.material_name;
                if (!matTotals[key]) {{
                    matTotals[key] = {{ name: e.material_name, unit: e.material_unit, qty: 0, cost: 0 }};
                }}
                matTotals[key].qty += (e.quantity || 0);
                matTotals[key].cost += (e.total_amount || 0);
            }});

            const topMatsList = Object.values(matTotals).sort((a, b) => b.cost - a.cost).slice(0, 10);
            const matsGrid = document.getElementById('monthlyTopMaterialsGrid');
            if (topMatsList.length === 0) {{
                matsGrid.innerHTML = `<div class="col-span-full py-6 text-center text-slate-400">Is mahine koi material use nahi hua hai.</div>`;
            }} else {{
                matsGrid.innerHTML = topMatsList.map((m, idx) => `
                    <div class="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="w-6 h-6 rounded-full bg-amber-400 text-slate-900 font-black text-xs flex items-center justify-center">#${{idx + 1}}</span>
                            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-200 text-slate-600">${{m.unit}}</span>
                        </div>
                        <h4 class="text-xs font-bold text-slate-800 line-clamp-2 h-8" title="${{m.name}}">${{m.name}}</h4>
                        <div class="pt-2 border-t border-slate-200 flex items-center justify-between text-xs">
                            <div>
                                <span class="text-[9px] text-slate-400 block">Total Qty</span>
                                <span class="font-mono font-bold text-blue-700">${{m.qty.toFixed(1)}}</span>
                            </div>
                            <div class="text-right">
                                <span class="text-[9px] text-slate-400 block">Total Bill</span>
                                <span class="font-mono font-black text-emerald-700">₹${{Math.round(m.cost).toLocaleString('en-IN')}}</span>
                            </div>
                        </div>
                    </div>
                `).join('');
            }}

            // Day-by-day Trend in this month
            const dayGroups = {{}};
            monthEntries.forEach(e => {{
                const d = e.usage_date;
                if (!dayGroups[d]) dayGroups[d] = [];
                dayGroups[d].push(e);
            }});

            const sortedDates = Object.keys(dayGroups).sort();
            document.getElementById('monthlyActiveDaysCount').textContent = `${{sortedDates.length}} Active Days`;

            const trendTbody = document.getElementById('monthlyDailyTrendTbody');
            if (sortedDates.length === 0) {{
                trendTbody.innerHTML = `<tr><td colspan="5" class="p-4 text-center text-slate-400">Koi tareekh-war hisab nahi hai.</td></tr>`;
            }} else {{
                trendTbody.innerHTML = sortedDates.map(dateKey => {{
                    const dItems = dayGroups[dateKey];
                    const dCost = dItems.reduce((sum, it) => sum + (it.total_amount || 0), 0);
                    const dSites = new Set(dItems.map(it => it.site_id)).size;
                    return `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-2.5 font-mono font-bold text-slate-800">${{dateKey}}</td>
                            <td class="p-2.5 text-center font-bold text-indigo-700">${{dSites}} sites</td>
                            <td class="p-2.5 text-right font-mono text-blue-600">${{dItems.length}} items</td>
                            <td class="p-2.5 text-right font-mono font-black text-emerald-700">₹${{dCost.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}</td>
                            <td class="p-2.5 text-center">
                                <button onclick="viewDateDailyReport('${{dateKey}}')" class="px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-semibold transition">
                                    Roj Ka Hisab &rarr;
                                </button>
                            </td>
                        </tr>
                    `;
                }}).join('');
            }}

            // Monthly Detailed Transactions Log
            document.getElementById('monthlyEntriesCountDisplay').textContent = `${{monthEntries.length}} records`;
            const txTbody = document.getElementById('monthlyTransactionsTbody');
            if (monthEntries.length === 0) {{
                txTbody.innerHTML = `<tr><td colspan="10" class="p-6 text-center text-slate-400">Is mahine (${{chosenMonth}}) me koi transaction record nahi mila.</td></tr>`;
            }} else {{
                txTbody.innerHTML = monthEntries.map((e, idx) => `
                    <tr class="hover:bg-slate-50 transition">
                        <td class="p-2.5 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                        <td class="p-2.5 font-mono font-bold text-slate-700 whitespace-nowrap">${{e.usage_date}}</td>
                        <td class="p-2.5">
                            <span class="font-bold text-slate-800 block">${{e.site_name || 'Site'}}</span>
                            <span class="text-[10px] text-slate-400 font-mono">${{e.site_code || ''}}</span>
                        </td>
                        <td class="p-2.5 font-bold text-slate-800">${{e.material_name}}</td>
                        <td class="p-2.5 text-right font-mono font-bold text-blue-600">${{e.quantity}}</td>
                        <td class="p-2.5 text-center font-mono text-slate-500">${{e.material_unit}}</td>
                        <td class="p-2.5 text-right font-mono text-slate-600">₹${{(e.rate || 0).toFixed(2)}}</td>
                        <td class="p-2.5 text-right font-mono font-bold text-emerald-600">₹${{(e.total_amount || 0).toFixed(2)}}</td>
                        <td class="p-2.5 text-slate-500 text-[11px]">
                            ${{e.purpose || '-'}}
                            ${{e.entered_by ? `<span class="text-[10px] text-slate-400 block">By: ${{e.entered_by}}</span>` : ''}}
                        </td>
                        <td class="p-2.5 text-center">
                            <div class="flex items-center justify-center gap-1.5">
                                <button onclick="openEditEntryModal(${{e.id}})" class="px-2 py-1 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 font-bold text-[11px] transition flex items-center gap-1" title="Edit Karein">
                                    <i class="fa-solid fa-pen-to-square"></i> Edit
                                </button>
                                <button onclick="deleteStandaloneEntry(${{e.id}})" class="px-2 py-1 rounded-lg bg-rose-50 text-rose-600 hover:bg-rose-100 font-bold text-[11px] transition flex items-center gap-1" title="Delete Karein">
                                    <i class="fa-solid fa-trash-can"></i> Hatao
                                </button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            }}
        }}

        function viewDateDailyReport(dateStr) {{
            const input = document.getElementById('dailyReportDateInput');
            if (input) input.value = dateStr;
            switchTab('daily-report');
        }}

        function shareMonthlyWhatsApp() {{
            const monthInput = document.getElementById('monthlyReportMonthInput');
            const chosenMonth = monthInput ? monthInput.value : todayStr.slice(0, 7);

            const monthEntries = appEntries.filter(e => (e.usage_date || '').startsWith(chosenMonth));
            const monthTotalCost = monthEntries.reduce((sum, e) => sum + (e.total_amount || 0), 0);

            // Active sites count & top sites
            const siteTotals = {{}};
            monthEntries.forEach(e => {{
                siteTotals[e.site_name || 'Site'] = (siteTotals[e.site_name || 'Site'] || 0) + (e.total_amount || 0);
            }});
            const sortedSites = Object.entries(siteTotals).sort((a, b) => b[1] - a[1]);

            let text = `*M/S SANDIP KUMAR - MONTHLY MATERIAL EXPENSE REPORT*\\n` +
                `📅 *Mahina:* ${{chosenMonth}}\\n` +
                `💰 *Kul Mahine Ka Kharch:* ₹${{monthTotalCost.toLocaleString('en-IN', {{minimumFractionDigits: 2}})}}\\n` +
                `🏗️ *Active Sites:* ${{sortedSites.length}} / 19 Sites\\n` +
                `📦 *Total Records:* ${{monthEntries.length}} Entries\\n\\n` +
                `*Top Sites Kharch:*\\n`;

            sortedSites.slice(0, 5).forEach(([sName, sCost]) => {{
                text += `• ${{sName}}: ₹${{Math.round(sCost).toLocaleString('en-IN')}}\\n`;
            }});

            text += `\\n_Generated via M/S Sandip Kumar Material Management System_`;

            const waUrl = `https://api.whatsapp.com/send?text=${{encodeURIComponent(text)}}`;
            window.open(waUrl, '_blank');
        }}

        function exportMonthlyCSV() {{
            const monthInput = document.getElementById('monthlyReportMonthInput');
            const chosenMonth = monthInput ? monthInput.value : todayStr.slice(0, 7);
            const monthEntries = appEntries.filter(e => (e.usage_date || '').startsWith(chosenMonth));

            let csv = "ID,Site Code,Site Name,Date,Material Name,Unit,Quantity,Rate,Total Amount,Purpose,Entered By\\n";
            monthEntries.forEach(e => {{
                const line = [
                    e.id,
                    `"${{(e.site_code || '').replace(/"/g, '""')}}"`,
                    `"${{(e.site_name || '').replace(/"/g, '""')}}"`,
                    e.usage_date,
                    `"${{(e.material_name || '').replace(/"/g, '""')}}"`,
                    e.material_unit,
                    e.quantity,
                    e.rate,
                    e.total_amount,
                    `"${{(e.purpose || '').replace(/"/g, '""')}}"`,
                    `"${{(e.entered_by || '').replace(/"/g, '""')}}"`
                ].join(',');
                csv += line + "\\n";
            }});

            const blob = new Blob(["\\ufeff" + csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `Sandip_Kumar_Monthly_Report_${{chosenMonth}}.csv`;
            link.click();
        }}

        // --- TAB 5: 271 MATERIALS CATALOG ---
        function renderMaterialsCatalog() {{
            const tbody = document.getElementById('catalogTableBody');
            tbody.innerHTML = appMaterials.map((m, idx) => `
                <tr class="hover:bg-slate-50 transition catalog-row" data-name="${{m.name.toLowerCase()}}" data-cat="${{(m.category || '').toLowerCase()}}">
                    <td class="p-3 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                    <td class="p-2 text-center">
                        <div class="relative group/img inline-block cursor-pointer" onclick="openStandalonePhotoModal(${{m.id}})" title="Photo Badlein">
                            <img src="${{getMatImg(m)}}" id="catalog-img-${{m.id}}" class="w-10 h-10 rounded-lg object-cover mx-auto border border-slate-200" referrerpolicy="no-referrer" onerror="handleCardImgError(this, ${{m.id}})">
                            <div class="absolute inset-0 bg-black/40 rounded-lg flex items-center justify-center opacity-0 group-hover/img:opacity-100 transition text-white text-[10px]">
                                <i class="fa-solid fa-camera"></i>
                            </div>
                        </div>
                    </td>
                    <td class="p-3 font-bold text-slate-800">${{m.name}}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 text-[10px]">${{m.category || 'General'}}</span></td>
                    <td class="p-3 text-center font-mono font-bold text-slate-600">${{m.unit}}</td>
                    <td class="p-3 text-right font-mono font-bold text-emerald-600">₹${{m.rate.toFixed(2)}}</td>
                    <td class="p-3 text-center">
                        <button onclick="openStandalonePhotoModal(${{m.id}})" class="px-2.5 py-1 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-800 font-semibold text-[11px] transition flex items-center gap-1 mx-auto">
                            <i class="fa-solid fa-camera"></i> Photo
                        </button>
                    </td>
                </tr>
            `).join('');
        }}

        // Photo Modal JS Engine
        let currentPhotoMatId = null;
        let currentTempImg = '';

        function extractClientImgUrl(url) {{
            if (!url) return '';
            url = url.trim();
            if (url.includes('google.') || url.includes('googleadservices.')) {{
                try {{
                    const u = new URL(url);
                    const imgurl = u.searchParams.get('imgurl');
                    if (imgurl) return decodeURIComponent(imgurl);
                    const adurl = u.searchParams.get('adurl');
                    if (adurl) return decodeURIComponent(adurl);
                    const destUrl = u.searchParams.get('url');
                    if (destUrl) return decodeURIComponent(destUrl);
                    const q = u.searchParams.get('q');
                    if (q && q.startsWith('http')) return decodeURIComponent(q);
                }} catch(e) {{}}
            }}
            return url;
        }}

        function openStandalonePhotoModal(matId) {{
            currentPhotoMatId = matId;
            const m = materialMap[matId];
            if (!m) return;

            document.getElementById('photoModalMatName').textContent = m.name;
            document.getElementById('photoModalCategory').textContent = `Category: ${{m.category || 'General'}} | Rate: ₹${{m.rate}}/${{m.unit}}`;

            const curImg = getMatImg(m);
            currentTempImg = curImg;
            document.getElementById('modalPreviewImg').src = curImg;
            document.getElementById('modalUrlInput').value = '';
            document.getElementById('modalFileInput').value = '';
            const notice = document.getElementById('photoStatusNotice');
            if (notice) notice.innerHTML = '';

            // Generate smart suggested stock photos for this specific material
            const suggestContainer = document.getElementById('modalSmartSuggested');
            if (suggestContainer) {{
                const lower = (m.name || '').toLowerCase();
                const catLower = (m.category || '').toLowerCase();
                let pills = [];
                if (catLower.includes('pipe') || lower.includes('pipe')) {{
                    pills.push({{ name: 'UPVC / PVC Pipe (White)', key: 'upvc_pipe.jpg', icon: 'fa-lines-leaning', color: 'text-blue-500' }});
                    pills.push({{ name: 'HDPE Pipe (Black)', key: 'hdpe_pipe.jpg', icon: 'fa-lines-leaning', color: 'text-slate-800' }});
                }} else if (catLower.includes('motor') || lower.includes('motor') || lower.includes('pump')) {{
                    pills.push({{ name: 'Submersible Motor', key: 'submersible_motor.jpg', icon: 'fa-water-ladder', color: 'text-emerald-600' }});
                    pills.push({{ name: 'Starter Panel', key: 'starter_panel.jpg', icon: 'fa-bolt', color: 'text-amber-600' }});
                }} else if (lower.includes('starter') || lower.includes('panel')) {{
                    pills.push({{ name: 'Starter Panel', key: 'starter_panel.jpg', icon: 'fa-bolt', color: 'text-amber-600' }});
                }} else if (lower.includes('gate valve') || lower.includes('brass')) {{
                    pills.push({{ name: 'Brass Gate Valve', key: 'brass_gate_valve.jpg', icon: 'fa-faucet-drip', color: 'text-rose-600' }});
                }} else if (lower.includes('ball valve')) {{
                    pills.push({{ name: 'UPVC Ball Valve', key: 'upvc_ball_valve.jpg', icon: 'fa-circle-dot', color: 'text-indigo-600' }});
                }} else if (catLower.includes('tank') || lower.includes('tank') || lower.includes('sintex')) {{
                    pills.push({{ name: 'Sintex Water Tank', key: 'sintex_water_tank.jpg', icon: 'fa-oil-well', color: 'text-cyan-600' }});
                }} else if (catLower.includes('cable') || lower.includes('cable') || lower.includes('wire')) {{
                    pills.push({{ name: 'Submersible Cable Wire', key: 'cable.jpg', icon: 'fa-plug', color: 'text-purple-600' }});
                }} else if (lower.includes('tap') || lower.includes('nal')) {{
                    pills.push({{ name: 'Water Tap (Nal)', key: 'water_tap.jpg', icon: 'fa-faucet', color: 'text-sky-600' }});
                }} else if (lower.includes('teflon')) {{
                    pills.push({{ name: 'Teflon Tape', key: 'teflon_tape.jpg', icon: 'fa-tape', color: 'text-rose-500' }});
                }} else if (lower.includes('solvent') || catLower.includes('consumable')) {{
                    pills.push({{ name: 'Solvent Cement', key: 'hardware_consumables.jpg', icon: 'fa-flask', color: 'text-amber-700' }});
                }} else if (lower.includes('union') || lower.includes('socket') || lower.includes('elbow') || catLower.includes('fitting')) {{
                    pills.push({{ name: 'Plumbing Fittings', key: 'fittings.jpg', icon: 'fa-wrench', color: 'text-slate-600' }});
                    pills.push({{ name: 'Union / Jointer', key: 'mat_160_7ba622.jpg', icon: 'fa-link', color: 'text-teal-600' }});
                }} else {{
                    pills.push({{ name: 'Fittings & Accessories', key: 'fittings.jpg', icon: 'fa-wrench', color: 'text-slate-600' }});
                }}

                suggestContainer.innerHTML = `
                    <div class="p-3 rounded-2xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200/80 space-y-2">
                        <div class="text-[11px] font-black uppercase text-blue-900 tracking-wider flex items-center justify-between">
                            <span>⚡ Is Material Ke Liye Best Photos (1-Click Me Lagayein):</span>
                            <span class="text-[10px] text-blue-600 font-bold bg-blue-100 px-2 py-0.5 rounded-full">Sabse Fast</span>
                        </div>
                        <div class="flex flex-wrap gap-2">
                            ${{pills.map(p => `
                                <button type="button" onclick="setPresetPhoto('${{p.key}}')" class="px-3 py-2 rounded-xl bg-white hover:bg-blue-600 hover:text-white text-slate-800 text-xs font-bold border border-slate-200 shadow-sm transition flex items-center gap-2 group">
                                    <i class="fa-solid ${{p.icon}} ${{p.color}} group-hover:text-white text-sm"></i>
                                    <span>${{p.name}}</span>
                                    <span class="text-[10px] bg-slate-100 group-hover:bg-blue-500 group-hover:text-white text-slate-500 px-1.5 py-0.5 rounded font-mono font-bold">1-Click</span>
                                </button>
                            `).join('')}}
                        </div>
                    </div>
                `;
            }}

            const googleUrl = `https://www.google.com/search?tbm=isch&q=${{encodeURIComponent(m.name + ' plumbing construction water supply')}}`;
            const gBtn = document.getElementById('googleSearchBtn');
            if (gBtn) gBtn.href = googleUrl;

            document.getElementById('photoModal').classList.remove('hidden');
        }}

        function closePhotoModal() {{
            document.getElementById('photoModal').classList.add('hidden');
            currentPhotoMatId = null;
            currentTempImg = '';
        }}

        // Client-side Canvas Image Compression: Compresses camera/phone photos to max 400x400 JPEG (approx 20 KB)
        function onModalFileSelected(input) {{
            if (input.files && input.files[0]) {{
                const file = input.files[0];
                const reader = new FileReader();
                reader.onload = function(e) {{
                    const tempImg = new Image();
                    tempImg.onload = function() {{
                        const maxDim = 400;
                        let w = tempImg.width;
                        let h = tempImg.height;
                        if (w > maxDim || h > maxDim) {{
                            if (w > h) {{ h = Math.round((h * maxDim) / w); w = maxDim; }}
                            else {{ w = Math.round((w * maxDim) / h); h = maxDim; }}
                        }}
                        const canvas = document.createElement('canvas');
                        canvas.width = w;
                        canvas.height = h;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(tempImg, 0, 0, w, h);
                        const compressedB64 = canvas.toDataURL('image/jpeg', 0.82);
                        currentTempImg = compressedB64;
                        document.getElementById('modalPreviewImg').src = compressedB64;
                        document.getElementById('modalUrlInput').value = '';
                        const notice = document.getElementById('photoStatusNotice');
                        if (notice) notice.innerHTML = '<span class="text-emerald-600 font-bold">✅ Photo device se select ho gayi (Ready)!</span>';
                    }};
                    tempImg.src = e.target.result;
                }};
                reader.readAsDataURL(file);
            }}
        }}

        function onModalUrlInput(val) {{
            const notice = document.getElementById('photoStatusNotice');
            if (!val || !val.trim()) {{
                if (notice) notice.innerHTML = '';
                return;
            }}
            const cleanUrl = extractClientImgUrl(val);
            if (cleanUrl) {{
                testAndSetPreview(cleanUrl);
            }}
        }}

        async function testAndSetPreview(url) {{
            const previewImg = document.getElementById('modalPreviewImg');
            const notice = document.getElementById('photoStatusNotice');
            if (notice) notice.innerHTML = '<span class="text-blue-600 font-bold"><i class="fa-solid fa-spinner fa-spin"></i> Online photo extract ho rahi hai...</span>';

            // 1. Try local Python smart resolver (can extract real photos from Google Ads, IndiaMART, Flipkart, webpages!)
            try {{
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 4500);
                const res = await fetch('http://127.0.0.1:5000/api/resolve_photo_url', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ url: url, material_id: currentPhotoMatId }}),
                    signal: controller.signal
                }});
                clearTimeout(timeoutId);
                const data = await res.json();
                if (data.success && data.b64) {{
                    currentTempImg = data.b64;
                    previewImg.src = data.b64;
                    if (notice) notice.innerHTML = '<span class="text-emerald-600 font-bold">✅ Google/Online Photo safalta se extract ho gayi! "Photo Save Karein" dabayein.</span>';
                    return;
                }}
            }} catch(err) {{
                // Fallback to direct client image loading
            }}

            // 2. Direct browser image loading fallback (e.g. for .jpg, .png, gstatic)
            const testImg = new Image();
            testImg.referrerPolicy = "no-referrer";
            testImg.onload = function() {{
                currentTempImg = url;
                previewImg.src = url;
                if (notice) notice.innerHTML = '<span class="text-emerald-600 font-bold">✅ Photo Preview Ready! "Photo Save Karein" dabayein.</span>';
            }};
            testImg.onerror = function() {{
                if (notice) notice.innerHTML = `
                    <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-[11px] space-y-1">
                        <div class="font-bold flex items-center gap-1 text-amber-800">
                            <i class="fa-solid fa-circle-exclamation text-amber-600"></i> Yeh link photo ka nahi hai (Google Ad ya Webpage ka link hai)
                        </div>
                        <div>
                            👉 <strong>Sabse Aasan:</strong> Upar <strong>Best Photos</strong> ya <strong>Stock Photo</strong> me se 1-click me photo chunein, ya phone/computer se upload karein.
                        </div>
                    </div>
                `;
            }};
            testImg.src = url;
        }}

        function applyModalUrlPreview() {{
            const val = document.getElementById('modalUrlInput').value.trim();
            const cleanUrl = extractClientImgUrl(val);
            if (cleanUrl) {{
                document.getElementById('modalUrlInput').value = cleanUrl;
                testAndSetPreview(cleanUrl);
            }}
        }}

        function setPresetPhoto(key) {{
            if (B64_IMAGES[key]) {{
                currentTempImg = B64_IMAGES[key];
                document.getElementById('modalPreviewImg').src = currentTempImg;
                document.getElementById('modalUrlInput').value = '';
                const notice = document.getElementById('photoStatusNotice');
                if (notice) notice.innerHTML = '<span class="text-emerald-600 font-bold">✅ Stock photo select ho gayi! "Photo Save Karein" dabayein.</span>';
            }}
        }}

        function compressDataUrl(srcDataUrl, maxDim = 320, quality = 0.78) {{
            return new Promise((resolve) => {{
                if (!srcDataUrl || !srcDataUrl.startsWith('data:image/')) {{
                    resolve(srcDataUrl);
                    return;
                }}
                const img = new Image();
                img.onload = function() {{
                    let w = img.width;
                    let h = img.height;
                    if (w <= maxDim && h <= maxDim && srcDataUrl.length < 40000) {{
                        resolve(srcDataUrl);
                        return;
                    }}
                    if (w > maxDim || h > maxDim) {{
                        if (w > h) {{ h = Math.round((h * maxDim) / w); w = maxDim; }}
                        else {{ w = Math.round((w * maxDim) / h); h = maxDim; }}
                    }}
                    const canvas = document.createElement('canvas');
                    canvas.width = w;
                    canvas.height = h;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, w, h);
                    resolve(canvas.toDataURL('image/jpeg', quality));
                }};
                img.onerror = function() {{
                    resolve(srcDataUrl);
                }};
                img.src = srcDataUrl;
            }});
        }}

        async function resetMaterialPhoto() {{
            if (!currentPhotoMatId) return;
            delete customImages[currentPhotoMatId];
            try {{
                localStorage.setItem('sandip_custom_images', JSON.stringify(customImages));
            }} catch(e) {{}}
            await idbRemovePhoto(currentPhotoMatId);

            const m = materialMap[currentPhotoMatId];
            const defImg = getStockFallbackImg(m);
            if (m) m.image_url = defImg;

            const cardImg = document.getElementById(`card-img-${{currentPhotoMatId}}`);
            if (cardImg) {{
                cardImg.src = defImg;
                cardImg.onerror = function() {{ handleCardImgError(this, currentPhotoMatId); }};
            }}

            const catImg = document.getElementById(`catalog-img-${{currentPhotoMatId}}`);
            if (catImg) {{
                catImg.src = defImg;
                catImg.onerror = function() {{ handleCardImgError(this, currentPhotoMatId); }};
            }}

            if (cart[currentPhotoMatId]) {{
                cart[currentPhotoMatId].img = defImg;
                updateCartUI();
            }}

            // Sync reset to backend if running
            fetch(`http://127.0.0.1:5000/api/materials/${{currentPhotoMatId}}/photo`, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ image_url: '/uploads/materials/fittings.jpg' }})
            }}).catch(() => {{}});

            alert("✅ Default photo safalta se wapas lag gayi!");
            closePhotoModal();
        }}

        async function saveCustomPhoto() {{
            if (!currentPhotoMatId || !currentTempImg) {{
                alert("Kripya pehle photo select karein ya link dalein!");
                return;
            }}

            const saveBtn = document.getElementById('savePhotoBtn') || document.querySelector('#photoModal button[onclick="saveCustomPhoto()"]');
            const originalBtnHtml = saveBtn ? saveBtn.innerHTML : '';
            if (saveBtn) {{
                saveBtn.disabled = true;
                saveBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
            }}

            try {{
                let finalImg = currentTempImg;

                // 1. If remote URL, try converting to Base64 via canvas for 100% offline support
                if (finalImg.startsWith('http://') || finalImg.startsWith('https://')) {{
                    try {{
                        const previewImg = document.getElementById('modalPreviewImg');
                        if (previewImg && previewImg.naturalWidth > 0) {{
                            const maxDim = 320;
                            let w = previewImg.naturalWidth;
                            let h = previewImg.naturalHeight;
                            if (w > maxDim || h > maxDim) {{
                                if (w > h) {{ h = Math.round((h * maxDim) / w); w = maxDim; }}
                                else {{ w = Math.round((w * maxDim) / h); h = maxDim; }}
                            }}
                            const canvas = document.createElement('canvas');
                            canvas.width = w;
                            canvas.height = h;
                            const ctx = canvas.getContext('2d');
                            ctx.drawImage(previewImg, 0, 0, w, h);
                            finalImg = canvas.toDataURL('image/jpeg', 0.78);
                        }}
                    }} catch(corsErr) {{
                        // Cross-origin canvas export blocked, keeping direct URL
                    }}
                }}

                // 2. Compress data URL to lightweight thumbnail (~15-25KB)
                if (finalImg.startsWith('data:image/')) {{
                    finalImg = await compressDataUrl(finalImg, 320, 0.78);
                }}

                // 3. Save to In-Memory
                customImages[currentPhotoMatId] = finalImg;
                const m = materialMap[currentPhotoMatId];
                if (m) m.image_url = finalImg;

                // 4. Save to IndexedDB (Permanent browser database, virtually unlimited storage)
                await idbSavePhoto(currentPhotoMatId, finalImg);

                // 5. Save to LocalStorage (Immediate backup)
                try {{
                    localStorage.setItem('sandip_custom_images', JSON.stringify(customImages));
                }} catch(quotaErr) {{
                    console.warn('LocalStorage quota warning (safe in IndexedDB):', quotaErr);
                }}

                // 6. Update UI on page immediately
                const cardImg = document.getElementById(`card-img-${{currentPhotoMatId}}`);
                if (cardImg) {{
                    cardImg.src = finalImg;
                    cardImg.onerror = function() {{ handleCardImgError(this, currentPhotoMatId); }};
                }}

                const catImg = document.getElementById(`catalog-img-${{currentPhotoMatId}}`);
                if (catImg) {{
                    catImg.src = finalImg;
                    catImg.onerror = function() {{ handleCardImgError(this, currentPhotoMatId); }};
                }}

                if (cart[currentPhotoMatId]) {{
                    cart[currentPhotoMatId].img = finalImg;
                    updateCartUI();
                }}

                // 7. Auto-sync with local Python server (if running) to bake into Desktop HTML & SQLite
                fetch(`http://127.0.0.1:5000/api/materials/${{currentPhotoMatId}}/photo`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ image_url: finalImg }})
                }}).then(res => res.json()).then(data => {{
                    console.log('✅ Background synced to Python backend and Desktop HTML regenerated:', data);
                }}).catch(() => {{
                    // Purely offline standalone mode, already preserved in IndexedDB & LocalStorage
                }});

                alert("✅ Photo safalta se set aur permanently save ho gayi! Dubara kholne par bhi hamesha rahegi.");
                closePhotoModal();
            }} catch(err) {{
                alert("Photo save error: " + (err.message || err));
            }} finally {{
                if (saveBtn) {{
                    saveBtn.disabled = false;
                    saveBtn.innerHTML = originalBtnHtml || '<i class="fa-solid fa-check"></i> Photo Save Karein';
                }}
            }}
        }}

        function filterCatalog() {{
            const query = (document.getElementById('catalogSearchInput').value || '').toLowerCase().trim();
            const rows = document.querySelectorAll('.catalog-row');
            rows.forEach(r => {{
                const name = r.dataset.name;
                const cat = r.dataset.cat;
                if (!query || name.includes(query) || cat.includes(query)) r.style.display = '';
                else r.style.display = 'none';
            }});
        }}

        // --- TAB 6: NEW ENTRY (OFFLINE LOCAL STORAGE) ---
        let entryRowIdx = 0;

        function initNewEntryTab() {{
            const select = document.getElementById('newEntrySite');
            select.innerHTML = `<option value="">-- Site Chunein (1 to 19) --</option>` + appSites.map(s => `
                <option value="${{s.id}}" data-supervisor="${{s.supervisor || ''}}">${{s.code}} - ${{s.name}}</option>
            `).join('');
            document.getElementById('newEntryDate').value = todayStr;

            // Populate Datalist
            const dl = document.getElementById('allMaterialsDatalist');
            dl.innerHTML = appMaterials.map(m => `
                <option value="${{m.name}}" data-id="${{m.id}}" data-rate="${{m.rate}}" data-unit="${{m.unit}}">₹${{m.rate}} / ${{m.unit}} (${{m.category}})</option>
            `).join('');

            addNewEntryRow();
            renderRecentEntriesList();
        }}

        function onNewEntrySiteChange() {{
            const select = document.getElementById('newEntrySite');
            const opt = select.options[select.selectedIndex];
            document.getElementById('newEntrySupervisor').value = opt ? (opt.dataset.supervisor || '') : '';
        }}

        function addNewEntryRow() {{
            entryRowIdx++;
            const tbody = document.getElementById('newEntryTableBody');
            const tr = document.createElement('tr');
            tr.id = `entry-row-${{entryRowIdx}}`;
            tr.className = "hover:bg-slate-50 transition";
            tr.innerHTML = `
                <td class="p-2.5 text-center text-slate-400 font-mono row-num"></td>
                <td class="p-2.5">
                    <input type="text" list="allMaterialsDatalist" placeholder="Material search karein..." oninput="onEntryMatInput(this)" class="mat-input w-full rounded-lg border border-slate-300 py-1.5 px-2.5 text-xs font-semibold text-slate-800">
                    <input type="hidden" class="mat-id-input" value="">
                </td>
                <td class="p-2.5 text-center">
                    <span class="unit-span px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-mono text-[11px]">-</span>
                </td>
                <td class="p-2.5 text-right">
                    <input type="number" step="any" min="0" placeholder="Qty" oninput="recalcEntryTotal()" class="qty-input w-full text-right rounded-lg border border-slate-300 py-1.5 px-2 text-xs font-bold text-slate-800">
                </td>
                <td class="p-2.5 text-right">
                    <input type="number" step="any" min="0" placeholder="Rate" oninput="recalcEntryTotal()" class="rate-input w-full text-right rounded-lg border border-slate-300 py-1.5 px-2 text-xs font-mono text-slate-700">
                </td>
                <td class="p-2.5 text-right font-mono font-bold text-emerald-600 row-amount">₹0.00</td>
                <td class="p-2.5 text-center">
                    <button type="button" onclick="this.closest('tr').remove(); recalcEntryTotal();" class="text-rose-500 hover:text-rose-700 p-1">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
            recalcEntryTotal();
        }}

        function onEntryMatInput(input) {{
            const val = input.value.trim().toLowerCase();
            const row = input.closest('tr');
            const matIdInput = row.querySelector('.mat-id-input');
            const unitSpan = row.querySelector('.unit-span');
            const rateInput = row.querySelector('.rate-input');

            const matched = appMaterials.find(m => m.name.toLowerCase() === val);
            if (matched) {{
                matIdInput.value = matched.id;
                unitSpan.textContent = matched.unit;
                rateInput.value = matched.rate;
            }} else {{
                matIdInput.value = "";
                unitSpan.textContent = "-";
            }}
            recalcEntryTotal();
        }}

        function recalcEntryTotal() {{
            const rows = document.querySelectorAll('#newEntryTableBody tr');
            let grand = 0;
            rows.forEach((row, idx) => {{
                const num = row.querySelector('.row-num');
                if (num) num.textContent = idx + 1;

                const qty = parseFloat(row.querySelector('.qty-input')?.value) || 0;
                const rate = parseFloat(row.querySelector('.rate-input')?.value) || 0;
                const amt = qty * rate;
                grand += amt;

                const amtSpan = row.querySelector('.row-amount');
                if (amtSpan) amtSpan.textContent = `₹${{amt.toFixed(2)}}`;
            }});
            document.getElementById('newEntryGrandTotal').textContent = `₹${{grand.toLocaleString('en-IN', {{minimumFractionDigits: 2, maximumFractionDigits: 2}})}}`;
        }}

        function saveNewEntryRecord() {{
            const siteId = document.getElementById('newEntrySite').value;
            const date = document.getElementById('newEntryDate').value;
            const purpose = document.getElementById('newEntryPurpose').value.trim();
            const enteredBy = document.getElementById('newEntryEnteredBy').value.trim();

            if (!siteId) {{ alert("Kripya Site chunein!"); return; }}
            if (!date) {{ alert("Kripya Date chunein!"); return; }}

            const rows = document.querySelectorAll('#newEntryTableBody tr');
            const toAdd = [];

            rows.forEach(row => {{
                const name = row.querySelector('.mat-input').value.trim();
                const matId = row.querySelector('.mat-id-input').value;
                const qty = parseFloat(row.querySelector('.qty-input').value) || 0;
                const rate = parseFloat(row.querySelector('.rate-input').value) || 0;
                const unit = row.querySelector('.unit-span').textContent;

                if (name && qty > 0) {{
                    const matObj = materialMap[matId] || {{ name: name }};
                    toAdd.push({{
                        id: Date.now() + Math.floor(Math.random() * 1000),
                        site_id: parseInt(siteId),
                        material_id: matId ? parseInt(matId) : null,
                        quantity: qty,
                        rate: rate,
                        total_amount: qty * rate,
                        usage_date: date,
                        purpose: purpose,
                        entered_by: enteredBy,
                        remarks: "Manual entry",
                        site_name: siteMap[siteId] ? siteMap[siteId].name : "Site",
                        site_code: siteMap[siteId] ? siteMap[siteId].code : "",
                        site_supervisor: siteMap[siteId] ? siteMap[siteId].supervisor : "",
                        material_name: name,
                        material_unit: unit !== '-' ? unit : 'NOS',
                        material_image: getMatImg(matObj)
                    }});
                }}
            }});

            if (toAdd.length === 0) {{
                alert("Kam se kam ek valid material aur quantity dalein!");
                return;
            }}

            toAdd.forEach(item => appEntries.unshift(item));
            localStorage.setItem('sandip_entries', JSON.stringify(appEntries));

            // Background sync with server if running
            try {{
                toAdd.forEach(item => {{
                    fetch('/api/entries', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(item)
                    }}).catch(() => {{}});
                }});
            }} catch (e) {{}}

            alert(`✅ Safalta se save ho gaya!\n${{toAdd.length}} items darj ho gaye.`);

            // Reset form
            document.getElementById('newEntryTableBody').innerHTML = '';
            addNewEntryRow();
            renderRecentEntriesList();

            // Redirect to Site Report
            document.getElementById('reportSiteSelect').value = siteId;
            switchTab('site-report');
        }}

        // --- RECENT ENTRIES LIST (TAB 6) ---
        function renderRecentEntriesList() {{
            const tbody = document.getElementById('recentEntriesTableBody');
            if (!tbody) return;
            const recent = appEntries.slice(0, 30);
            if (recent.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="8" class="p-6 text-center text-slate-400">Abhi tak koi entry darj nahi hui hai. Upar form bharkar 'Save Karein' dabayein!</td></tr>`;
                return;
            }}
            tbody.innerHTML = recent.map((e, idx) => `
                <tr class="hover:bg-slate-50 transition">
                    <td class="p-2.5 text-center text-slate-400 font-mono">${{idx + 1}}</td>
                    <td class="p-2.5 font-mono font-bold text-slate-700 whitespace-nowrap">${{e.usage_date}}</td>
                    <td class="p-2.5">
                        <span class="font-bold text-slate-800 block">${{e.site_name || (siteMap[e.site_id] ? siteMap[e.site_id].name : 'Site')}}</span>
                        <span class="text-[10px] text-slate-400 font-mono">${{e.site_code || ''}}</span>
                    </td>
                    <td class="p-2.5 font-bold text-slate-800">${{e.material_name}}</td>
                    <td class="p-2.5 text-right font-mono font-bold text-blue-600">${{e.quantity}}</td>
                    <td class="p-2.5 text-center font-mono text-slate-500">${{e.material_unit}}</td>
                    <td class="p-2.5 text-right font-mono font-bold text-emerald-600">₹${{(e.total_amount || 0).toFixed(2)}}</td>
                    <td class="p-2.5 text-center">
                        <div class="flex items-center justify-center gap-1.5">
                            <button onclick="openEditEntryModal(${{e.id}})" class="px-2 py-1 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-100 font-bold text-[11px] transition flex items-center gap-1" title="Edit Karein">
                                <i class="fa-solid fa-pen-to-square"></i> Edit
                            </button>
                            <button onclick="deleteStandaloneEntry(${{e.id}})" class="px-2 py-1 rounded-lg bg-rose-50 text-rose-600 hover:bg-rose-100 font-bold text-[11px] transition flex items-center gap-1" title="Delete Karein">
                                <i class="fa-solid fa-trash-can"></i> Hatao
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        }}

        // --- BACKUP DOWNLOAD & RESTORE ---
        function downloadEntriesBackup() {{
            const backupData = {{
                app_version: "2.0",
                app_name: "M/S SANDIP KUMAR MATERIAL TRACKER",
                backup_date: new Date().toISOString(),
                total_entries: appEntries.length,
                entries: appEntries,
                sites: appSites,
                custom_photos: (function() {{
                    try {{ return JSON.parse(localStorage.getItem('sandip_custom_photos') || '{{}}'); }}
                    catch(e) {{ return {{}}; }}
                }})()
            }};

            const jsonStr = JSON.stringify(backupData, null, 2);
            const blob = new Blob([jsonStr], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `SANDIP_KUMAR_BACKUP_${{todayStr}}.json`;
            link.click();
            URL.revokeObjectURL(url);
        }}

        function openRestoreModal() {{
            document.getElementById('restoreBackupModal').classList.remove('hidden');
        }}

        function closeRestoreModal() {{
            document.getElementById('restoreBackupModal').classList.add('hidden');
        }}

        function handleBackupFileRestore(input) {{
            const file = input.files && input.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(evt) {{
                try {{
                    const data = JSON.parse(evt.target.result);
                    if (!data.entries && !Array.isArray(data)) {{
                        alert("Galat backup file format! Kripya valid backup JSON file chunein.");
                        return;
                    }}

                    const newEntries = Array.isArray(data) ? data : (data.entries || []);

                    // Save undo before restoring
                    localStorage.setItem('sandip_entries_undo_backup', JSON.stringify(appEntries));

                    // Restore entries
                    appEntries = newEntries;
                    localStorage.setItem('sandip_entries', JSON.stringify(appEntries));

                    // Restore custom photos if present
                    if (data.custom_photos && typeof data.custom_photos === 'object') {{
                        const existingPhotos = JSON.parse(localStorage.getItem('sandip_custom_photos') || '{{}}');
                        const mergedPhotos = Object.assign({{}}, existingPhotos, data.custom_photos);
                        localStorage.setItem('sandip_custom_photos', JSON.stringify(mergedPhotos));
                    }}

                    // Sync with server if server is running
                    try {{
                        fetch('/api/restore', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ entries: appEntries }})
                        }}).catch(() => {{}});
                    }} catch (e) {{}}

                    closeRestoreModal();
                    renderSiteReport();
                    renderDailyReport();
                    renderRecentEntriesList();
                    renderProducts();
                    alert(`✅ Backup Safalta Se Restore Ho Gaya!\nKul ${{appEntries.length}} entries load ho gayi hain.`);
                }} catch (err) {{
                    alert("File read karne me error aayi: " + err.message);
                }}
            }};
            reader.readAsText(file);
        }}

        function undoLastDelete() {{
            const undoData = localStorage.getItem('sandip_entries_undo_backup');
            if (!undoData) {{
                alert("Koi recent deleted entry backup nahi mila!");
                return;
            }}
            try {{
                appEntries = JSON.parse(undoData);
                localStorage.setItem('sandip_entries', JSON.stringify(appEntries));
                renderSiteReport();
                renderDailyReport();
                renderRecentEntriesList();
                closeRestoreModal();
                alert("✅ Aakhiri delete safalta se undo (wapas restore) ho gaya!");
            }} catch (e) {{
                alert("Undo karne me problem aayi: " + e.message);
            }}
        }}

        // --- EDIT ENTRY MODAL FUNCTIONS ---
        function openEditEntryModal(entryId) {{
            const entry = appEntries.find(e => e.id == entryId);
            if (!entry) {{
                alert("Entry nahi mili!");
                return;
            }}

            const select = document.getElementById('editEntrySiteSelect');
            select.innerHTML = appSites.map(s => `
                <option value="${{s.id}}" ${{s.id == entry.site_id ? 'selected' : ''}}>${{s.code}} - ${{s.name}}</option>
            `).join('');

            document.getElementById('editEntryId').value = entry.id;
            document.getElementById('editEntryMaterialName').textContent = entry.material_name;
            document.getElementById('editEntryUnit').textContent = entry.material_unit || 'NOS';
            document.getElementById('editEntryDate').value = entry.usage_date;
            document.getElementById('editEntryQty').value = entry.quantity;
            document.getElementById('editEntryRate').value = entry.rate;
            document.getElementById('editEntryPurpose').value = entry.purpose || '';
            document.getElementById('editEntryEnteredBy').value = entry.entered_by || '';
            document.getElementById('editEntryRemarks').value = entry.remarks || '';

            updateEditEntryTotal();
            document.getElementById('editEntryModal').classList.remove('hidden');
        }}

        function closeEditEntryModal() {{
            document.getElementById('editEntryModal').classList.add('hidden');
        }}

        function updateEditEntryTotal() {{
            const qty = parseFloat(document.getElementById('editEntryQty').value) || 0;
            const rate = parseFloat(document.getElementById('editEntryRate').value) || 0;
            const total = qty * rate;
            document.getElementById('editEntryTotalDisplay').textContent = `₹${{total.toFixed(2)}}`;
        }}

        function saveEditedEntry() {{
            const id = document.getElementById('editEntryId').value;
            const siteId = parseInt(document.getElementById('editEntrySiteSelect').value);
            const date = document.getElementById('editEntryDate').value;
            const qty = parseFloat(document.getElementById('editEntryQty').value) || 0;
            const rate = parseFloat(document.getElementById('editEntryRate').value) || 0;
            const purpose = document.getElementById('editEntryPurpose').value.trim();
            const enteredBy = document.getElementById('editEntryEnteredBy').value.trim();
            const remarks = document.getElementById('editEntryRemarks').value.trim();

            if (!siteId) {{ alert("Site chunein!"); return; }}
            if (!date) {{ alert("Date chunein!"); return; }}
            if (qty <= 0) {{ alert("Valid quantity dalein!"); return; }}

            const idx = appEntries.findIndex(e => e.id == id);
            if (idx === -1) {{ alert("Entry nahi mili!"); return; }}

            const sObj = siteMap[siteId];
            const updated = Object.assign({{}}, appEntries[idx], {{
                site_id: siteId,
                site_name: sObj ? sObj.name : "Site",
                site_code: sObj ? sObj.code : "",
                site_supervisor: sObj ? sObj.supervisor : "",
                usage_date: date,
                quantity: qty,
                rate: rate,
                total_amount: qty * rate,
                purpose: purpose,
                entered_by: enteredBy,
                remarks: remarks
            }});

            appEntries[idx] = updated;
            localStorage.setItem('sandip_entries', JSON.stringify(appEntries));

            // Background sync with Flask server if running
            try {{
                fetch(`/api/entries/${{id}}`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        site_id: siteId,
                        quantity: qty,
                        rate: rate,
                        usage_date: date,
                        purpose: purpose,
                        remarks: remarks,
                        entered_by: enteredBy
                    }})
                }}).catch(() => {{}});
            }} catch (e) {{}}

            closeEditEntryModal();
            renderSiteReport();
            renderDailyReport();
            renderRecentEntriesList();
            alert("✅ Entry safalta se update ho gayi!");
        }}

        function deleteStandaloneEntry(entryId) {{
            const entry = appEntries.find(e => e.id == entryId);
            if (!entry) return;

            const pin = prompt("🚨 SURAKSHA CHECK (मालिक केवल):\n\nएंट्री केवल मालिक ही हटा सकते हैं।\nकृपया मालिक PIN डालें:");
            if (!pin || pin.trim() !== '7808') {{
                alert("❌ गलत पिन! केवल मालिक ही एंट्री डिलीट कर सकते हैं।");
                return;
            }}

            const confirmMsg = `Kya aap sach me is entry ko DELETE karna chahte hain?\\n\\n` +
                `• Tareekh: ${{entry.usage_date}}\\n` +
                `• Material: ${{entry.material_name}}\\n` +
                `• Qty: ${{entry.quantity}} ${{entry.material_unit}}\\n` +
                `• Site: ${{entry.site_name || 'Site'}}\\n` +
                `• Kul Bill: ₹${{(entry.total_amount || 0).toFixed(2)}}\\n\\n` +
                `Agar galti se delete ho jaye toh 'Backup Restore' se 'Undo' kiya ja sakta hai.`;

            if (!confirm(confirmMsg)) return;

            // Save undo snapshot
            localStorage.setItem('sandip_entries_undo_backup', JSON.stringify(appEntries));

            appEntries = appEntries.filter(e => e.id != entryId);
            localStorage.setItem('sandip_entries', JSON.stringify(appEntries));

            // Background sync with Flask server if running
            try {{
                fetch(`/api/entries/${{entryId}}`, {{ method: 'DELETE' }}).catch(() => {{}});
            }} catch (e) {{}}

            renderSiteReport();
            renderDailyReport();
            renderRecentEntriesList();
            alert("🗑️ Entry delete ho gayi! (Wapas lane ke liye 'Backup Restore' se Undo karein)");
        }}

        // Export All to CSV
        function exportAllCSV() {{
            let csv = "ID,Site Code,Site Name,Date,Material Name,Unit,Quantity,Rate,Total Amount,Purpose,Entered By\\n";
            appEntries.forEach(e => {{
                const line = [
                    e.id,
                    `"${{(e.site_code || '').replace(/"/g, '""')}}"`,
                    `"${{(e.site_name || '').replace(/"/g, '""')}}"`,
                    e.usage_date,
                    `"${{(e.material_name || '').replace(/"/g, '""')}}"`,
                    e.material_unit,
                    e.quantity,
                    e.rate,
                    e.total_amount,
                    `"${{(e.purpose || '').replace(/"/g, '""')}}"`,
                    `"${{(e.entered_by || '').replace(/"/g, '""')}}"`
                ].join(',');
                csv += line + "\\n";
            }});

            const blob = new Blob(["\\ufeff" + csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = `Sandip_Kumar_Material_Report_${{todayStr}}.csv`;
            link.click();
        }}

        function resetToFactoryData() {{
            if (confirm("Kya aap sach me sabhi test entries reset karke original data wapas lana chahte hain?")) {{
                localStorage.removeItem('sandip_entries');
                localStorage.removeItem('sandip_sites');
                localStorage.removeItem('sandip_materials');
                location.reload();
            }}
        }}

        // Bootstrap on DOM ready
        window.addEventListener('DOMContentLoaded', () => {{
            initStore();
            initNewEntryTab();
            initStandaloneManpower();
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
        }});
    </script>
</body>
</html>
"""

    # 4. Generate Files in Target Directories
    for d_path in dest_desktops:
        os.makedirs(d_path, exist_ok=True)
        folder_name = "M-S_SANDIP_KUMAR_MATERIAL_TRACKER"
        target_folder = os.path.join(d_path, folder_name)
        images_dest_folder = os.path.join(target_folder, "images")
        desktop_images_dest = os.path.join(d_path, "images")

        os.makedirs(images_dest_folder, exist_ok=True)
        os.makedirs(desktop_images_dest, exist_ok=True)

        # Copy original jpg images as well for backup
        if os.path.exists(uploads_materials_dir):
            for fname in os.listdir(uploads_materials_dir):
                src_file = os.path.join(uploads_materials_dir, fname)
                if os.path.isfile(src_file):
                    shutil.copy2(src_file, os.path.join(images_dest_folder, fname))
                    shutil.copy2(src_file, os.path.join(desktop_images_dest, fname))

        # Write index.html inside the folder
        index_path = os.path.join(target_folder, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Write README_INSTRUCTIONS.txt
        readme_path = os.path.join(target_folder, "README_INSTRUCTIONS.txt")
        readme_text = """============================================================
M/S SANDIP KUMAR - 19 SITES MATERIAL MANAGEMENT SYSTEM
============================================================

Yeh folder aur iske andar ki file ko aap kisi ko bhi bhej sakte hain:

1. KAISE CHALAYEIN (HOW TO USE):
   - 'index.html' par double-click karein ya Desktop par 'Site_Material_Tracker.html' par double-click karein.
   - Yeh aapke computer / mobile browser (Chrome, Edge, Firefox) me khul jayega.
   - Iske liye koi Python ya software install karne ki zaroorat NAHI hai.
   - Sabhi 271 materials ki photos is file ke andar hi 100% EMBEDDED hain, isliye photos hamesha dikhengi!

2. ISME KYA KYA HAI:
   - 🛒 Material Store: Sabhi 271 materials photos aur rates ke sath.
   - 🏗️ 19 Sites Directory: Sabhi 19 sites ke supervisors aur contact numbers.
   - 📊 Site-wise Report: Har site par kitna samaan laga, kab laga, total bill.
   - 📅 Roj Ka Hisab: Date-wise daily consumption report.
   - 📦 271 Materials Catalog: Saare products ki master list.
   - ✍️ + Naya Entry: Koi bhi nayi entry karein, wo browser me save ho jayegi.
   - 🖨️ Print / Save as PDF button & 📥 Export to Excel (CSV) button.

3. KISI KO BHEJNA HO TOH (HOW TO SHARE):
   - Tarika 1: Desktop par bane hue 'Site_Material_Tracker.html' file ko seedha WhatsApp ya Email par bhej dein. Yeh 1 single file akele hi poori photos ke sath khul jayegi!
   - Tarika 2: Desktop par 'M-S_SANDIP_KUMAR_MATERIAL_TRACKER.zip' file ko bhej dein.

============================================================
"""
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_text)

        # Place standalone HTML file directly on Desktop:
        direct_desktop_html = os.path.join(d_path, "Site_Material_Tracker.html")
        with open(direct_desktop_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Create ZIP file of the folder on Desktop for easy 1-click sharing
        zip_path = os.path.join(d_path, "M-S_SANDIP_KUMAR_MATERIAL_TRACKER.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(target_folder):
                for file in files:
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, target_folder)
                    zipf.write(full_p, arcname=os.path.join(folder_name, rel_p))

    return True

if __name__ == "__main__":
    build_standalone_package()
    print("Optimized standalone packaging completed successfully!")
