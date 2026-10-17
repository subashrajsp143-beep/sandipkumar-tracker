# -*- coding: utf-8 -*-
"""
Main Flask Web Application for Multi-Site Material Consumption Tracker.
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, send_from_directory, session
import datetime
import os
import uuid
import json
import urllib.request
import urllib.parse
import base64
import re
import io
import database
import exporter
import ocr_extractor
import photo_service

app = Flask(__name__)
app.secret_key = "construction-material-secret-key-19-sites"
app.permanent_session_lifetime = datetime.timedelta(days=365)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Ensure DB is created on startup
database.init_db()

@app.context_processor
def inject_common():
    return {
        "current_date": (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d"),
        "now_year": (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).year,
        "user_role": session.get("role", "guest"),
        "user_name": session.get("worker_name", ""),
        "user_site_id": session.get("site_id", None),
        "user_site_name": session.get("site_name", ""),
        "all_sites_list": database.get_all_sites()
    }

@app.before_request
def ensure_canonical_and_auth():
    host = request.host.lower()
    if "ms-sandipkumar-tracker.onrender.com" in host:
        url = request.url.replace("ms-sandipkumar-tracker.onrender.com", "sandipkumar-tracker.onrender.com")
        return redirect(url, code=301)

    # Public paths that never require login
    path = request.path
    if (path.startswith("/static") or 
        path.startswith("/uploads") or 
        path in ["/login", "/api/auth/worker-login", "/api/auth/supervisor-login", "/api/owner/login", 
                 "/logout", "/manifest.json", "/sw.js", "/api/live-status", "/website"] or
        path.startswith("/worker/") or 
        path == "/api/worker/ping"):
        return None

    role = session.get("role")
    is_owner = session.get("is_owner", False) or role == "owner"

    # If worker is logged in, restrict to worker portal only (privacy protection)
    # BUT if worker role is Data Entry / DEO, allow them to also access daily entry!
    if role == "worker":
        allowed_worker_paths = ["/my-attendance", "/logout", "/api/worker/ping"]
        worker_role = session.get("worker_role", "")
        if worker_role in ["Data Entry", "DEO", "डाटा एंट्री"]:
            allowed_worker_paths.extend(["/entry", "/daily-entry", "/api/entries", "/api/scan-slip", "/api/parse-text"])
        if path not in allowed_worker_paths:
            return redirect(url_for("my_attendance_portal"))

    # If not logged in at all, direct them to login
    if not role and not is_owner:
        if path in ["/", "/dashboard", "/portal", "/stock", "/entry", "/daily-entry", 
                    "/reports", "/attendance", "/geo-attendance", "/sites", "/materials", "/store"]:
            return redirect(url_for("login_page"))


# 24/7 Keep-Alive & 10:30 AM GPS Attendance Auto-Analyzer Daemon
def _start_keep_alive_daemon():
    def ping_worker():
        import time
        import urllib.request
        # Wait 60 seconds after boot to let server warm up
        time.sleep(60)
        target_urls = [
            "https://sandipkumar-tracker.onrender.com/api/live-status",
            "https://ms-sandipkumar-tracker.onrender.com/api/live-status"
        ]
        last_synced_date = None
        while True:
            # 1. 24/7 Render Keep-Alive Ping
            for url in target_urls:
                try:
                    req = urllib.request.Request(
                        url,
                        headers={"User-Agent": "SandipTracker-KeepAlive/2.0"}
                    )
                    urllib.request.urlopen(req, timeout=12)
                except Exception:
                    pass

            # 2. Check IST time for 10:30 AM Auto-Sync
            try:
                ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
                today_str = ist_now.strftime("%Y-%m-%d")
                # Trigger once daily at 10:30 AM IST
                if ist_now.hour == 10 and ist_now.minute >= 30 and last_synced_date != today_str:
                    database.auto_sync_gps_to_manpower(today_str)
                    last_synced_date = today_str
                    print(f"[{ist_now.strftime('%H:%M:%S')}] 10:30 AM GPS Auto-Attendance Sync Completed for {today_str}")
            except Exception as e:
                print(f"Auto-sync worker notice: {e}")

            # Sleep 60 seconds (1 minute interval)
            time.sleep(60)

    try:
        import threading
        t = threading.Thread(target=ping_worker, daemon=True)
        t.start()
    except Exception as e:
        print(f"Keep-alive thread notice: {e}")

_start_keep_alive_daemon()


# 0. App Root Landing - Role-Based Smart Router
@app.route("/")
def home_index():
    role = session.get("role")
    if role == "worker":
        return redirect(url_for("my_attendance_portal"))
    elif role == "supervisor":
        sid = session.get("site_id")
        return redirect(url_for("site_stock", site_id=sid) if sid else url_for("site_stock"))
    elif role == "owner" or session.get("is_owner"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))

# 0.1 Public Showcase Website
@app.route("/website")
def company_website():
    stats = database.get_dashboard_stats()
    sites = database.get_all_sites()
    materials = database.get_all_materials()
    return render_template("website.html", stats=stats, sites=sites, materials=materials)

# 0.2 Universal Login Page
@app.route("/login")
def login_page():
    role = session.get("role")
    if role == "worker":
        return redirect(url_for("my_attendance_portal"))
    elif role == "supervisor":
        return redirect(url_for("site_stock"))
    elif role == "owner" or session.get("is_owner"):
        return redirect(url_for("dashboard"))
    
    sites = database.get_all_sites()
    return render_template("login.html", sites=sites)

# 0.3 Worker Login API
@app.route("/api/auth/worker-login", methods=["POST", "OPTIONS"])
def api_worker_login():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        site_id = int(data.get("site_id", 0))
        role = data.get("role", "Helper").strip()
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()

        if not site_id or not name:
            return jsonify({"success": False, "message": "साइट और नाम भरना अनिवार्य है।"}), 400

        worker = database.get_or_create_worker(site_id, name, role, phone)
        session.permanent = True
        session["role"] = "worker"
        session["worker_id"] = worker["id"]
        session["worker_token"] = worker["worker_token"]
        session["worker_name"] = worker["name"]
        session["worker_role"] = worker["role"]
        session["worker_phone"] = worker["phone"]
        session["site_id"] = worker["site_id"]
        session["site_name"] = worker["site_name"]

        return jsonify({"success": True, "worker": worker})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 0.4 Supervisor Login API
@app.route("/api/auth/supervisor-login", methods=["POST", "OPTIONS"])
def api_supervisor_login():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        site_id = int(data.get("site_id", 0))
        role = data.get("role", "Supervisor").strip()
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()

        if not site_id or not name:
            return jsonify({"success": False, "message": "साइट और नाम भरना अनिवार्य है।"}), 400

        worker = database.get_or_create_worker(site_id, name, role, phone)
        session.permanent = True
        session["role"] = "supervisor"
        session["is_owner"] = False
        session["worker_id"] = worker["id"]
        session["worker_token"] = worker["worker_token"]
        session["worker_name"] = worker["name"]
        session["worker_role"] = worker["role"]
        session["worker_phone"] = worker["phone"]
        session["site_id"] = worker["site_id"]
        session["site_name"] = worker["site_name"]

        # Capture & Process Live GPS Location during Login
        lat = data.get("latitude")
        lng = data.get("longitude")
        location_status = "pending"
        distance_m = None
        if lat and lng:
            try:
                ping_res = database.process_location_ping(
                    worker_id=worker["id"],
                    site_id=worker["site_id"],
                    lat=float(lat),
                    lng=float(lng),
                    site_lat=worker.get("site_lat"),
                    site_lng=worker.get("site_lng"),
                    radius=worker.get("site_radius") or 500
                )
                location_status = "on_site" if ping_res.get("is_on_site") else "off_site"
                distance_m = ping_res.get("distance_m")
            except Exception as pe:
                pass

        return jsonify({
            "success": True, 
            "worker": worker,
            "location_status": location_status,
            "distance_m": distance_m
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 0.5 Worker Dedicated Portal (Only Their Own Attendance & GPS)
@app.route("/my-attendance")
def my_attendance_portal():
    wid = session.get("worker_id")
    if not wid:
        return redirect(url_for("login_page"))
    
    token = session.get("worker_token")
    worker = database.get_worker_by_token(token) if token else None
    if not worker:
        return redirect(url_for("login_page"))

    today_att = database.get_worker_today_status(wid)
    history = database.get_worker_attendance_history(wid, limit=30)

    return render_template(
        "worker_portal.html",
        worker=worker,
        today_att=today_att,
        history=history
    )

# 0.6 Universal Logout
@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for("login_page"))

# 1. Internal Contractor Portal & Tracker Dashboard
@app.route("/dashboard")
@app.route("/portal")
def dashboard():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        return redirect(url_for("site_stock"))

    stats = database.get_dashboard_stats()
    sites = database.get_all_sites()
    return render_template("dashboard.html", stats=stats, sites=sites)

# 1.1 Download Windows Desktop Launcher BAT
@app.route("/download/desktop-launcher")
def download_desktop_launcher():
    bat_content = """@echo off
