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

app = Flask(__name__)
app.secret_key = "construction-material-secret-key-19-sites"

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
        "now_year": (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).year
    }

@app.before_request
def ensure_canonical_domain():
    host = request.host.lower()
    if "ms-sandipkumar-tracker.onrender.com" in host:
        url = request.url.replace("ms-sandipkumar-tracker.onrender.com", "sandipkumar-tracker.onrender.com")
        return redirect(url, code=301)

# 24/7 Keep-Alive Background Worker (Prevents Render Free Tier Cold-Start Sleep)
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
        while True:
            for url in target_urls:
                try:
                    req = urllib.request.Request(
                        url,
                        headers={"User-Agent": "SandipTracker-KeepAlive/2.0"}
                    )
                    urllib.request.urlopen(req, timeout=12)
                except Exception:
                    pass
            # Sleep 8 minutes (480 seconds) - keeps Render from sleeping after 15 min idle
            time.sleep(480)

    try:
        import threading
        t = threading.Thread(target=ping_worker, daemon=True)
        t.start()
    except Exception as e:
        print(f"Keep-alive thread notice: {e}")

_start_keep_alive_daemon()

# 0. Official Company Website (Public Home Page)
@app.route("/")
def company_website():
    stats = database.get_dashboard_stats()
    sites = database.get_all_sites()
    materials = database.get_all_materials()
    return render_template("website.html", stats=stats, sites=sites, materials=materials)

# 1. Internal Contractor Portal & Tracker Dashboard
@app.route("/dashboard")
@app.route("/portal")
def dashboard():
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
def daily_entry():
    sites = database.get_all_sites()
    materials = database.get_all_materials()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    return render_template("daily_entry.html", sites=sites, materials=materials, today=today_str)

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
    sites = database.get_all_sites()
    materials = database.get_all_materials()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    categories = sorted(list(set(m["category"] for m in materials if m.get("category"))))
    return render_template("store.html", sites=sites, materials=materials, categories=categories, today=today_str)

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

# 3. Site-wise Report
@app.route("/reports/sites")
def site_report():
    sites = database.get_all_sites()
    materials = database.get_all_materials()
    
    site_id_arg = request.args.get("site_id", type=int)
    from_date = request.args.get("from_date", "")
    to_date = request.args.get("to_date", "")
    mat_id_arg = request.args.get("material_id", type=int)

    # Default to first site if none specified
    selected_site_id = site_id_arg if site_id_arg else (sites[0]["id"] if sites else None)
    
    entries, material_summary = [], []
    selected_site = None
    grand_total = 0.0

    if selected_site_id:
        selected_site = database.get_site_by_id(selected_site_id)
        entries, material_summary = database.get_site_report(
            site_id=selected_site_id,
            from_date=from_date if from_date else None,
            to_date=to_date if to_date else None,
            material_id=mat_id_arg if mat_id_arg else None
        )
        grand_total = sum(item["total_amount"] or 0 for item in material_summary)

    return render_template(
        "site_report.html",
        sites=sites,
        materials=materials,
        selected_site=selected_site,
        selected_site_id=selected_site_id,
        from_date=from_date,
        to_date=to_date,
        selected_mat_id=mat_id_arg,
        entries=entries,
        material_summary=material_summary,
        grand_total=grand_total
    )

# 4. Daily / Date-wise Report
@app.route("/reports/daily")
def daily_report():
    report_date = request.args.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    entries, site_summaries = database.get_daily_report(report_date)
    total_day_cost = sum(s["site_total_cost"] or 0 for s in site_summaries)
    
    return render_template(
        "daily_report.html",
        report_date=report_date,
        entries=entries,
        site_summaries=site_summaries,
        total_day_cost=total_day_cost
    )

# 4.5 Monthly / Mahina-war Report across 19 sites
@app.route("/reports/monthly")
def monthly_report():
    month_arg = request.args.get("month", datetime.date.today().strftime("%Y-%m"))
    report_data = database.get_monthly_report(month_arg)
    return render_template(
        "monthly_report.html",
        month=month_arg,
        entries=report_data["entries"],
        site_summaries=report_data["site_summaries"],
        top_materials=report_data["top_materials"],
        daily_trend=report_data["daily_trend"],
        total_month_cost=report_data["total_month_cost"],
        total_items_count=report_data["total_items_count"],
        active_sites_count=report_data["active_sites_count"],
        available_months=report_data["available_months"]
    )

