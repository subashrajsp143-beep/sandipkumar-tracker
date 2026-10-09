# -*- coding: utf-8 -*-
"""
Setup Owner PIN 7808:
1. Update app.py backend with PIN 7808 authentication and routes.
2. Update base.html with Owner PIN modal and role-based navigation.
3. Update site_report.html delete button protection.
4. Update generate_standalone_package.py with PIN 7808.
"""
import sys

def patch_app():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update delete route with 7808
    old_pin_check = 'if not pin or str(pin).strip() != "1234":'
    new_pin_check = '''is_owner_auth = session.get("is_owner", False) or (pin and str(pin).strip() == "7808")
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ गलत पिन! केवल मालिक (PIN: 7808) ही एंट्री डिलीट कर सकते हैं।"}), 403'''

    if old_pin_check in content:
        content = content.replace(old_pin_check, new_pin_check, 1)

    # 2. Add Owner Login / Logout endpoints
    owner_routes = '''
# ==========================================
# OWNER PIN (7808) AUTHENTICATION
# ==========================================
@app.route("/api/owner/login", methods=["POST", "OPTIONS"])
def owner_login_api():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json(silent=True) or {}
    pin = str(data.get("pin", "")).strip()
    if pin == "7808":
        session["is_owner"] = True
        return jsonify({"success": True, "is_owner": True, "message": "👑 मालिक मोड सक्रिय (Owner Mode Active)!"})
    return jsonify({"success": False, "is_owner": False, "message": "❌ गलत पिन! केवल मालिक (PIN: 7808) ही लॉगिन कर सकते हैं।"}), 401

@app.route("/api/owner/logout", methods=["POST", "GET"])
def owner_logout_api():
    session["is_owner"] = False
    return jsonify({"success": True, "is_owner": False, "message": "वर्कर मोड में वापस आ गए।"})

@app.route("/api/owner/status", methods=["GET"])
def owner_status_api():
    return jsonify({"is_owner": session.get("is_owner", False)})
'''

    if '@app.route("/api/owner/login"' not in content:
        target = 'if __name__ == "__main__":'
        content = content.replace(target, owner_routes + '\n' + target, 1)

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.py patched with PIN 7808 and Owner authentication routes!")