title M/S SANDIP KUMAR 24x7 TRACKER
echo Opening M/S Sandip Kumar 24x7 Cloud Tracker...
start https://sandipkumar-tracker.onrender.com/
exit
"""
    return send_file(
        io.BytesIO(bat_content.encode("utf-8")),
        mimetype="application/x-bat",
        as_attachment=True,
        download_name="OPEN_SANDIP_KUMAR_APP.bat"
    )

# 2. Daily Material Usage Entry
@app.route("/entry")
@app.route("/daily-entry")
def daily_entry():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    sites = database.get_all_sites()
    locked_site = None
    if not is_owner and user_site_id:
        user_site_id = int(user_site_id)
        locked_site = database.get_site_by_id(user_site_id)
        sites = [s for s in sites if s["id"] == user_site_id]

    materials = database.get_all_materials()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    return render_template(
        "daily_entry.html", 
        sites=sites, 
        materials=materials, 
        today=today_str,
        locked_site_id=user_site_id if not is_owner else None,
        locked_site=locked_site
    )

@app.route("/api/entries", methods=["POST"])
def save_entries():
    try:
        data = request.get_json()
        site_id = int(data.get("site_id"))
        usage_date = data.get("usage_date") or datetime.date.today().strftime("%Y-%m-%d")
        purpose = data.get("purpose", "")
        entered_by = data.get("entered_by", "")
        items = data.get("items", [])

        if not site_id or not items:
            return jsonify({"success": False, "message": "Site aur materials select karna anivarya hai."}), 400

        # Security check: If not owner, prevent posting to other sites
        is_owner = session.get("is_owner", False)
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id:
            if site_id != int(user_site_id):
                return jsonify({"success": False, "message": "❌ सुरक्षा प्रतिबंध: आप केवल अपनी अधिकृत साइट की खपत दर्ज कर सकते हैं।"}), 403

        added_count = 0
        for item in items:
            mat_id = int(item["material_id"])
            qty = float(item["quantity"])
            rate = float(item.get("rate", 0))
            item_remarks = item.get("remarks", "")
            if qty > 0:
                database.add_consumption_entry(
                    site_id=site_id,
                    material_id=mat_id,
                    usage_date=usage_date,
                    quantity=qty,
                    rate=rate,
                    purpose=purpose,
                    entered_by=entered_by,
                    remarks=item_remarks
                )
                added_count += 1

        return jsonify({"success": True, "message": f"{added_count} material entries safalta-purvak save ho gayi hain!", "count": added_count})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error saving entries: {str(e)}"}), 500

@app.route("/api/entries/<int:entry_id>", methods=["DELETE", "OPTIONS"])
def delete_entry(entry_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        # Security: Require Owner PIN (Default: 1234) to delete financial logs
        data = request.get_json(silent=True) or {}
        pin = request.args.get("pin") or data.get("pin") or request.headers.get("X-Admin-PIN")
        is_owner_auth = session.get("is_owner", False) or (pin and str(pin).strip() == "7808")
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ गलत पिन! केवल अधिकृत मालिक ही एंट्री डिलीट कर सकते हैं।"}), 403

        database.delete_consumption_entry(entry_id)
        return jsonify({"success": True, "message": "Entry delete ho gayi."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/entries/<int:entry_id>", methods=["PUT", "POST", "OPTIONS"])
def update_entry(entry_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or request.form
        success = database.update_consumption_entry(
            entry_id=entry_id,
            site_id=data.get("site_id"),
            material_id=data.get("material_id"),
            usage_date=data.get("usage_date"),
            quantity=data.get("quantity"),
            rate=data.get("rate"),
            purpose=data.get("purpose"),
            entered_by=data.get("entered_by"),
            remarks=data.get("remarks")
        )
        if success:
            return jsonify({"success": True, "message": "Entry safalta-purvak update ho gayi!"})
        else:
            return jsonify({"success": False, "message": "Entry nahi mili."}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Full Database Backup Export API (JSON)
@app.route("/api/backup", methods=["GET"])
def export_database_backup():
    is_owner = session.get("is_owner", False)
    if not is_owner:
        return jsonify({"success": False, "message": "❌ सुरक्षा प्रतिबंध: केवल अधिकृत मालिक ही पूरा डेटा बैकअप डाउनलोड कर सकते हैं।"}), 403
    try:
        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sites ORDER BY id ASC")
        sites = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM materials ORDER BY id ASC")
        materials = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM daily_consumption ORDER BY id ASC")
        entries = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM daily_manpower ORDER BY id ASC")
        manpower = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT * FROM material_inward ORDER BY id ASC")
        inward = [dict(r) for r in cursor.fetchall()]
        conn.close()

        backup_data = {
            "version": "2.0",
            "app": "M/S SANDIP KUMAR MATERIAL TRACKER",
            "exported_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_sites": len(sites),
            "total_materials": len(materials),
            "total_entries": len(entries),
            "total_manpower": len(manpower),
            "total_inward": len(inward),
            "sites": sites,
            "materials": materials,
            "entries": entries,
            "daily_manpower": manpower,
            "material_inward": inward
        }
        resp = jsonify(backup_data)
        resp.headers["Content-Disposition"] = f"attachment; filename=SANDIP_KUMAR_BACKUP_{datetime.date.today().strftime('%Y%m%d')}.json"
        return resp
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Full Database Restore API
@app.route("/api/restore", methods=["POST", "OPTIONS"])
def restore_database_backup():
    if request.method == "OPTIONS":
        return "", 200
    try:
        backup_file = request.files.get("backup_file")
        if backup_file:
            data = json.load(backup_file)
        else:
            data = request.get_json(silent=True) or {}
        
        entries = data.get("entries", [])
        if not entries:
            return jsonify({"success": False, "message": "Backup file me koi entries nahi mili."}), 400

        conn = database.get_db()
        cursor = conn.cursor()
        for e in entries:
            cursor.execute("SELECT id FROM daily_consumption WHERE id = ?", (e.get("id"),))
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE daily_consumption
                    SET site_id = ?, material_id = ?, usage_date = ?, quantity = ?, rate = ?, total_amount = ?, purpose = ?, entered_by = ?, remarks = ?
                    WHERE id = ?
                """, (e.get("site_id"), e.get("material_id"), e.get("usage_date"), e.get("quantity"), e.get("rate"), e.get("total_amount"), e.get("purpose"), e.get("entered_by"), e.get("remarks"), e.get("id")))
            else:
                cursor.execute("""
                    INSERT INTO daily_consumption (id, site_id, material_id, usage_date, quantity, rate, total_amount, purpose, entered_by, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (e.get("id"), e.get("site_id"), e.get("material_id"), e.get("usage_date"), e.get("quantity"), e.get("rate"), e.get("total_amount"), e.get("purpose"), e.get("entered_by"), e.get("remarks")))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": f"{len(entries)} entries safalta se restore ho gayi!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 2.1 AI Photo / Parchi Slip Scanner Endpoint
@app.route("/api/scan-slip", methods=["POST"])
def scan_slip():
    try:
        if "photo" not in request.files:
            return jsonify({"success": False, "message": "Koi photo upload nahi ki gayi."}), 400
        
        file = request.files["photo"]
        if file.filename == "":
            return jsonify({"success": False, "message": "File ka naam khali hai."}), 400

        # Save image file safely
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            ext = ".png"
        
        filename = f"slip_{uuid.uuid4().hex[:10]}{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Run native Windows OCR
        lines = ocr_extractor.run_native_ocr(filepath)
        if not lines:
            return jsonify({"success": False, "message": "Photo se text read nahi ho paya. Kripya saaf photo upload karein."})

        # Match with master materials
        detected_items = ocr_extractor.extract_quantities_and_materials(lines)

        return jsonify({
            "success": True,
            "message": f"{len(detected_items)} materials pehchaan liye gaye!",
            "raw_lines": lines,
            "detected_items": detected_items
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Scan error: {str(e)}"}), 500

# 2.2 Quick Text / WhatsApp Message Parser Endpoint
@app.route("/api/parse-text", methods=["POST"])
def parse_text():
    try:
        data = request.get_json() or {}
        raw_text = data.get("text", "")
        if not raw_text.strip():
            return jsonify({"success": False, "message": "Text khali hai."}), 400

        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        detected_items = ocr_extractor.extract_quantities_and_materials(lines)

        return jsonify({
            "success": True,
            "message": f"{len(detected_items)} items detect huye!",
            "detected_items": detected_items
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 2.3 Material Store & Requisition
@app.route("/store")
def material_store():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    sites = database.get_all_sites()
    locked_site = None
    if not is_owner and user_site_id:
        user_site_id = int(user_site_id)
        locked_site = database.get_site_by_id(user_site_id)
        sites = [s for s in sites if s["id"] == user_site_id]

    materials = database.get_all_materials()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    categories = sorted(list(set(m["category"] for m in materials if m.get("category"))))
    return render_template(
        "store.html", 
        sites=sites, 
        materials=materials, 
        categories=categories, 
        today=today_str,
        locked_site_id=user_site_id if not is_owner else None,
        locked_site=locked_site
    )

def process_and_save_photo(url_or_path, material_id):
    """
    1. If it's a Google Image search URL (google.com/imgres?...imgurl=...), extract the real image link.
    2. If it's a webpage HTML URL, extract og:image / twitter:image product image.
    3. Download, validate via PIL, and save locally in uploads/materials/ for offline and standalone support.
    """
    if not url_or_path:
        return url_or_path
    
    clean_url = url_or_path.strip()

    # 1. Extract from Google Image search or Ad redirect URL
    if "google." in clean_url or "googleadservices." in clean_url:
        try:
            parsed = urllib.parse.urlparse(clean_url)
            qs = urllib.parse.parse_qs(parsed.query)
            if "imgurl" in qs and qs["imgurl"]:
                clean_url = qs["imgurl"][0]
            elif "adurl" in qs and qs["adurl"]:
                clean_url = qs["adurl"][0]
            elif "url" in qs and qs["url"]:
                clean_url = qs["url"][0]
            elif "q" in qs and qs["q"] and qs["q"][0].startswith("http"):
                clean_url = qs["q"][0]
        except Exception:
            pass

    # 2. If already a local path, keep as is
    if clean_url.startswith("/uploads/"):
        return clean_url

    # 3. If Base64 data URI, decode and save to local JPEG file
    if clean_url.startswith("data:image/"):
        try:
            header, encoded = clean_url.split(",", 1)
            raw_bytes = base64.b64decode(encoded)
            import io
            from PIL import Image
            im = Image.open(io.BytesIO(raw_bytes))
            im = im.convert("RGB")
            fname = f"mat_{material_id}_{uuid.uuid4().hex[:6]}.jpg"
            target_dir = os.path.join(UPLOAD_FOLDER, "materials")
            os.makedirs(target_dir, exist_ok=True)
            fpath = os.path.join(target_dir, fname)
            im.save(fpath, format="JPEG", quality=85, optimize=True)
            return f"/uploads/materials/{fname}"
        except Exception as e:
            print(f"Warning: could not process data:image URI: {e}")
            return clean_url

    # 4. If remote HTTP/HTTPS, download and save locally
    if clean_url.startswith("http://") or clean_url.startswith("https://"):
        try:
            req = urllib.request.Request(
                clean_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
                }
            )
            resp = urllib.request.urlopen(req, timeout=10)
            data = resp.read()

            # Check if response is an HTML page (user pasted product page link instead of direct image)
            text_preview = data[:500].decode("utf-8", errors="ignore").lower()
            if "<!doctype html" in text_preview or "<html" in text_preview:
                full_html = data.decode("utf-8", errors="ignore")
                found_img = None
                # Check og:image or twitter:image or itemprop="image" or main image tag
                candidates = (
                    re.findall(r'og:image.*?content=[\"\']([^\"\']+)[\"\']', full_html, re.I) +
                    re.findall(r'content=[\"\']([^\"\']+)[\"\'].*?og:image', full_html, re.I) +
                    re.findall(r'itemprop=[\"\']image[\"\'].*?content=[\"\']([^\"\']+)[\"\']', full_html, re.I) +
                    re.findall(r'content=[\"\']([^\"\']+)[\"\'].*?itemprop=[\"\']image[\"\']', full_html, re.I) +
                    re.findall(r'twitter:image.*?content=[\"\']([^\"\']+)[\"\']', full_html, re.I) +
                    re.findall(r'content=[\"\']([^\"\']+)[\"\'].*?twitter:image', full_html, re.I) +
                    re.findall(r'<img[^>]+id=[\"\'](?:main-image|product-image|landingImage)[\"\'][^>]+src=[\"\']([^\"\']+)[\"\']', full_html, re.I) +
                    re.findall(r'<img[^>]+src=[\"\']([^\"\']+(?:product|catalog|large|detail)[^\"\']+\.(?:jpg|jpeg|png|webp))[\"\']', full_html, re.I)
                )
                if candidates:
                    found_img = candidates[0]

                if found_img:
                    # Recursively fetch the actual image URL
                    return process_and_save_photo(urllib.parse.urljoin(clean_url, found_img), material_id)

            # Verify that data is a valid image using PIL
            import io
            from PIL import Image
            im = Image.open(io.BytesIO(data))
            im = im.convert("RGB")

            fname = f"mat_{material_id}_{uuid.uuid4().hex[:6]}.jpg"
            target_dir = os.path.join(UPLOAD_FOLDER, "materials")
            os.makedirs(target_dir, exist_ok=True)
            fpath = os.path.join(target_dir, fname)
            im.save(fpath, format="JPEG", quality=85, optimize=True)
            return f"/uploads/materials/{fname}"
        except Exception as e:
            print(f"Warning: could not process remote image {clean_url}: {e}")
            return clean_url

    return clean_url

# CORS and Options handler + No-Cache for HTML
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Admin-PIN"
    if "text/html" in response.headers.get("Content-Type", ""):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Fast Photo URL Resolver API for Google Ad & Web Links
@app.route("/api/resolve_photo_url", methods=["POST", "OPTIONS"])
def resolve_photo_url():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        raw_url = data.get("url", "").strip()
        mat_id = data.get("material_id", 0)
        if not raw_url:
            return jsonify({"success": False, "message": "Koi URL nahi mila"}), 400
        
        saved_path = process_and_save_photo(raw_url, mat_id)
        if saved_path and saved_path.startswith("/uploads/"):
            full_path = os.path.join(app.root_path, saved_path.lstrip("/"))
            if os.path.exists(full_path):
                import io
                from PIL import Image
                im = Image.open(full_path)
                im = im.convert("RGB")
                im.thumbnail((380, 380), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, format="JPEG", quality=80, optimize=True)
                b64 = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
                return jsonify({"success": True, "image_url": saved_path, "b64": b64})
        return jsonify({"success": False, "message": "Image extract nahi ho payi"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# 2.4 Update Material Photo (Online URL or File Upload)
@app.route("/api/materials/<int:material_id>/photo", methods=["POST", "OPTIONS"])
def update_material_photo(material_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        # Check if file was uploaded
        if "photo" in request.files and request.files["photo"].filename != "":
            file = request.files["photo"]
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".webp", ".svg"]:
                ext = ".jpg"
            fname = f"mat_{material_id}_{uuid.uuid4().hex[:6]}{ext}"
            target_dir = os.path.join(UPLOAD_FOLDER, "materials")
            os.makedirs(target_dir, exist_ok=True)
            filepath = os.path.join(target_dir, fname)
            file.save(filepath)
            image_url = f"/uploads/materials/{fname}"
        else:
            image_url = request.form.get("image_url", "").strip()
            if not image_url and request.is_json:
                image_url = (request.get_json() or {}).get("image_url", "").strip()

        if not image_url:
            return jsonify({"success": False, "message": "Photo URL ya file upload karna anivarya hai."}), 400

        # Smartly process, extract Google image links and save locally
        final_image_url = process_and_save_photo(image_url, material_id)
        database.update_material_photo(material_id, final_image_url)

        return jsonify({"success": True, "message": "Material photo safalta se update ho gayi!", "image_url": final_image_url})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error updating photo: {str(e)}"}), 500

# 3. Unified Reports Hub (All-in-One: Daily, Monthly, Site, Material, Matrix)
@app.route("/reports")
def reports_hub():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    tab = request.args.get("tab", "daily")
    sites = database.get_all_sites()
    if not is_owner and user_site_id:
        sites = [s for s in sites if s["id"] == int(user_site_id)]

    materials = database.get_all_materials()

    report_date = request.args.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    month_arg = request.args.get("month", datetime.date.today().strftime("%Y-%m"))

    # Daily Data
    daily_entries, site_summaries = [], []
    total_day_cost = 0.0
    if tab == "daily":
        daily_entries, site_summaries = database.get_daily_report(report_date)
        if not is_owner and user_site_id:
            uid = int(user_site_id)
            daily_entries = [e for e in daily_entries if e.get("site_id") == uid]
            site_summaries = [s for s in site_summaries if s.get("id") == uid or s.get("site_id") == uid]
        total_day_cost = sum(s["site_total_cost"] or 0 for s in site_summaries)

    # Monthly Data
    monthly_data = {
        "entries": [], "site_summaries": [], "top_materials": [],
        "daily_trend": [], "total_month_cost": 0.0,
        "total_items_count": 0, "active_sites_count": 0, "available_months": []
    }
    if tab == "monthly":
        monthly_data = database.get_monthly_report(month_arg)

    # Site Wise Data
    site_id_arg = request.args.get("site_id", type=int)
    if not is_owner and user_site_id:
        site_id_arg = int(user_site_id)
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")
    selected_site_id = site_id_arg if site_id_arg else (sites[0]["id"] if sites else None)
    site_entries, site_material_summary = [], []
    selected_site = None
    grand_total = 0.0
    if tab == "site" and selected_site_id:
        selected_site = database.get_site_by_id(selected_site_id)
        site_entries, site_material_summary = database.get_site_report(
            site_id=selected_site_id,
            from_date=from_date if from_date else None,
            to_date=to_date if to_date else None
        )
        grand_total = sum(item["total_amount"] or 0 for item in site_material_summary)

    # Material Wise Data
    mat_id_arg = request.args.get("material_id", type=int)
    selected_mat_id = mat_id_arg if mat_id_arg else (materials[0]["id"] if materials else None)
    selected_material = None
    sites_usage, mat_logs = [], []
    total_qty_all_sites = 0
    total_cost_all_sites = 0
    if tab == "material" and selected_mat_id:
        selected_material = database.get_material_by_id(selected_mat_id)
        sites_usage, mat_logs = database.get_material_distribution(selected_mat_id)
        total_qty_all_sites = sum(u["total_quantity"] or 0 for u in sites_usage)
        total_cost_all_sites = sum(u["total_cost"] or 0 for u in sites_usage)

    # Matrix Data
    matrix_sites, top_mats, matrix = [], [], {}
    if tab == "matrix":
        matrix_sites, top_mats, matrix = database.get_matrix_data()

    return render_template(
        "reports.html",
        active_tab=tab,
        sites=sites,
        materials=materials,
        # Daily
        report_date=report_date,
        entries=daily_entries if tab == "daily" else site_entries,
        site_summaries=site_summaries if tab == "daily" else monthly_data["site_summaries"],
        total_day_cost=total_day_cost,
        # Monthly
        month=month_arg,
        total_month_cost=monthly_data["total_month_cost"],
        active_sites_count=monthly_data["active_sites_count"],
        total_items_count=monthly_data["total_items_count"],
        top_materials=monthly_data["top_materials"],
        daily_trend=monthly_data["daily_trend"],
        available_months=monthly_data["available_months"],
        # Site Wise
        selected_site_id=selected_site_id,
        selected_site=selected_site,
        from_date=from_date,
        to_date=to_date,
        material_summary=site_material_summary,
        grand_total=grand_total,
        # Material Wise
        selected_mat_id=selected_mat_id,
        selected_material=selected_material,
        sites_usage=sites_usage,
        total_qty=total_qty_all_sites,
        total_cost=total_cost_all_sites,
        # Matrix
        matrix_sites=matrix_sites,
        top_mats=top_mats,
        matrix=matrix
    )

# Backwards-compatible report endpoints redirecting to unified reports_hub
@app.route("/reports/sites")
def site_report():
    return redirect(url_for("reports_hub", tab="site", **request.args))

@app.route("/reports/daily")
def daily_report():
    return redirect(url_for("reports_hub", tab="daily", **request.args))

@app.route("/reports/monthly")
def monthly_report():
    return redirect(url_for("reports_hub", tab="monthly", **request.args))

@app.route("/reports/materials")
def material_report():
    return redirect(url_for("reports_hub", tab="material", **request.args))

@app.route("/reports/matrix")
def matrix_report():
    return redirect(url_for("reports_hub", tab="matrix", **request.args))

# 5.1 Dedicated Item Date Timeline (Kab Kab Use Hua)
@app.route("/item-history")
def item_history():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    materials = database.get_all_materials()
    sites = database.get_all_sites()
    mat_id_arg = request.args.get("material_id", type=int)
    site_id_arg = request.args.get("site_id", type=int)

    # Security Lock: If not owner, lock to user's assigned site
    if not is_owner and user_site_id:
        site_id_arg = int(user_site_id)
        sites = [s for s in sites if s["id"] == int(user_site_id)]

    selected_mat_id = mat_id_arg if mat_id_arg else (materials[0]["id"] if materials else None)
    selected_material = database.get_material_by_id(selected_mat_id) if selected_mat_id else None
    selected_site = database.get_site_by_id(site_id_arg) if site_id_arg else None

    history_data = database.get_item_date_timeline(selected_mat_id, site_id=site_id_arg) if selected_mat_id else None

    return render_template(
        "item_history.html",
        materials=materials,
        sites=sites,
        selected_mat_id=selected_mat_id,
        selected_material=selected_material,
        selected_site_id=site_id_arg,
        selected_site=selected_site,
        history=history_data
    )

# 7. Excel Exports
@app.route("/export/site-excel")
def export_site_excel():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    site_id = request.args.get("site_id", type=int)
    if not is_owner and user_site_id:
        site_id = int(user_site_id)
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")
    
    if not site_id:
        return "Site ID is required", 400

    site = database.get_site_by_id(site_id)
    entries, material_summary = database.get_site_report(site_id=site_id, from_date=from_date or None, to_date=to_date or None)
    
    excel_stream = exporter.generate_site_report_excel(
        site_name=site["name"] if site else f"Site_{site_id}",
        entries=entries,
        material_summary=material_summary,
        from_date=from_date,
        to_date=to_date
    )

    filename = f"Material_Report_{site['code'] if site else 'Site'}_{datetime.date.today().strftime('%Y%m%d')}.xlsx"
    return send_file(
        excel_stream,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename
    )

@app.route("/export/daily-excel")
def export_daily_excel():
    report_date = request.args.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    entries, site_summaries = database.get_daily_report(report_date)

    excel_stream = exporter.generate_daily_report_excel(report_date, entries, site_summaries)
    filename = f"Daily_Material_Report_{report_date}.xlsx"
    return send_file(
        excel_stream,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename
    )

@app.route("/export/monthly-excel")
def export_monthly_excel():
    month_arg = request.args.get("month", datetime.date.today().strftime("%Y-%m"))
    report_data = database.get_monthly_report(month_arg)
    excel_stream = exporter.generate_monthly_report_excel(
        month_str=month_arg,
        entries=report_data["entries"],
        site_summaries=report_data["site_summaries"],
        top_materials=report_data["top_materials"]
    )
    filename = f"Monthly_Material_Report_{month_arg}.xlsx"
    return send_file(
        excel_stream,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename
    )

# 8. Sites Master Management
@app.route("/sites")
def sites_list():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        return redirect(url_for("site_stock"))

    sites = database.get_all_sites()
    points_counts = database.get_geo_points_counts_by_site()
    return render_template("sites.html", sites=sites, points_counts=points_counts)

@app.route("/api/sites/<int:site_id>/edit", methods=["POST"])
def edit_site(site_id):
    is_owner = session.get("is_owner", False)
    if not is_owner:
        return jsonify({"success": False, "message": "❌ सुरक्षा प्रतिबंध: केवल अधिकृत मालिक ही साइट विवरण बदल सकते हैं।"}), 403
    try:
        data = request.form
        name = data.get("name", "").strip()
        location = data.get("location", "").strip()
        supervisor = data.get("supervisor", "").strip()
        contact = data.get("contact", "").strip()
        incharge = data.get("incharge", "").strip()
        incharge_phone = data.get("incharge_phone", "").strip()

        if not name:
            flash("Site name cannot be empty", "error")
            return redirect(url_for("sites_list"))

        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sites 
            SET name = ?, location = ?, supervisor = ?, contact = ?, incharge = ?, incharge_phone = ?
            WHERE id = ?
        """, (name, location, supervisor, contact, incharge, incharge_phone, site_id))
        conn.commit()
        conn.close()
        flash("Site details safalta se update ho gayi!", "success")
        return redirect(url_for("sites_list"))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("sites_list"))