# 5. Material-wise Report across 19 sites
@app.route("/reports/materials")
def material_report():
    materials = database.get_all_materials()
    mat_id_arg = request.args.get("material_id", type=int)
    selected_mat_id = mat_id_arg if mat_id_arg else (materials[0]["id"] if materials else None)
    
    selected_material = None
    sites_usage, logs = [], []
    total_qty_all_sites = 0
    total_cost_all_sites = 0

    if selected_mat_id:
        selected_material = database.get_material_by_id(selected_mat_id)
        sites_usage, logs = database.get_material_distribution(selected_mat_id)
        total_qty_all_sites = sum(u["total_quantity"] or 0 for u in sites_usage)
        total_cost_all_sites = sum(u["total_cost"] or 0 for u in sites_usage)

    return render_template(
        "material_report.html",
        materials=materials,
        selected_mat_id=selected_mat_id,
        selected_material=selected_material,
        sites_usage=sites_usage,
        logs=logs,
        total_qty=total_qty_all_sites,
        total_cost=total_cost_all_sites
    )

# 5.1 Dedicated Item Date Timeline (Kab Kab Use Hua)
@app.route("/item-history")
def item_history():
    materials = database.get_all_materials()
    sites = database.get_all_sites()
    mat_id_arg = request.args.get("material_id", type=int)
    site_id_arg = request.args.get("site_id", type=int)

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

# 6. Master Matrix (19 Sites vs Top Materials)
@app.route("/reports/matrix")
def matrix_report():
    sites, top_mats, matrix = database.get_matrix_data()
    return render_template("matrix_report.html", sites=sites, top_mats=top_mats, matrix=matrix)

# 7. Excel Exports
@app.route("/export/site-excel")
def export_site_excel():
    site_id = request.args.get("site_id", type=int)
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
    sites = database.get_all_sites()
    return render_template("sites.html", sites=sites)

@app.route("/api/sites/<int:site_id>/edit", methods=["POST"])
def edit_site(site_id):
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
    materials = database.get_all_materials()
    return render_template("materials.html", materials=materials)

@app.route("/api/materials", methods=["POST"])
def add_material():
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
        session["is_owner"] = True
        return jsonify({"success": True, "is_owner": True, "message": "👑 मालिक मोड सक्रिय (Owner Mode Active)!"})
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
        totals=totals
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
        return jsonify({"success": True, "date": att_date, "rows": rows, "totals": totals})
    try:
        data = request.get_json(silent=True) or {}
        att_date = data.get("date")
        rows = data.get("rows", [])
        if not att_date:
            return jsonify({"success": False, "message": "तारीख चुनना अनिवार्य है।"}), 400

        database.save_daily_manpower(att_date, rows, updated_by="Web User")
        return jsonify({"success": True, "message": f"{att_date} की हाजिरी सफलतापूर्वक सेव हो गई!"})
    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500

@app.route("/export/manpower-excel")
def export_manpower_excel():
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    att_date = request.args.get("date") or ist_now.strftime("%Y-%m-%d")
    rows, totals = database.get_daily_manpower(att_date)

    excel_file = exporter.generate_manpower_excel(att_date, rows, totals)
    
    # Format filename: MANPOWER_ATTENDANCE_08_10_2026.xlsx
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

    pdf_file = exporter.generate_manpower_pdf(att_date, rows, totals)
    
    # Format filename: MANPOWER_ATTENDANCE_08_10_2026.pdf
    clean_date = att_date.replace("-", "_")
    filename = f"MANPOWER_ATTENDANCE_{clean_date}.pdf"

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )

# 9. Site Stock & Inventory Register
@app.route("/stock")
def site_stock():
    site_id_arg = request.args.get("site_id")
    selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None
    
    sites = database.get_all_sites()
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
        # Require Owner PIN
        pin = request.args.get("pin") or data.get("pin") or request.headers.get("X-Admin-PIN")
        is_owner_auth = session.get("is_owner", False) or (pin and str(pin).strip() == "7808")
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ गलत पिन! स्टॉक एंट्री (माल भेजना) केवल अधिकृत मालिक ही कर सकते हैं।"}), 403

        site_id = data.get("site_id")
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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