def patch_base_html():
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add owner modal and client-side role toggle
    owner_modal_and_js = '''
    <!-- OWNER PIN MODAL (PIN: 7808) -->
    <div id="ownerPinModal" class="hidden fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border border-slate-200 text-center space-y-4 animate-scaleIn">
            <div class="w-16 h-16 rounded-2xl bg-amber-100 text-amber-600 flex items-center justify-center text-3xl mx-auto shadow-inner">
                <i class="fa-solid fa-crown text-amber-500"></i>
            </div>
            <div>
                <h3 class="text-lg font-black text-slate-800">मालिक लॉगिन (Owner Mode)</h3>
                <p class="text-xs text-slate-500 mt-1">मास्टर कंट्रोल, कुल खर्चे और डिलीट पावर के लिए 4 अंकों का पिन डालें:</p>
            </div>
            <div>
                <input type="password" id="ownerPinInput" maxlength="6" placeholder="••••" class="w-full text-center text-2xl tracking-[0.5em] font-black py-3 rounded-2xl border-2 border-slate-300 focus:border-amber-500 focus:outline-none bg-slate-50 text-slate-900">
                <div id="ownerPinError" class="hidden text-xs text-rose-600 font-bold mt-2"></div>
            </div>
            <div class="grid grid-cols-2 gap-3 pt-2">
                <button type="button" onclick="closeOwnerPinModal()" class="py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition">
                    रद्द करें (Cancel)
                </button>
                <button type="button" onclick="submitOwnerPin()" class="py-2.5 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black text-xs shadow-lg transition">
                    लॉगिन करें (Unlock)
                </button>
            </div>
            <p class="text-[10px] text-slate-400 pt-1">वर्कर को इस पिन की जानकारी नहीं होनी चाहिए।</p>
        </div>
    </div>

    <script>
    // --- OWNER ROLE (PIN: 7808) CLIENT LOGIC ---
    function isOwnerLoggedIn() {
        return localStorage.getItem('sandip_is_owner') === 'true';
    }

    function openOwnerPinModal() {
        const modal = document.getElementById('ownerPinModal');
        const input = document.getElementById('ownerPinInput');
        const err = document.getElementById('ownerPinError');
        if (modal) {
            modal.classList.remove('hidden');
            if (input) { input.value = ''; input.focus(); }
            if (err) err.classList.add('hidden');
        }
    }

    function closeOwnerPinModal() {
        const modal = document.getElementById('ownerPinModal');
        if (modal) modal.classList.add('hidden');
    }

    async function submitOwnerPin() {
        const input = document.getElementById('ownerPinInput');
        const err = document.getElementById('ownerPinError');
        const pin = (input ? input.value : '').trim();

        if (pin === '7808') {
            try {
                await fetch('/api/owner/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pin: pin })
                });
            } catch(e) {}

            localStorage.setItem('sandip_is_owner', 'true');
            closeOwnerPinModal();
            alert('👑 स्वागत है मालिक साहब! मास्टर कंट्रोल सक्रिय हो गया है।');
            window.location.reload();
        } else {
            if (err) {
                err.textContent = '❌ गलत पिन! केवल मालिक ही लॉगिन कर सकते हैं।';
                err.classList.remove('hidden');
            }
            if (input) input.value = '';
        }
    }

    async function logoutOwner() {
        if (!confirm('क्या आप मालिक मोड से बाहर निकलकर वर्कर मोड में जाना चाहते हैं?')) return;
        localStorage.removeItem('sandip_is_owner');
        try {
            await fetch('/api/owner/logout', { method: 'POST' });
        } catch(e) {}
        alert('वर्कर मोड सक्रिय हो गया है।');
        window.location.reload();
    }

    // Apply role-based visibility across the page
    document.addEventListener('DOMContentLoaded', () => {
        const isOwner = isOwnerLoggedIn();
        const ownerBtn = document.getElementById('navOwnerLoginBtn');
        const ownerActiveBadge = document.getElementById('navOwnerActiveBadge');

        if (isOwner) {
            if (ownerBtn) ownerBtn.classList.add('hidden');
            if (ownerActiveBadge) ownerActiveBadge.classList.remove('hidden');
            document.querySelectorAll('.owner-only').forEach(el => el.classList.remove('hidden'));
        } else {
            if (ownerBtn) ownerBtn.classList.remove('hidden');
            if (ownerActiveBadge) ownerActiveBadge.classList.add('hidden');
            document.querySelectorAll('.owner-only').forEach(el => el.classList.add('hidden'));
            // Hide delete buttons in tables for workers
            document.querySelectorAll('.owner-delete-btn').forEach(el => el.classList.add('hidden'));
        }
    });
    </script>
    '''

    # Add button to top navbar
    old_nav_end = '''                <!-- Mobile Menu Button -->
                <div class="md:hidden flex items-center">'''

    new_nav_end = '''                <!-- Owner Mode Button / Crown in Navbar -->
                <div class="flex items-center gap-2">
                    <button type="button" id="navOwnerLoginBtn" onclick="openOwnerPinModal()" class="px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 text-slate-950 font-black text-xs shadow-md transition flex items-center gap-1.5">
                        <i class="fa-solid fa-lock"></i> <span class="hidden sm:inline">मालिक लॉगिन</span><span class="sm:hidden">मालिक</span>
                    </button>
                    <div id="navOwnerActiveBadge" class="hidden flex items-center gap-1.5">
                        <span class="px-2.5 py-1 rounded-xl bg-emerald-500 text-white font-black text-xs shadow-md flex items-center gap-1.5 animate-pulse">
                            <i class="fa-solid fa-crown text-amber-300"></i> <span class="hidden sm:inline">👑 मालिक</span>
                        </span>
                        <button type="button" onclick="logoutOwner()" class="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition" title="वर्कर मोड में बदलें">
                            <i class="fa-solid fa-power-off text-rose-400"></i>
                        </button>
                    </div>
                </div>

                <!-- Mobile Menu Button -->
                <div class="md:hidden flex items-center">'''

    if old_nav_end in content and 'navOwnerLoginBtn' not in content:
        content = content.replace(old_nav_end, new_nav_end, 1)

    # Wrap confidential admin links with owner-only class
    admin_links_old = '''                    <a href="{{ url_for('monthly_report') }}" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-brand-800 hover:text-white transition flex items-center gap-2">
                        <i class="fa-solid fa-calendar-days text-xs"></i> Mahina-war
                    </a>'''
    admin_links_new = '''                    <a href="{{ url_for('monthly_report') }}" class="owner-only hidden px-3 py-2 rounded-md text-sm font-medium text-amber-200 hover:bg-brand-800 hover:text-white transition flex items-center gap-2">
                        <i class="fa-solid fa-calendar-days text-xs"></i> Mahina-war
                    </a>'''

    if admin_links_old in content:
        content = content.replace(admin_links_old, admin_links_new, 1)

    if 'ownerPinModal' not in content:
        content = content.replace('</body>', owner_modal_and_js + '\n</body>', 1)

    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("templates/base.html patched with Owner PIN 7808 UI & Role toggles!")

def patch_site_report_delete_pin():
    with open('templates/site_report.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Tag delete buttons with owner-delete-btn class
    old_btn = 'class="p-1.5 rounded-lg bg-rose-50 text-rose-500 hover:text-rose-700 transition" title="Delete Karein"'
    new_btn = 'class="owner-delete-btn p-1.5 rounded-lg bg-rose-50 text-rose-500 hover:text-rose-700 transition" title="Delete Karein (मालिक केवल)"'
    if old_btn in content:
        content = content.replace(old_btn, new_btn)

    # In JS deleteEntry, check for PIN 7808
    old_pin_prompt = "const pin = prompt('🚨 SURAKSHA CHEK (Malik Authorization):\\n\\nKeval Malik hi record delete kar sakte hain.\\nKripya Malik PIN dalein:');"
    new_pin_prompt = """const storedOwner = localStorage.getItem('sandip_is_owner') === 'true';
        let pin = '7808';
        if (!storedOwner) {
            pin = prompt('🚨 SURAKSHA CHECK (मालिक केवल):\\n\\nरिकॉर्ड केवल मालिक ही हटा सकते हैं।\\nकृपया मालिक PIN (7808) डालें:');
            if (!pin) return;
            if (pin.trim() !== '7808') {
                alert('❌ गलत पिन! केवल मालिक ही डिलीट कर सकते हैं।');
                return;
            }
        }"""

    if old_pin_prompt in content:
        content = content.replace(old_pin_prompt, new_pin_prompt, 1)

    with open('templates/site_report.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("templates/site_report.html delete button secured with PIN 7808!")

if __name__ == '__main__':
    patch_app()
    patch_base_html()
    patch_site_report_delete_pin()
