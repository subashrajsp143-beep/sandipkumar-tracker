# -*- coding: utf-8 -*-
"""
Setup script to configure PWA, Offline Service Worker, Cloud Sync, and Render deployment files.
"""
import os
import sys

def update_app_py():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_routes = '''
# ==========================================
# PWA & OFFLINE CLOUD SYNC ROUTES
# ==========================================
@app.route("/manifest.json")
def pwa_manifest():
    return send_from_directory("static", "manifest.json", mimetype="application/manifest+json")

@app.route("/sw.js")
def pwa_sw():
    response = send_from_directory("static", "sw.js", mimetype="application/javascript")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/api/sync/batch", methods=["POST", "OPTIONS"])
def sync_batch_entries():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})
    try:
        data = request.get_json() or {}
        entries = data.get("entries", [])
        saved_count = 0
        for e in entries:
            site_id = int(e.get("site_id"))
            items = e.get("items", [])
            usage_date = e.get("usage_date") or datetime.date.today().strftime("%Y-%m-%d")
            purpose = e.get("purpose", "")
            entered_by = e.get("entered_by", "")
            for item in items:
                mat_id = int(item["material_id"])
                qty = float(item["quantity"])
                rate = float(item.get("rate", 0))
                remarks = item.get("remarks", "")
                if qty > 0:
                    database.add_consumption_entry(
                        site_id=site_id,
                        material_id=mat_id,
                        usage_date=usage_date,
                        quantity=qty,
                        rate=rate,
                        purpose=purpose,
                        entered_by=entered_by,
                        remarks=remarks
                    )
                    saved_count += 1
        return jsonify({"success": True, "saved_count": saved_count, "message": f"{saved_count} offline entries synced!"})
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@app.route("/api/live-status", methods=["GET"])
def live_status():
    try:
        stats = database.get_dashboard_stats()
        return jsonify({
            "status": "online",
            "total_entries": stats.get("total_entries", 0),
            "total_cost": stats.get("total_cost", 0),
            "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as ex:
        return jsonify({"status": "online", "error": str(ex)})
'''

    if '@app.route("/manifest.json")' not in content:
        # insert right before if __name__ == '__main__':
        target = 'if __name__ == "__main__":'
        if target in content:
            content = content.replace(target, new_routes + '\n' + target)
        else:
            content += '\n' + new_routes

        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("app.py updated with PWA & Batch Sync routes!")
    else:
        print("app.py already contains PWA routes.")