@app.route("/api/sites", methods=["POST"])
def add_site():
    try:
        data = request.form
        name = data.get("name", "").strip()
        code = data.get("code", "").strip()
        location = data.get("location", "").strip()
        supervisor = data.get("supervisor", "").strip()
        contact = data.get("contact", "").strip()
        incharge = data.get("incharge", "").strip()
        incharge_phone = data.get("incharge_phone", "").strip()

        is_owner = session.get("is_owner", False)
        if not is_owner:
            flash("❌ केवल अधिकृत मालिक ही नई साइट जोड़ सकते हैं।", "error")
            return redirect(url_for("site_stock"))

        if not name:
            flash("Site name bharna anivarya hai!", "error")
            return redirect(url_for("sites_list"))

        conn = database.get_db()
        cursor = conn.cursor()

        if not code:
            cursor.execute("SELECT COUNT(*) FROM sites")
            cnt = cursor.fetchone()[0] + 1
            code = f"SITE-{cnt:02d}"

        cursor.execute("""
            INSERT INTO sites (code, name, location, supervisor, contact, incharge, incharge_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (code, name, location, supervisor, contact, incharge, incharge_phone))
        conn.commit()
        conn.close()
        flash(f"Nayi Site '{name}' ({code}) safalta se list me jud gayi!", "success")
        return redirect(url_for("sites_list"))
    except Exception as e:
        flash(f"Error adding site: {str(e)}", "error")
        return redirect(url_for("sites_list"))

@app.route("/api/sites/<int:site_id>/delete", methods=["POST"])
def delete_site(site_id):
    is_owner = session.get("is_owner", False)
    if not is_owner:
        flash("❌ केवल अधिकृत मालिक ही साइट हटा सकते हैं।", "error")
        return redirect(url_for("site_stock"))
    try:
        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM daily_consumption WHERE site_id = ?", (site_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            flash(f"Is site par {count} material entries darj hain, isliye ise direct delete nahi kiya ja sakta.", "error")
            conn.close()
            return redirect(url_for("sites_list"))
        
        cursor.execute("DELETE FROM sites WHERE id = ?", (site_id,))
        conn.commit()
        conn.close()
        flash("Site safalta se delete kar di gayi!", "success")
        return redirect(url_for("sites_list"))
    except Exception as e:
        flash(f"Error deleting site: {str(e)}", "error")
        return redirect(url_for("sites_list"))


# 9. Materials Master Management
@app.route("/materials")
def materials_list():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        return redirect(url_for("site_stock"))

    materials = database.get_all_materials()
    return render_template("materials.html", materials=materials)

@app.route("/api/materials", methods=["POST"])
def add_material():
    is_owner = session.get("is_owner", False)
    if not is_owner:
        flash("❌ केवल अधिकृत मालिक ही सामग्री जोड़ सकते हैं।", "error")
        return redirect(url_for("site_stock"))
    try:
        data = request.form
        name = data.get("name", "").strip()
        unit = data.get("unit", "NOS").strip()
        rate = float(data.get("rate", 0))
        category = data.get("category", "General").strip()

        if not name:
            flash("Material name is required", "error")
            return redirect(url_for("materials_list"))

        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO materials (name, unit, rate, category)
            VALUES (?, ?, ?, ?)
        """, (name, unit, rate, category))
        conn.commit()
        conn.close()
        flash("Naya material list me jud gaya!", "success")
        return redirect(url_for("materials_list"))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("materials_list"))