def update_base_html():
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add PWA head tags
    pwa_head = '''    <!-- PWA Manifest & App Icons -->
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#0f172a">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Sandip Tracker">
    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">'''

    if '<link rel="manifest"' not in content:
        content = content.replace('</head>', pwa_head + '\n</head>', 1)

    # 2. Add Live Sync Status Pill & Install App Button in Header
    old_brand = '''                        <div>
                            <span class="font-bold text-lg tracking-wide text-white block leading-tight">M/S SANDIP KUMAR</span>
                            <span class="text-xs text-blue-200 block font-medium">19 Sites Material Consumption System</span>
                        </div>
                    </a>
                </div>'''

    new_brand = '''                        <div>
                            <span class="font-bold text-lg tracking-wide text-white block leading-tight">M/S SANDIP KUMAR</span>
                            <div class="flex items-center gap-2">
                                <span class="text-xs text-blue-200 block font-medium">19 Sites Material Tracker</span>
                                <span id="networkBadge" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping inline-block"></span>
                                    <span id="networkText">Online (Live Sync)</span>
                                </span>
                            </div>
                        </div>
                    </a>
                </div>'''

    if old_brand in content:
        content = content.replace(old_brand, new_brand, 1)

    # 3. Add Mobile Install Banner & Floating Notification Toast right before </body>
    pwa_ui_and_script = '''
    <!-- Mobile Install App Bottom Banner -->
    <div id="pwaInstallBanner" class="hidden fixed bottom-4 left-4 right-4 max-w-md mx-auto bg-slate-900/95 backdrop-blur-md border-2 border-amber-400 text-white p-4 rounded-2xl shadow-2xl z-50 flex items-center justify-between gap-3 transition-all">
        <div class="flex items-center gap-3">
            <img src="/static/icons/icon-144.png" class="w-11 h-11 rounded-xl shadow-md border border-slate-700 flex-shrink-0" alt="App Icon">
            <div>
                <div class="font-bold text-sm text-amber-300 flex items-center gap-1.5">
                    <i class="fa-solid fa-mobile-screen-button"></i> M/S Sandip Kumar App
                </div>
                <div class="text-[11px] text-slate-300">Apne phone me app install karein (1-Click)</div>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <button id="pwaInstallBtn" class="px-3.5 py-2 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black text-xs shadow-lg transition">
                Install
            </button>
            <button onclick="dismissInstallBanner()" class="p-1.5 text-slate-400 hover:text-white text-xs">
                ✕
            </button>
        </div>
    </div>

    <!-- Floating Live Alert Toast (When another supervisor adds an entry) -->
    <div id="liveNewEntryToast" class="hidden fixed top-20 right-4 max-w-sm bg-slate-900/95 border border-emerald-400 text-white p-4 rounded-2xl shadow-2xl z-50 flex items-center gap-3 animate-bounce">
        <div class="w-9 h-9 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
            <i class="fa-solid fa-bell text-lg"></i>
        </div>
        <div class="text-xs">
            <div class="font-bold text-emerald-300">Nayi Entry Aayi Hai!</div>
            <div id="liveNewEntryText" class="text-slate-300 text-[11px]">Dusri site se entry darj hui hai.</div>
        </div>
        <button onclick="window.location.reload()" class="px-2 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-[10px] font-bold">
            Refresh
        </button>
    </div>

    <!-- PWA Service Worker & Real-Time Sync Script -->
    <script>
    // 1. Register Service Worker
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then(reg => console.log('[PWA] Service Worker registered:', reg.scope))
                .catch(err => console.log('[PWA] Service Worker registration failed:', err));
        });
    }

    // 2. Handle Mobile Install Prompt
    let deferredPrompt = null;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        const banner = document.getElementById('pwaInstallBanner');
        if (banner && !localStorage.getItem('sandip_install_dismissed')) {
            banner.classList.remove('hidden');
        }
    });

    const installBtn = document.getElementById('pwaInstallBtn');
    if (installBtn) {
        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log('[PWA] User response:', outcome);
                deferredPrompt = null;
                document.getElementById('pwaInstallBanner').classList.add('hidden');
            }
        });
    }

    function dismissInstallBanner() {
        document.getElementById('pwaInstallBanner').classList.add('hidden');
        localStorage.setItem('sandip_install_dismissed', 'true');
    }

    // 3. Online / Offline Status Detection
    function updateOnlineStatus() {
        const badge = document.getElementById('networkBadge');
        const text = document.getElementById('networkText');
        if (!badge || !text) return;

        if (navigator.onLine) {
            badge.className = "inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30";
            text.textContent = "Online (Live Sync)";
            syncPendingOfflineQueue();
        } else {
            badge.className = "inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-400/30";
            text.textContent = "Offline (Saved locally)";
        }
    }

    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    document.addEventListener('DOMContentLoaded', updateOnlineStatus);

    // 4. Offline Queue Sync to Server
    async function syncPendingOfflineQueue() {
        try {
            const queue = JSON.parse(localStorage.getItem('sandip_offline_queue') || '[]');
            if (queue.length === 0) return;

            console.log(`[PWA] Syncing ${queue.length} pending offline entries to server...`);
            const res = await fetch('/api/sync/batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ entries: queue })
            });
            const data = await res.json();
            if (data.success) {
                localStorage.removeItem('sandip_offline_queue');
                alert(`✅ Internet judte hi aapki ${data.saved_count} offline entries central server par sync ho gayi hain! Sabhi ko dikhne lagi hain.`);
                window.location.reload();
            }
        } catch (e) {
            console.warn('[PWA] Auto-sync retry failed:', e);
        }
    }

    // 5. Live Poll for other supervisors' new entries (every 25s)
    let lastKnownTotalEntries = null;
    async function checkLiveUpdates() {
        if (!navigator.onLine) return;
        try {
            const res = await fetch('/api/live-status');
            const data = await res.json();
            if (data && data.total_entries !== undefined) {
                if (lastKnownTotalEntries !== null && data.total_entries > lastKnownTotalEntries) {
                    const diff = data.total_entries - lastKnownTotalEntries;
                    const toast = document.getElementById('liveNewEntryToast');
                    const toastText = document.getElementById('liveNewEntryText');
                    if (toast && toastText) {
                        toastText.textContent = `Nayi ${diff} entry aayi hai! Refresh karke dekhein.`;
                        toast.classList.remove('hidden');
                        setTimeout(() => toast.classList.add('hidden'), 8000);
                    }
                }
                lastKnownTotalEntries = data.total_entries;
            }
        } catch (e) {
            // ignore network glitch
        }
    }
    setInterval(checkLiveUpdates, 25000);
    checkLiveUpdates();
    </script>
</body>
'''

    if 'pwaInstallBanner' not in content:
        content = content.replace('</body>', pwa_ui_and_script)

    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("templates/base.html successfully updated with PWA & Auto-Sync UI!")

if __name__ == '__main__':
    update_app_py()
    update_base_html()