@app.route("/api/materials/<int:mat_id>/edit", methods=["POST"])
def edit_material(mat_id):
    try:
        data = request.form
        name = data.get("name", "").strip()
        unit = data.get("unit", "NOS").strip()
        rate = float(data.get("rate", 0))
        category = data.get("category", "General").strip()

        conn = database.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE materials SET name = ?, unit = ?, rate = ?, category = ?
            WHERE id = ?
        """, (name, unit, rate, category, mat_id))
        conn.commit()
        conn.close()
        flash("Material safalta se update ho gaya!", "success")
        return redirect(url_for("materials_list"))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for("materials_list"))


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

@app.route("/api/live-entries", methods=["GET", "OPTIONS"])
def get_live_entries_api():
    if request.method == "OPTIONS":
        return "", 200
    try:
        entries, _ = database.get_site_report()
        return jsonify({"success": True, "entries": entries})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

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
        session.permanent = True
        session["is_owner"] = True
        session["role"] = "owner"
        session["worker_name"] = "मालिक"
        return jsonify({"success": True, "is_owner": True, "role": "owner", "message": "👑 मालिक मोड सक्रिय (Owner Mode Active)!"})
    return jsonify({"success": False, "is_owner": False, "message": "❌ गलत पिन! केवल अधिकृत मालिक ही लॉगिन कर सकते हैं।"}), 401

@app.route("/api/owner/logout", methods=["POST", "GET"])
def owner_logout_api():
    session["is_owner"] = False
    return jsonify({"success": True, "is_owner": False, "message": "वर्कर मोड में वापस आ गए।"})

@app.route("/api/owner/status", methods=["GET"])
def owner_status_api():
    return jsonify({"is_owner": session.get("is_owner", False)})


# ==========================================
# DAILY MANPOWER ATTENDANCE ROUTES
# ==========================================
@app.route("/attendance")
def attendance_view():
    selected_date = request.args.get("date")
    if not selected_date:
        ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        selected_date = ist_now.strftime("%Y-%m-%d")

    rows, totals = database.get_daily_manpower(selected_date)

    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    is_supervisor_view = False
    locked_site = None

    if not is_owner and user_site_id:
        is_supervisor_view = True
        user_site_id = int(user_site_id)
        locked_site = database.get_site_by_id(user_site_id)
        rows = [r for r in rows if r["site_id"] == user_site_id]
        if rows:
            r0 = rows[0]
            totals = {
                "site_incharge": r0.get("site_incharge", 0),
                "supervisor": r0.get("supervisor", 0),
                "electrician": r0.get("electrician", 0),
                "gi_mistri": r0.get("gi_mistri", 0),
                "deo": r0.get("deo", 0),
                "plumber": r0.get("plumber", 0),
                "helper": r0.get("helper", 0),
                "other": r0.get("other", 0),
                "total": r0.get("total", 0)
            }
        else:
            totals = {
                "site_incharge": 0, "supervisor": 0, "electrician": 0,
                "gi_mistri": 0, "deo": 0, "plumber": 0, "helper": 0, "other": 0, "total": 0
            }

    # Format date for red title: DD/MM/YYYY
    try:
        parts = selected_date.split("-")
        formatted_date = f"{parts[2]}/{parts[1]}/{parts[0]}" if len(parts) == 3 else selected_date
    except:
        formatted_date = selected_date

    return render_template(
        "attendance.html",
        selected_date=selected_date,
        formatted_date=formatted_date,
        rows=rows,
        totals=totals,
        is_supervisor_view=is_supervisor_view,
        locked_site=locked_site
    )

@app.route("/api/attendance", methods=["GET", "POST", "OPTIONS"])
def save_attendance_api():
    if request.method == "OPTIONS":
        return "", 200
    if request.method == "GET":
        att_date = request.args.get("date")
        if not att_date:
            ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
            att_date = ist_now.strftime("%Y-%m-%d")
        rows, totals = database.get_daily_manpower(att_date)
        is_owner = session.get("is_owner", False)
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id:
            rows = [r for r in rows if r["site_id"] == int(user_site_id)]
        return jsonify({"success": True, "date": att_date, "rows": rows, "totals": totals})
    try:
        data = request.get_json(silent=True) or {}
        att_date = data.get("date")
        rows = data.get("rows", [])
        if not att_date:
            return jsonify({"success": False, "message": "तारीख चुनना अनिवार्य है।"}), 400

        # Security check: If not owner, only allow saving attendance for supervisor's site
        is_owner = session.get("is_owner", False)
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id:
            rows = [r for r in rows if int(r.get("site_id", 0)) == int(user_site_id)]

        database.save_daily_manpower(att_date, rows, updated_by=session.get("worker_name", "Web User"))
        return jsonify({"success": True, "message": f"{att_date} की हाजिरी सफलतापूर्वक सेव हो गई!"})
    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500

@app.route("/api/attendance/auto-fetch", methods=["POST", "GET", "OPTIONS"])
def auto_fetch_attendance_from_gps():
    if request.method == "OPTIONS":
        return "", 200
    try:
        ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        att_date = request.args.get("date") or ist_now.strftime("%Y-%m-%d")
        res = database.auto_sync_gps_to_manpower(att_date)
        rows, totals = database.get_daily_manpower(att_date)
        is_owner = session.get("is_owner", False)
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id:
            rows = [r for r in rows if r["site_id"] == int(user_site_id)]
        return jsonify({
            "success": True,
            "date": att_date,
            "updated_sites": res["updated_sites"],
            "total_workers": res["total_workers"],
            "site_counts": res["site_counts"],
            "rows": rows,
            "totals": totals,
            "message": f"✅ GPS से {res['total_workers']} वर्करों की उपस्थिति 21 साइट्स की हाजिरी शीट में स्वतः फेच कर ली गई!"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/export/manpower-excel")
def export_manpower_excel():
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    att_date = request.args.get("date") or ist_now.strftime("%Y-%m-%d")
    rows, totals = database.get_daily_manpower(att_date)
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        rows = [r for r in rows if r["site_id"] == int(user_site_id)]

    excel_file = exporter.generate_manpower_excel(att_date, rows, totals)
    
    clean_date = att_date.replace("-", "_")
    filename = f"MANPOWER_ATTENDANCE_{clean_date}.xlsx"

    return send_file(
        excel_file,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/export/manpower-pdf")
def export_manpower_pdf():
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    att_date = request.args.get("date") or ist_now.strftime("%Y-%m-%d")
    rows, totals = database.get_daily_manpower(att_date)

    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        user_site_id = int(user_site_id)
        rows = [r for r in rows if r["site_id"] == user_site_id]
        if rows:
            r0 = rows[0]
            totals = {
                "site_incharge": r0.get("site_incharge", 0),
                "supervisor": r0.get("supervisor", 0),
                "electrician": r0.get("electrician", 0),
                "gi_mistri": r0.get("gi_mistri", 0),
                "deo": r0.get("deo", 0),
                "plumber": r0.get("plumber", 0),
                "helper": r0.get("helper", 0),
                "other": r0.get("other", 0),
                "total": r0.get("total", 0)
            }

    pdf_file = exporter.generate_manpower_pdf(att_date, rows, totals)
    
    clean_date = att_date.replace("-", "_")
    filename = f"MANPOWER_ATTENDANCE_{clean_date}.pdf"

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )

# ==========================================
# 8.1 SITE WORK PHOTOS & A4 4-PHOTO ALBUM ROUTES
# ==========================================

@app.route("/site-photos")
def site_photos_view():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    site_id_arg = request.args.get("site_id")
    selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None

    # SECURITY LOCK: If supervisor / non-owner, strictly lock to assigned site
    if not is_owner and user_site_id:
        selected_site_id = int(user_site_id)

    selected_month = request.args.get("month", "").strip()
    selected_date = request.args.get("date", "").strip()
    selected_category = request.args.get("category", "").strip()

    sites = database.get_all_sites()
    if not is_owner and user_site_id:
        sites = [s for s in sites if s["id"] == int(user_site_id)]

    selected_site = database.get_site_by_id(selected_site_id) if selected_site_id else None
    available_months = database.get_available_photo_months(site_id=selected_site_id)

    # If no month chosen and we have available months, pick the latest month
    if not selected_month and not selected_date and available_months:
        selected_month = available_months[0]["ym"]
    elif not selected_month and not selected_date:
        ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        selected_month = ist_now.strftime("%Y-%m")

    photos = database.get_site_work_photos(
        site_id=selected_site_id,
        month_str=selected_month if not selected_date else None,
        date_str=selected_date if selected_date else None,
        category=selected_category,
        limit=1000
    )

    total_photos = len(photos)
    total_pages = (total_photos + 3) // 4 if total_photos > 0 else 0
    categories = photo_service.PHOTO_CATEGORIES
    category_counts = database.get_photo_category_counts(site_id=selected_site_id, month_str=selected_month)

    return render_template(
        "site_photos.html",
        sites=sites,
        selected_site=selected_site,
        selected_site_id=selected_site_id,
        locked_site_id=int(user_site_id) if (not is_owner and user_site_id) else None,
        months=available_months,
        selected_month=selected_month,
        selected_date=selected_date,
        selected_category=selected_category,
        categories=categories,
        photos=photos,
        total_photos=total_photos,
        total_pages=total_pages,
        category_counts=category_counts
    )


@app.route("/site-photos/upload", methods=["GET", "POST"])
def site_photo_upload():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    if request.method == "POST":
        try:
            site_id_raw = request.form.get("site_id")
            if not site_id_raw:
                return jsonify({"success": False, "message": "कृपया साइट चुनें"}), 400
            
            # SECURITY RESTRICTION: Non-owners can only upload photos for their own assigned site
            if not is_owner and user_site_id:
                if int(site_id_raw) != int(user_site_id):
                    return jsonify({"success": False, "message": "❌ सुरक्षा प्रतिबंध: आप केवल अपनी अधिकृत साइट की फोटो अपलोड कर सकते हैं।"}), 403

            site = database.get_site_by_id(int(site_id_raw))
            if not site:
                return jsonify({"success": False, "message": "अमान्य साइट"}), 400

            file = request.files.get("photo")
            if not file or file.filename == "":
                return jsonify({"success": False, "message": "कृपया काम की फोटो चुनें"}), 400

            category = request.form.get("category") or "सामान्य कार्य"
            description = request.form.get("description", "").strip()
            photo_date = request.form.get("photo_date")
            uploaded_by = request.form.get("uploaded_by") or session.get("worker_name") or session.get("supervisor_name") or "Staff"
            uploader_phone = session.get("worker_phone") or request.form.get("uploader_phone", "")

            lat = request.form.get("latitude")
            lng = request.form.get("longitude")
            accuracy = request.form.get("accuracy", 0)

            res = photo_service.process_and_save_photo(
                file_storage=file,
                site=site,
                category=category,
                description=description,
                lat=lat,
                lng=lng,
                accuracy=accuracy,
                photo_date=photo_date,
                uploaded_by=uploaded_by,
                uploader_phone=uploader_phone
            )

            return jsonify({
                "success": True,
                "message": f"✅ {site['name']} की फोटो सफलतापूर्वक सेव हो गई!",
                "photo": res
            })
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    # GET: Render Mobile Upload Page
    sites = database.get_all_sites()
    site_id_arg = request.args.get("site_id")
    selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None

    # SECURITY LOCK: If non-owner, lock strictly to assigned site
    if not is_owner and user_site_id:
        selected_site_id = int(user_site_id)
        sites = [s for s in sites if s["id"] == int(user_site_id)]

    uploader_name = session.get("worker_name") or session.get("supervisor_name") or ""
    categories = photo_service.PHOTO_CATEGORIES
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%Y-%m-%d")

    return render_template(
        "photo_upload.html",
        sites=sites,
        selected_site_id=selected_site_id,
        locked_site_id=int(user_site_id) if (not is_owner and user_site_id) else None,
        uploader_name=uploader_name,
        categories=categories,
        today=today
    )


@app.route("/api/site-photos/delete/<int:photo_id>", methods=["POST", "DELETE"])
def delete_site_photo_api(photo_id):
    try:
        is_owner = session.get("is_owner", False)
        user_site_id = session.get("site_id")

        # Security check: If not owner, verify photo belongs to user's site
        if not is_owner and user_site_id:
            conn = database.get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT site_id FROM site_work_photos WHERE id = ?", (photo_id,))
            row = cursor.fetchone()
            conn.close()
            if not row or row[0] != int(user_site_id):
                return jsonify({"success": False, "message": "❌ सुरक्षा प्रतिबंध: आप केवल अपनी अधिकृत साइट की फोटो हटा सकते हैं।"}), 403

        url = database.delete_site_work_photo(photo_id)
        if url and url.startswith("/static/"):
            disk_path = url.lstrip("/")
            if os.path.exists(disk_path):
                try:
                    os.remove(disk_path)
                except Exception:
                    pass
        return jsonify({"success": True, "message": "फोटो सफलतापूर्वक हटा दी गई"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/export/site-photos-pdf")
def export_site_photos_pdf():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    site_id_arg = request.args.get("site_id")
    selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None

    # SECURITY LOCK: If non-owner, strictly lock to assigned site
    if not is_owner and user_site_id:
        selected_site_id = int(user_site_id)

    selected_month = request.args.get("month", "").strip()
    selected_date = request.args.get("date", "").strip()
    selected_category = request.args.get("category", "").strip()

    selected_site = database.get_site_by_id(selected_site_id) if selected_site_id else None

    if not selected_month and not selected_date:
        ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        selected_month = ist_now.strftime("%Y-%m")

    photos = database.get_site_work_photos(
        site_id=selected_site_id,
        month_str=selected_month if not selected_date else None,
        date_str=selected_date if selected_date else None,
        category=selected_category,
        limit=2000
    )

    pdf_buffer = exporter.generate_photo_album_pdf(
        site=selected_site,
        month_str=selected_date if selected_date else selected_month,
        photos=photos
    )

    site_slug = selected_site["code"].replace(" ", "_") if selected_site else "ALL_SITES"
    period_slug = (selected_date or selected_month).replace("-", "_")
    filename = f"A4_PHOTO_ALBUM_{site_slug}_{period_slug}.pdf"

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


@app.route("/site-photos/print-album")
def site_photos_print_album():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    site_id_arg = request.args.get("site_id")
    selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None

    # SECURITY LOCK: If non-owner, strictly lock to assigned site
    if not is_owner and user_site_id:
        selected_site_id = int(user_site_id)

    selected_month = request.args.get("month", "").strip()
    selected_date = request.args.get("date", "").strip()
    selected_category = request.args.get("category", "").strip()

    selected_site = database.get_site_by_id(selected_site_id) if selected_site_id else None

    if not selected_month and not selected_date:
        ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        selected_month = ist_now.strftime("%Y-%m")

    photos = database.get_site_work_photos(
        site_id=selected_site_id,
        month_str=selected_month if not selected_date else None,
        date_str=selected_date if selected_date else None,
        category=selected_category,
        limit=2000
    )

    # Chunk photos into pages of exactly 4 photos each
    pages = [photos[i:i+4] for i in range(0, len(photos), 4)] if photos else []

    return render_template(
        "site_photos_print.html",
        pages=pages,
        selected_site=selected_site,
        selected_site_id=selected_site_id,
        selected_month=selected_date if selected_date else selected_month
    )


# 9. Site Stock & Inventory Register
@app.route("/stock")
def site_stock():
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")

    site_id_arg = request.args.get("site_id")
    selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None
    
    # SECURITY LOCK: If not owner, lock strictly to supervisor's site!
    if not is_owner and user_site_id:
        selected_site_id = int(user_site_id)

    sites = database.get_all_sites()
    if not is_owner and user_site_id:
        sites = [s for s in sites if s["id"] == int(user_site_id)]

    materials = database.get_all_materials()
    stock_rows = database.get_site_stock_inventory(site_id=selected_site_id)
    overview = database.get_all_sites_stock_overview()

    selected_site = database.get_site_by_id(selected_site_id) if selected_site_id else None

    total_inward_sum = sum(r["total_inward"] for r in stock_rows)
    total_consumed_sum = sum(r["total_consumed"] for r in stock_rows)
    balance_sum = sum(r["balance_stock"] for r in stock_rows)
    low_stock_count = sum(1 for r in stock_rows if r["status"] in ["low_stock", "out_of_stock"])

    return render_template(
        "stock.html",
        sites=sites,
        materials=materials,
        stock_rows=stock_rows,
        overview=overview,
        selected_site=selected_site,
        selected_site_id=selected_site_id,
        locked_site_id=int(user_site_id) if (not is_owner and user_site_id) else None,
        total_inward_sum=total_inward_sum,
        total_consumed_sum=total_consumed_sum,
        balance_sum=balance_sum,
        low_stock_count=low_stock_count,
        today=datetime.date.today().strftime("%Y-%m-%d")
    )

@app.route("/api/stock/inward", methods=["POST", "OPTIONS"])
def save_stock_inward():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        # Require Owner PIN or logged-in Supervisor / Site Incharge
        pin = request.args.get("pin") or data.get("pin") or request.headers.get("X-Admin-PIN")
        is_authorized = (session.get("is_owner", False) or 
                         (pin and str(pin).strip() == "7808") or 
                         session.get("role") in ["supervisor", "owner"])
        if not is_authorized:
            return jsonify({"success": False, "message": "❌ स्टॉक एंट्री (माल भेजना) केवल अधिकृत सुपरवाइज़र, साइट इनचार्ज या मालिक ही कर सकते हैं।"}), 403

        site_id = data.get("site_id")
        # SECURITY RESTRICTION: Non-owners can only add stock to their own assigned site
        is_owner = session.get("is_owner", False)
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id:
            if int(site_id) != int(user_site_id):
                return jsonify({"success": False, "message": "❌ सुरक्षा प्रतिबंध: आप केवल अपनी अधिकृत साइट का ही माल दर्ज कर सकते हैं।"}), 403

        inward_date = data.get("inward_date") or datetime.date.today().strftime("%Y-%m-%d")
        challan_no = data.get("challan_no", "")
        supplier = data.get("supplier", "मालिक / हेड ऑफिस")
        remarks = data.get("remarks", "")
        items = data.get("items", [])

        if not site_id or not items:
            return jsonify({"success": False, "message": "साइट और सामान चुनना अनिवार्य है।"}), 400

        added_count = 0
        for it in items:
            mat_id = int(it.get("material_id"))
            qty = float(it.get("quantity") or 0)
            if qty > 0:
                database.add_inward_entry(
                    site_id=int(site_id),
                    material_id=mat_id,
                    inward_date=inward_date,
                    quantity=qty,
                    challan_no=challan_no,
                    supplier=supplier,
                    remarks=remarks
                )
                added_count += 1

        return jsonify({
            "success": True,
            "message": f"{added_count} सामान की इनवर्ड एंट्री (भेजा गया माल) सफलतापूर्वक दर्ज हो गई!",
            "count": added_count
        })
    except Exception as ex:
        return jsonify({"success": False, "message": f"Error: {str(ex)}"}), 500

@app.route("/api/stock/reset-zero", methods=["POST", "OPTIONS"])
def reset_stock_zero_api():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = request.args.get("pin") or data.get("pin") or request.headers.get("X-Admin-PIN")
        is_owner_auth = session.get("is_owner", False) or (pin and str(pin).strip() == "7808")
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ गलत पिन! केवल अधिकृत मालिक ही स्टॉक को 0 (रीसेट) कर सकते हैं।"}), 403

        site_id = data.get("site_id")
        if site_id:
            site_id = int(site_id)

        database.backup_database()
        database.reset_stock_to_zero(site_id=site_id)

        msg = "सभी साइट्स की सामग्री मात्रा और स्टॉक सफलतापूर्वक 0 (रीसेट) कर दिया गया है।" if not site_id else "साइट का स्टॉक सफलतापूर्वक 0 (रीसेट) कर दिया गया है।"
        return jsonify({"success": True, "message": msg})
    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500

@app.route("/api/stock/ledger/<int:site_id>/<int:material_id>")
def get_stock_ledger_api(site_id, material_id):
    try:
        ledger = database.get_material_stock_ledger(site_id, material_id)
        return jsonify({"success": True, "ledger": ledger})
    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500

@app.route("/api/stock/inward/<int:entry_id>", methods=["DELETE", "OPTIONS"])
def delete_stock_inward_api(entry_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = request.args.get("pin") or data.get("pin") or request.headers.get("X-Admin-PIN")
        is_owner_auth = session.get("is_owner", False) or (pin and str(pin).strip() == "7808")
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ गलत पिन! केवल अधिकृत मालिक ही इनवर्ड एंट्री हटा सकते हैं।"}), 403

        database.delete_inward_entry(entry_id)
        return jsonify({"success": True, "message": "इनवर्ड एंट्री हटा दी गई।"})
    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500

@app.route("/export/stock-excel")
def export_stock_excel():
    site_id_arg = request.args.get("site_id")
    selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None
    
    site_name = None
    if selected_site_id:
        s = database.get_site_by_id(selected_site_id)
        if s:
            site_name = s["name"]

    stock_rows = database.get_site_stock_inventory(site_id=selected_site_id)
    excel_file = exporter.generate_site_stock_excel(stock_rows, site_name=site_name)

    safe_name = (site_name or "ALL_SITES").replace(" ", "_")
    filename = f"SITE_STOCK_REGISTER_{safe_name}_{datetime.date.today().strftime('%Y%m%d')}.xlsx"

    return send_file(
        excel_file,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ==========================================
# GPS ATTENDANCE SYSTEM ROUTES
# ==========================================

@app.route("/geo-attendance")
def geo_attendance_admin():
    """Live GPS attendance dashboard."""
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    date_str = request.args.get("date") or ist_now.strftime("%Y-%m-%d")
    rows, date_used = database.get_geo_attendance_today(date_str)
    sites = database.get_all_sites()
    workers = database.get_all_workers()

    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        user_site_id = int(user_site_id)
        rows = [r for r in rows if r["site_id"] == user_site_id]
        sites = [s for s in sites if s["id"] == user_site_id]
        workers = [w for w in workers if w["site_id"] == user_site_id]

    # Group rows by site for display
    by_site = {}
    for r in rows:
        sid = r["site_id"]
        if sid not in by_site:
            by_site[sid] = {"site_name": r["site_name"], "site_code": r["site_code"], "workers": []}
        by_site[sid]["workers"].append(r)

    # Summary counts
    total_w = len(rows)
    present_w = sum(1 for r in rows if r.get("att_status") == "present")
    left_w = sum(1 for r in rows if r.get("att_status") == "left")
    absent_w = total_w - present_w - left_w

    points_counts = database.get_geo_points_counts_by_site()
    site_points_map = {s["id"]: database.get_site_geo_points(s["id"]) for s in sites}

    return render_template(
        "geo_attendance.html",
        rows=rows,
        by_site=by_site,
        date_str=date_str,
        sites=sites,
        workers=workers,
        total_w=total_w,
        present_w=present_w,
        left_w=left_w,
        absent_w=absent_w,
        points_counts=points_counts,
        site_points_map=site_points_map
    )


@app.route("/api/geo-attendance/today")
def geo_attendance_today_api():
    """JSON API for live refresh of GPS attendance data."""
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    date_str = request.args.get("date") or ist_now.strftime("%Y-%m-%d")
    rows, _ = database.get_geo_attendance_today(date_str)
    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        rows = [r for r in rows if r["site_id"] == int(user_site_id)]
    return jsonify({"success": True, "date": date_str, "workers": rows})


@app.route("/api/worker/ping", methods=["POST", "OPTIONS"])
def worker_location_ping():
    """Receives GPS coordinates from a worker's phone and updates attendance."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        token = data.get("token", "").strip()
        lat = float(data.get("lat", 0))
        lng = float(data.get("lng", 0))

        if not token or not lat or not lng:
            return jsonify({"success": False, "message": "Token aur location zaruri hai."}), 400

        worker = database.get_worker_by_token(token)
        if not worker:
            return jsonify({"success": False, "message": "Worker nahi mila ya inactive hai."}), 404

        site_lat = worker.get("site_lat")
        site_lng = worker.get("site_lng")
        radius = worker.get("site_radius") or 1000

        result = database.process_location_ping(
            worker_id=worker["id"],
            site_id=worker["site_id"],
            lat=lat,
            lng=lng,
            site_lat=site_lat,
            site_lng=site_lng,
            radius=radius
        )

        if result.get("distance_m") == 99999.0 and not result.get("is_on_site") and result.get("nearest_point_name") == "GPS सेट नहीं":
            return jsonify({
                "success": True,
                "warning": "Site ka GPS set nahi hua. Admin se GPS set karwayein.",
                "is_on_site": False,
                "distance_m": None,
                "action": "no_gps"
            })

        return jsonify({
            "success": True,
            "worker_name": worker["name"],
            "site_name": worker["site_name"],
            "radius": radius,
            **result
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/worker/<token>")
def worker_tracking_page(token):
    """Worker's personal GPS tracking page — opened on their phone."""
    worker = database.get_worker_by_token(token)
    if not worker:
        return "<h2 style='font-family:sans-serif;text-align:center;margin-top:40px;color:#c00'>❌ Link invalid hai ya worker inactive hai.<br>Admin se naya link maangein.</h2>", 404
    return render_template("worker_tracking.html", worker=worker)


@app.route("/api/workers", methods=["POST", "OPTIONS"])
def add_worker_api():
    """Admin: add a new worker to a site."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        is_owner = session.get("is_owner", False) or (str(pin).strip() == "7808")
        if not is_owner:
            return jsonify({"success": False, "message": "❌ गलत पिन! केवल मालिक ही worker जोड़ सकते हैं।"}), 403

        site_id = int(data.get("site_id", 0))
        name = data.get("name", "").strip()
        role = data.get("role", "Helper").strip()
        phone = data.get("phone", "").strip()

        if not site_id or not name:
            return jsonify({"success": False, "message": "Site aur naam zaruri hai."}), 400

        worker_id, token = database.add_worker(site_id, name, role, phone)
        worker_link = f"https://sandipkumar-tracker.onrender.com/worker/{token}"
        return jsonify({
            "success": True,
            "worker_id": worker_id,
            "token": token,
            "worker_link": worker_link,
            "message": f"✅ {name} ({role}) ko successfully add kar diya! Unhe yeh link bhejein."
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/workers/<int:worker_id>/delete", methods=["POST", "OPTIONS"])
def delete_worker_api(worker_id):
    """Admin: soft-delete a worker (is_active = 0)."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        is_owner = session.get("is_owner", False) or (str(pin).strip() == "7808")
        if not is_owner:
            return jsonify({"success": False, "message": "❌ गलत पिन! केवल मालिक ही worker हटा सकते हैं।"}), 403
        database.delete_worker(worker_id)
        return jsonify({"success": True, "message": "Worker hataya gaya."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/sites/<int:site_id>/gps", methods=["POST", "OPTIONS"])
def set_site_gps(site_id):
    """Admin / Supervisor: save GPS coordinates for a site."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        is_owner = session.get("is_owner", False) or (str(pin).strip() == "7808")
        is_supervisor_of_site = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == site_id)
        if not (is_owner or is_supervisor_of_site):
            return jsonify({"success": False, "message": "❌ केवल अधिकृत सुपरवाइज़र या मालिक ही GPS सेट कर सकते हैं।"}), 403

        lat = float(data.get("latitude", 0))
        lng = float(data.get("longitude", 0))
        radius = int(data.get("radius", 1000))

        if not lat or not lng:
            return jsonify({"success": False, "message": "Latitude aur longitude zaruri hai."}), 400

        database.update_site_gps(site_id, lat, lng, radius)
        return jsonify({"success": True, "message": f"✅ Site GPS set ho gaya! ({lat:.5f}, {lng:.5f}) — {radius}m radius."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/sites/<int:site_id>/points", methods=["GET", "POST", "OPTIONS"])
def site_geo_points_api(site_id):
    """Admin / Supervisor: view and add multi-location GPS points for wide-radius sites."""
    if request.method == "OPTIONS":
        return "", 200
    if request.method == "GET":
        points = database.get_site_geo_points(site_id)
        return jsonify({"success": True, "site_id": site_id, "points": points})

    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        is_owner = session.get("is_owner", False) or (str(pin).strip() == "7808")
        is_supervisor_of_site = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == site_id)
        if not (is_owner or is_supervisor_of_site):
            return jsonify({"success": False, "message": "❌ केवल अधिकृत सुपरवाइज़र या मालिक ही GPS कार्य स्थल जोड़ सकते हैं।"}), 403

        point_name = data.get("point_name", "").strip()
        lat = float(data.get("latitude", 0))
        lng = float(data.get("longitude", 0))
        radius = int(data.get("radius", 1000))

        if not point_name or not lat or not lng:
            return jsonify({"success": False, "message": "पॉइंट का नाम, Latitude और Longitude अनिवार्य हैं।"}), 400

        pid = database.add_site_geo_point(site_id, point_name, lat, lng, radius)
        return jsonify({
            "success": True,
            "point_id": pid,
            "message": f"✅ GPS पॉइंट '{point_name}' ({lat:.4f}, {lng:.4f} — {radius}m) सफलतापूर्वक जोड़ा गया!"
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/sites/points/<int:point_id>/delete", methods=["POST", "OPTIONS"])
def delete_site_geo_point_api(point_id):
    """Admin / Supervisor: delete a multi-location GPS point."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        point = database.get_site_geo_point(point_id)
        if not point:
            return jsonify({"success": False, "message": "GPS पॉइंट नहीं मिला।"}), 404

        is_owner = session.get("is_owner", False) or (str(pin).strip() == "7808")
        is_supervisor_of_site = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == int(point["site_id"]))
        if not (is_owner or is_supervisor_of_site):
            return jsonify({"success": False, "message": "❌ केवल अधिकृत सुपरवाइज़र या मालिक ही GPS कार्य स्थल हटा सकते हैं।"}), 403

        database.delete_site_geo_point(point_id)
        return jsonify({"success": True, "message": "GPS पॉइंट हटा दिया गया।"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

