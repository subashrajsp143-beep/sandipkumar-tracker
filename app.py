# -*- coding: utf-8 -*-
"""
Main Flask Web Application for Multi-Site Material Consumption Tracker.
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, send_from_directory, session, make_response
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
    user_site_id = session.get("site_id", None)
    user_role = session.get("role", "guest")
    # Master owner mode is ONLY active if logged in as head-office owner without being locked to a supervisor site
    is_owner_admin = (session.get("is_owner", False) or user_role == "owner") and not user_site_id
    
    all_sites = database.get_all_sites()
    if user_site_id:
        visible_sites = [s for s in all_sites if s["id"] == int(user_site_id)]
    else:
        visible_sites = all_sites

    open_complaints_count = database.get_open_complaints_count(int(user_site_id) if user_site_id else None)
    return {
        "current_date": (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d"),
        "now_year": (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).year,
        "user_role": user_role,
        "user_name": session.get("worker_name", ""),
        "user_site_id": user_site_id,
        "user_site_name": session.get("site_name", ""),
        "locked_site_id": int(user_site_id) if user_site_id else None,
        "all_sites_list": visible_sites,
        "is_owner": is_owner_admin,
        "is_master_owner": is_owner_admin,
        "open_complaints_count": open_complaints_count
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
                 "/logout", "/manifest.json", "/sw.js", "/api/live-status", "/website", "/download-apk"] or
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
        if worker_role in ["Data Entry", "DEO"]:
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
    is_owner = session.get("is_owner", False)
    if role == "worker":
        return redirect(url_for("my_attendance_portal"))
    elif role == "supervisor":
        return redirect(url_for("site_stock"))
    elif role == "owner" or is_owner:
        return redirect(url_for("dashboard"))
    
    sites = database.get_all_sites()
    resp = make_response(render_template("login.html", sites=sites))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

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
            return jsonify({"success": False, "message": "Site and Name are required."}), 400

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

# 0.4 Supervisor Login API (Strict Authorization & Site Isolation)
@app.route("/api/auth/supervisor-login", methods=["POST", "OPTIONS"])
def api_supervisor_login():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        site_id = int(data.get("site_id", 0))
        role = data.get("role", "Supervisor").strip()
        name = data.get("name", "").strip()
        phone = str(data.get("phone", "")).strip()

        if not site_id:
            return jsonify({"success": False, "message": "Please select a work site."}), 400

        site = database.get_site_by_id(site_id)
        if not site:
            return jsonify({"success": False, "message": "Selected site does not exist."}), 404

        def _clean_ph(p):
            if not p:
                return ""
            d = re.sub(r"\D", "", str(p))
            return d[-10:] if len(d) >= 10 else d

        norm_phone = _clean_ph(phone)

        # Allow Sandip@@12 as phone override if entered
        if phone == "Sandip@@12":
            norm_phone = "9835180075"

        if not norm_phone or len(norm_phone) != 10:
            return jsonify({
                "success": False, 
                "message": "Please enter a valid 10-digit registered mobile number."
            }), 400

        official_name = name
        official_role = role
        is_authorized = False

        # Master phone number 9835180075 can login to EVERY site as supervisor
        if norm_phone == "9835180075":
            is_authorized = True
            official_name = "Sandip Kumar"
            official_role = "Supervisor"
            norm_phone = "9835180075"
        else:
            # Match against site's registered supervisor and incharge
            site_sup_phone = _clean_ph(site.get("contact"))
            site_inc_phone = _clean_ph(site.get("incharge_phone"))

            if site_sup_phone and norm_phone == site_sup_phone:
                is_authorized = True
                official_name = site.get("supervisor") or name or "Supervisor"
                official_role = "Supervisor"
            elif site_inc_phone and norm_phone == site_inc_phone:
                is_authorized = True
                official_name = site.get("incharge") or name or "Site Incharge"
                official_role = "Site Incharge"
            else:
                # Check if registered DEO (Data Entry Operator) in site_workers
                workers = database.get_all_workers_for_site(site_id)
                for w in workers:
                    if w.get("role") in ["DEO", "Data Entry"] and _clean_ph(w.get("phone")) == norm_phone and w.get("is_active", 1):
                        is_authorized = True
                        official_name = w.get("name") or name
                        official_role = w.get("role") or role
                        break

            if not is_authorized:
                return jsonify({
                    "success": False,
                    "message": "Not an authorized person"
                }), 403

        # Create or fetch worker record with verified official name and role
        worker = database.get_or_create_worker(site_id, official_name, official_role, norm_phone)
        session.permanent = True
        session["role"] = "supervisor"
        session["is_owner"] = False
        session["worker_id"] = worker["id"]
        session["worker_token"] = worker["worker_token"]
        session["worker_name"] = official_name
        session["worker_role"] = official_role
        session["worker_phone"] = norm_phone
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

            try:
                # Silently log supervisor location for Office Work Live Monitor
                database.log_supervisor_silent_ping(
                    site_id=site_id,
                    supervisor_name=official_name,
                    phone=norm_phone,
                    lat=float(lat),
                    lng=float(lng),
                    accuracy=float(data.get("accuracy") or 0),
                    page_source="Supervisor Login"
                )
            except Exception as se:
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

# 0.6 Universal Logout - Instant 1-Click Session & Cookie Annihilation
@app.route("/logout", methods=["GET", "POST"])
def logout_user():
    session.clear()
    session.permanent = False
    
    resp = redirect(url_for("login_page"))
    # Explicitly expire session cookies across root path
    cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
    resp.delete_cookie(cookie_name, path="/")
    resp.delete_cookie("session", path="/")
    resp.delete_cookie("remember_token", path="/")
    
    # Strict anti-cache headers so browser never serves stale redirect/page
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0, post-check=0, pre-check=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers["Clear-Site-Data"] = '"cache", "cookies"'
    return resp

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
    outgoing_letters = database.get_outgoing_letters()
    next_letter_info = database.get_next_letter_ref_no()
    letter_fys = database.get_distinct_letter_fys()
    letters_stats = database.get_outgoing_letters_stats()

    supervisors_tracking = database.get_supervisors_live_tracking_today()

    return render_template(
        "dashboard.html",
        stats=stats,
        sites=sites,
        outgoing_letters=outgoing_letters,
        next_letter_info=next_letter_info,
        letter_fys=letter_fys,
        letters_stats=letters_stats,
        supervisors_tracking=supervisors_tracking
    )

@app.route("/letters")
def letters_shortcut():
    return redirect("/dashboard#letters")


# 1.05 Outgoing Letters Reference Register APIs & Exporters
@app.route("/api/letters", methods=["GET", "POST"])
def api_letters():
    if request.method == "GET":
        fy = request.args.get("fy")
        search = request.args.get("search")
        letters = database.get_outgoing_letters(search=search, fy=fy)
        next_info = database.get_next_letter_ref_no()
        fys = database.get_distinct_letter_fys()
        stats = database.get_outgoing_letters_stats()
        return jsonify({
            "success": True,
            "letters": letters,
            "next_ref_no": next_info["ref_no"],
            "next_seq": next_info["seq_num"],
            "current_fy": next_info["fy"],
            "fys": fys,
            "stats": stats
        })

    # POST: create new letter reference
    try:
        data = request.get_json(silent=True) or request.form
        letter_date = data.get("letter_date") or None
        department = data.get("department") or ""
        place = data.get("place") or ""
        purpose = data.get("purpose") or ""
        remarks = data.get("remarks") or ""
        custom_ref_no = data.get("ref_no") or None

        if not department.strip():
            return jsonify({"success": False, "message": "Department Name is required."}), 400
        if not place.strip():
            return jsonify({"success": False, "message": "Place / Site is required."}), 400
        if not purpose.strip():
            return jsonify({"success": False, "message": "Purpose / Subject is required."}), 400

        res = database.add_outgoing_letter(
            letter_date=letter_date,
            department=department,
            place=place,
            purpose=purpose,
            remarks=remarks,
            custom_ref_no=custom_ref_no
        )
        return jsonify({
            "success": True,
            "message": f"Letter reference no. {res['ref_no']} recorded successfully.",
            "letter": res
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/letters/<int:letter_id>", methods=["GET", "POST", "PUT", "DELETE"])
def api_letter_detail(letter_id):
    if request.method == "GET":
        letter = database.get_outgoing_letter_by_id(letter_id)
        if not letter:
            return jsonify({"success": False, "message": "Letter record not found."}), 404
        return jsonify({"success": True, "letter": letter})

    if request.method == "DELETE":
        ok = database.delete_outgoing_letter(letter_id)
        if ok:
            return jsonify({"success": True, "message": "Letter record deleted successfully."})
        return jsonify({"success": False, "message": "Failed to delete letter or record does not exist."}), 400

    # POST or PUT: update letter
    try:
        data = request.get_json(silent=True) or request.form
        letter_date = data.get("letter_date")
        department = data.get("department")
        place = data.get("place")
        purpose = data.get("purpose")
        remarks = data.get("remarks", "")
        ref_no = data.get("ref_no")

        if not department or not place or not purpose:
            return jsonify({"success": False, "message": "Department, Place, and Subject are required."}), 400

        ok = database.update_outgoing_letter(
            letter_id=letter_id,
            letter_date=letter_date,
            department=department,
            place=place,
            purpose=purpose,
            remarks=remarks,
            ref_no=ref_no
        )
        if ok:
            return jsonify({"success": True, "message": "Letter record updated successfully."})
        return jsonify({"success": False, "message": "Update failed."}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/export/letters-excel")
def export_letters_excel():
    fy = request.args.get("fy")
    search = request.args.get("search")
    letters = database.get_outgoing_letters(search=search, fy=fy)
    wb_buf = exporter.generate_letters_excel(letters, fy=fy)
    clean_fy = (fy or database.compute_financial_year()).replace("/", "_")
    filename = f"Outgoing_Letters_Register_SK_{clean_fy}.xlsx"
    return send_file(
        wb_buf,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename
    )


@app.route("/export/letters-pdf")
def export_letters_pdf():
    fy = request.args.get("fy")
    search = request.args.get("search")
    letters = database.get_outgoing_letters(search=search, fy=fy)
    pdf_buf = exporter.generate_letters_pdf(letters, fy=fy)
    clean_fy = (fy or database.compute_financial_year()).replace("/", "_")
    filename = f"Outgoing_Letters_Register_SK_{clean_fy}.pdf"
    return send_file(
        pdf_buf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename
    )

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
    is_owner = session.get("is_owner", False) or session.get("role") == "owner"
    user_site_id = session.get("site_id")
    sites = database.get_all_sites()
    locked_site = None
    if not is_owner and user_site_id:
        user_site_id = int(user_site_id)
        locked_site = database.get_site_by_id(user_site_id)
        sites = [s for s in sites if s["id"] == user_site_id]
        site_sent = database.get_materials_sent_to_site(user_site_id)
        if site_sent and len(site_sent) > 0:
            materials = site_sent
        else:
            materials = database.get_all_materials()
    else:
        materials = database.get_all_materials()

    if not is_owner:
        # Strict Price Shield: Zero out rates so they never leak to supervisors/DEO via JSON or DOM
        sanitized_materials = []
        for m in materials:
            mc = dict(m)
            mc["rate"] = 0
            sanitized_materials.append(mc)
        materials = sanitized_materials

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    return render_template(
        "daily_entry.html", 
        sites=sites, 
        materials=materials, 
        today=today_str,
        locked_site_id=user_site_id if not is_owner else None,
        locked_site=locked_site,
        is_owner=is_owner
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
        is_owner = session.get("is_owner", False) or session.get("role") == "owner"
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id:
            if site_id != int(user_site_id):
                return jsonify({"success": False, "message": "❌ Security Restriction: You can only record usage for your authorized site."}), 403

        added_count = 0
        for item in items:
            mat_id = int(item["material_id"])
            qty = float(item["quantity"])
            rate = float(item.get("rate", 0))
            item_remarks = item.get("remarks", "")

            # Auto-fill standard rate from DB for supervisors / non-owners to maintain accurate financial ledgers
            if not is_owner or rate <= 0:
                mat_info = database.get_material_by_id(mat_id)
                if mat_info and mat_info.get("rate"):
                    rate = float(mat_info["rate"])

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

        # Optional: Save DPR (Daily Progress Report) if provided in the voucher
        dpr_data = data.get("dpr")
        if dpr_data and isinstance(dpr_data, dict):
            pipe_len = float(dpr_data.get("pipe_laying_meters", 0) or 0)
            fhtc_cnt = int(dpr_data.get("fhtc_connections", 0) or 0)
            boring_d = float(dpr_data.get("boring_depth_feet", 0) or 0)
            road_res = float(dpr_data.get("road_restoration_meters", 0) or 0)
            ward_n = str(dpr_data.get("ward_no", "")).strip()
            desc = str(dpr_data.get("work_description", "")).strip() or purpose
            if pipe_len > 0 or fhtc_cnt > 0 or boring_d > 0 or road_res > 0 or ward_n or desc:
                database.save_dpr(
                    site_id=site_id,
                    report_date=usage_date,
                    ward_no=ward_n,
                    pipe_laying_meters=pipe_len,
                    fhtc_connections=fhtc_cnt,
                    boring_depth_feet=boring_d,
                    road_restoration_meters=road_res,
                    civil_stage=str(dpr_data.get("civil_stage", "")).strip(),
                    work_description=desc,
                    supervisor_name=entered_by,
                    supervisor_phone=session.get("worker_phone", "")
                )

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
        is_owner_auth = (session.get("is_owner", False) or session.get("role") == "owner" or session.get("worker_phone") == "9835180075" or (pin and str(pin).strip() in ["Sandip@@12"]))
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ Incorrect Password! Only authorized owner can delete entries."}), 403

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
    is_owner = (session.get("is_owner", False) or session.get("role") == "owner" or session.get("worker_phone") == "9835180075")
    if not is_owner:
        return jsonify({"success": False, "message": "❌ Security Restriction: Only authorized owner can download backup."}), 403
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
    is_owner = session.get("is_owner", False) or session.get("role") == "owner"
    user_site_id = session.get("site_id")

    # If owner passed a site_id query param to preview a site's store
    site_filter_id = request.args.get("site_id")

    sites = database.get_all_sites()
    locked_site = None

    if not is_owner:
        # Supervisors ONLY see materials dispatched to their assigned site by the Owner
        if user_site_id:
            user_site_id = int(user_site_id)
            locked_site = database.get_site_by_id(user_site_id)
            sites = [s for s in sites if s["id"] == user_site_id]
            materials = database.get_materials_sent_to_site(user_site_id)
        else:
            sites = []
            materials = []

        # Strict Price Shield: Zero out rates so they never leak to supervisors
        sanitized_materials = []
        for m in materials:
            mc = dict(m)
            mc["rate"] = 0
            sanitized_materials.append(mc)
        materials = sanitized_materials
    elif is_owner and site_filter_id:
        # Owner can filter by a specific site to see what was dispatched to that site
        try:
            site_filter_id = int(site_filter_id)
            locked_site = database.get_site_by_id(site_filter_id)
            materials = database.get_materials_sent_to_site(site_filter_id)
        except Exception:
            materials = database.get_all_materials()
    else:
        # Owner full view: 270+ catalog items
        materials = database.get_all_materials()

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    categories = sorted(list(set(m["category"] for m in materials if m.get("category"))))
    return render_template(
        "store.html", 
        sites=sites, 
        materials=materials, 
        categories=categories, 
        today=today_str,
        locked_site_id=user_site_id if not is_owner else (site_filter_id if site_filter_id else None),
        locked_site=locked_site,
        is_owner=is_owner,
        site_filter_id=site_filter_id
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
    is_owner = session.get("is_owner", False) or session.get("role") == "owner"
    user_site_id = session.get("site_id")

    all_sites = database.get_all_sites()
    if not is_owner and user_site_id:
        sites = [s for s in all_sites if s["id"] == int(user_site_id)]
    else:
        sites = all_sites

    points_counts = database.get_geo_points_counts_by_site()
    return render_template("sites.html", sites=sites, points_counts=points_counts, is_supervisor_view=(not is_owner))

@app.route("/api/sites/<int:site_id>/edit", methods=["POST"])
def edit_site(site_id):
    is_owner = session.get("is_owner", False)
    if not is_owner:
        return jsonify({"success": False, "message": "❌ Security Restriction: Only authorized owner can modify site details."}), 403
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
        pin = data.get("pin", "").strip()
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
            flash("❌ Only authorized owner can add new sites.", "error")
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
        flash("❌ Only authorized owner can delete sites.", "error")
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
    is_owner = session.get("is_owner", False) or session.get("role") == "owner"
    if not is_owner:
        flash("❌ Rate Master is authorized for Owner only.", "error")
        return redirect(url_for("site_stock"))

    materials = database.get_all_materials()
    return render_template("materials.html", materials=materials)

@app.route("/api/materials", methods=["POST"])
def add_material():
    is_owner = session.get("is_owner", False)
    if not is_owner:
        flash("❌ Only authorized owner can add materials.", "error")
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

@app.route("/download-apk")
def download_apk():
    """Serves or redirects to the latest released Android APK."""
    local_apk = os.path.join(os.path.dirname(__file__), "SandipKumarTracker.apk")
    if os.path.exists(local_apk) and os.path.getsize(local_apk) > 1000000:
        return send_file(local_apk, as_attachment=True, download_name="SandipKumarTracker.apk", mimetype="application/vnd.android.package-archive")
    return redirect("https://github.com/subashrajsp143-beep/sandipkumar-tracker/releases/download/v1.0-apk/SandipKumarTracker.apk")


@app.route("/api/app-version")
def app_version():
    """Returns the latest available Android APK version and release metadata."""
    return jsonify({
        "status": "ok",
        "version_code": 7,
        "version_name": "1.6.0",
        "apk_url": "https://github.com/subashrajsp143-beep/sandipkumar-tracker/releases/download/v1.0-apk/SandipKumarTracker.apk",
        "changelog": "New logo (JJM Water Shield) + ultra-clean mobile dashboard and attendance",
        "release_date": "2026-10-25"
    })


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
# OFFICE WORK (Sandip@@12) AUTHENTICATION
# ==========================================
@app.route("/api/owner/login", methods=["POST", "OPTIONS"])
def owner_login_api():
    if request.method == "OPTIONS":
        return "", 200
    data = request.get_json(silent=True) or {}
    pin = str(data.get("pin", "")).strip()
    if pin in ["Sandip@@12"]:
        session.permanent = True
        session["is_owner"] = True
        session["role"] = "owner"
        session["worker_name"] = "Sandip Kumar"
        return jsonify({"success": True, "is_owner": True, "role": "owner", "message": "🏢 Office Work Active!"})
    return jsonify({"success": False, "is_owner": False, "message": "❌ Incorrect password! Please enter correct Office Work password."}), 401

@app.route("/api/owner/logout", methods=["POST", "GET"])
def owner_logout_api():
    session.clear()
    session.permanent = False
    resp = jsonify({"success": True, "is_owner": False, "message": "Office Work mode ended."})
    resp.delete_cookie(app.config.get("SESSION_COOKIE_NAME", "session"), path="/")
    resp.delete_cookie("session", path="/")
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers["Clear-Site-Data"] = '"cache", "cookies"'
    return resp

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

    # Manual Attendance View: Preserves manual entries.
    # Note: GPS auto-sync only runs when user explicitly clicks 'GPS Auto-Sync' button.

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

    # Fetch workers & sites for quick photo punch & quick add
    all_sites = database.get_all_sites()
    if is_supervisor_view and user_site_id:
        site_workers = database.get_all_workers_for_site(user_site_id)
        sites = [s for s in all_sites if s["id"] == user_site_id]
    else:
        site_workers = database.get_all_workers()
        sites = all_sites

    # Fetch verified photo attendances for today to show live photo feed on this page
    today_geo_rows, _ = database.get_geo_attendance_today(selected_date)
    if is_supervisor_view and user_site_id:
        today_geo_rows = [r for r in today_geo_rows if r["site_id"] == user_site_id]
    today_photos = [r for r in today_geo_rows if r.get("photo_url")]

    return render_template(
        "attendance.html",
        selected_date=selected_date,
        formatted_date=formatted_date,
        rows=rows,
        totals=totals,
        is_supervisor_view=is_supervisor_view,
        locked_site=locked_site,
        site_workers=site_workers,
        sites=sites,
        today_photos=today_photos
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
            return jsonify({"success": False, "message": "Date is required."}), 400

        # Security check: If not owner, only allow saving attendance for supervisor's site
        is_owner = session.get("is_owner", False)
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id:
            rows = [r for r in rows if int(r.get("site_id", 0)) == int(user_site_id)]

        database.save_daily_manpower(att_date, rows, updated_by=session.get("worker_name", "Web User"))
        return jsonify({"success": True, "message": f"{att_date} attendance saved successfully!"})
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
            "message": f"✅ Auto-synced attendance for {res['total_workers']} worker(s) across 21 sites!"
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
                return jsonify({"success": False, "message": "Please select a site"}), 400
            
            # SECURITY RESTRICTION: Non-owners can only upload photos for their own assigned site
            if not is_owner and user_site_id:
                if int(site_id_raw) != int(user_site_id):
                    return jsonify({"success": False, "message": "❌ Security Restriction: You can only upload photos for your authorized site."}), 403

            site = database.get_site_by_id(int(site_id_raw))
            if not site:
                return jsonify({"success": False, "message": "Invalid site"}), 400

            file = request.files.get("photo")
            if not file or file.filename == "":
                return jsonify({"success": False, "message": "Please capture/select work photo"}), 400

            category = request.form.get("category") or "General Work"
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
                "message": f"✅ {site['name']} photo saved successfully!",
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
                return jsonify({"success": False, "message": "❌ Security Restriction: You can only delete photos for your authorized site."}), 403

        url = database.delete_site_work_photo(photo_id)
        if url and url.startswith("/static/"):
            disk_path = url.lstrip("/")
            if os.path.exists(disk_path):
                try:
                    os.remove(disk_path)
                except Exception:
                    pass
        return jsonify({"success": True, "message": "Photo deleted successfully"})
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
    user_site_id = session.get("site_id")
    user_role = session.get("role")
    is_owner_admin = (session.get("is_owner", False) or user_role == "owner") and not user_site_id

    # STRICT SITE LOCK: Anyone bound to a site (supervisor) can ONLY see their assigned site!
    if user_site_id:
        selected_site_id = int(user_site_id)
        locked_site_id = int(user_site_id)
        selected_site = database.get_site_by_id(selected_site_id)
        sites = [selected_site] if selected_site else []
    elif is_owner_admin:
        site_id_arg = request.args.get("site_id")
        selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None
        locked_site_id = None
        sites = database.get_all_sites()
        selected_site = database.get_site_by_id(selected_site_id) if selected_site_id else None
    else:
        return redirect(url_for("login_page"))

    materials = database.get_all_materials()
    if not is_owner_admin:
        sanitized_materials = []
        for m in materials:
            mc = dict(m)
            mc["rate"] = 0
            sanitized_materials.append(mc)
        materials = sanitized_materials

    stock_rows = database.get_site_stock_inventory(site_id=selected_site_id)
    all_overview = database.get_all_sites_stock_overview()
    overview = [o for o in all_overview if o["id"] == int(user_site_id)] if user_site_id else all_overview

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
        locked_site_id=locked_site_id,
        total_inward_sum=total_inward_sum,
        total_consumed_sum=total_consumed_sum,
        balance_sum=balance_sum,
        low_stock_count=low_stock_count,
        is_master_owner=is_owner_admin,
        today=datetime.date.today().strftime("%Y-%m-%d")
    )

@app.route("/api/stock/inward", methods=["POST", "OPTIONS"])
def save_stock_inward():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        # Require Owner PIN or logged-in Master Owner
        pin = request.args.get("pin") or data.get("pin") or request.headers.get("X-Admin-PIN")
        is_master_owner = (session.get("is_owner", False) or 
                           session.get("role") == "owner" or 
                           session.get("worker_phone") == "9835180075")

        # STRICT PIN ENFORCEMENT: If not master owner, strictly verify PIN is Sandip@@12
        if not is_master_owner:
            if not pin or str(pin).strip() != "Sandip@@12":
                return jsonify({
                    "success": False, 
                    "message": "❌ Incorrect Password! Only authorized owner with valid password can dispatch stock."
                }), 403

        site_id = data.get("site_id")
        # SECURITY RESTRICTION: Non-master supervisors can only add stock to their own assigned site
        user_site_id = session.get("site_id")
        if not is_master_owner and user_site_id:
            if int(site_id) != int(user_site_id):
                return jsonify({"success": False, "message": "❌ Security Restriction: You can only record materials for your authorized site."}), 403

        inward_date = data.get("inward_date") or datetime.date.today().strftime("%Y-%m-%d")
        challan_no = data.get("challan_no", "")
        supplier = data.get("supplier", "Owner / Head Office")
        remarks = data.get("remarks", "")
        items = data.get("items", [])

        if not site_id or not items:
            return jsonify({"success": False, "message": "Site and materials are required."}), 400

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
            "message": f"Inward entry for {added_count} material(s) recorded successfully!",
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
        is_owner_auth = (session.get("is_owner", False) or session.get("role") == "owner" or session.get("worker_phone") == "9835180075" or (pin and str(pin).strip() in ["Sandip@@12"]))
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ Incorrect Password! Only authorized owner can reset stock to 0."}), 403

        site_id = data.get("site_id")
        if site_id:
            site_id = int(site_id)

        database.backup_database()
        database.reset_stock_to_zero(site_id=site_id)

        msg = "All site stock balances have been reset to 0." if not site_id else "Site stock balance has been reset to 0."
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
        is_owner_auth = (session.get("is_owner", False) or session.get("role") == "owner" or session.get("worker_phone") == "9835180075" or (pin and str(pin).strip() in ["Sandip@@12"]))
        if not is_owner_auth:
            return jsonify({"success": False, "message": "❌ Incorrect Password! Only authorized owner can delete inward entries."}), 403

        database.delete_inward_entry(entry_id)
        return jsonify({"success": True, "message": "Inward entry deleted successfully."})
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

    # Group rows by site for display - initialize all sites so any site can be selected and viewed
    by_site = {}
    for s in sites:
        by_site[s["id"]] = {"site_name": s["name"], "site_code": s["code"], "workers": []}
    for r in rows:
        sid = r["site_id"]
        if sid in by_site:
            by_site[sid]["workers"].append(r)
        else:
            by_site[sid] = {"site_name": r["site_name"], "site_code": r["site_code"], "workers": [r]}

    # Summary counts
    total_w = len(rows)
    present_w = sum(1 for r in rows if r.get("att_status") == "present")
    left_w = sum(1 for r in rows if r.get("att_status") == "left")
    absent_w = total_w - present_w - left_w

    points_counts = database.get_geo_points_counts_by_site()
    site_points_map = {s["id"]: database.get_site_geo_points(s["id"]) for s in sites}

    # Silent Supervisor Live Tracking (Only visible to Owner, never to supervisors)
    supervisors_tracking = []
    if is_owner or session.get("role") == "owner":
        supervisors_tracking = database.get_supervisors_live_tracking_today(date_str)

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
        site_points_map=site_points_map,
        supervisors_tracking=supervisors_tracking
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

        if result.get("distance_m") == 99999.0 and not result.get("is_on_site") and result.get("nearest_point_name") == "GPS Not Set":
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


@app.route("/api/geo-attendance/photo-checkin", methods=["POST", "OPTIONS"])
def geo_attendance_photo_checkin():
    """
    Supervisor / Worker photo attendance endpoint with GPS stamping.
    Accepts individual or group photo check-in.
    """
    if request.method == "OPTIONS":
        return "", 200
    try:
        is_json = request.is_json
        if is_json:
            data = request.get_json() or {}
            photo_data = data.get("photo") or data.get("photo_base64")
            worker_id_raw = data.get("worker_id")
            worker_ids = data.get("worker_ids")
            site_id = int(data.get("site_id", 0))
            lat = data.get("latitude")
            lng = data.get("longitude")
            accuracy = data.get("accuracy", 0)
            check_type = data.get("check_type", "check_in")
            att_date = data.get("date")
        else:
            photo_file = request.files.get("photo")
            photo_data = photo_file or request.form.get("photo_base64")
            worker_id_raw = request.form.get("worker_id")
            worker_ids_str = request.form.get("worker_ids")
            worker_ids = [int(x.strip()) for x in worker_ids_str.split(",") if x.strip().isdigit()] if worker_ids_str else None
            site_id = int(request.form.get("site_id", 0))
            lat = request.form.get("latitude")
            lng = request.form.get("longitude")
            accuracy = request.form.get("accuracy", 0)
            check_type = request.form.get("check_type", "check_in")
            att_date = request.form.get("date")

        if not photo_data:
            return jsonify({"success": False, "message": "Please capture attendance photo."}), 400

        target_wids = []
        if worker_ids and isinstance(worker_ids, list):
            target_wids = [int(w) for w in worker_ids if w]
        elif worker_id_raw:
            if str(worker_id_raw).isdigit():
                target_wids = [int(worker_id_raw)]
            elif "," in str(worker_id_raw):
                target_wids = [int(x.strip()) for x in str(worker_id_raw).split(",") if x.strip().isdigit()]

        if not target_wids:
            return jsonify({"success": False, "message": "Please select at least 1 worker."}), 400

        is_owner = session.get("is_owner", False) or session.get("role") == "owner"
        user_site_id = session.get("site_id")

        primary_worker = database.get_worker_by_id(target_wids[0]) if target_wids else None
        if not site_id and primary_worker:
            site_id = primary_worker["site_id"]

        if not is_owner and user_site_id and site_id and int(user_site_id) != site_id:
            return jsonify({"success": False, "message": "❌ Security Restriction: You can only record attendance for your own site."}), 403

        site = database.get_site_by_id(site_id) if site_id else None
        site_name = site["name"] if site else (primary_worker["site_name"] if primary_worker else "Site")
        site_code = site["code"] if site else (primary_worker["site_code"] if primary_worker else f"SITE-{site_id}")

        w_name = primary_worker["name"] if primary_worker else "Worker"
        w_role = primary_worker["role"] if primary_worker else "Staff"
        if len(target_wids) > 1:
            w_name = f"{w_name} + {len(target_wids)-1} other worker(s) (Group Photo)"
            w_role = "Team / Group"

        # Process photo with GPS watermark
        photo_url = photo_service.process_and_save_attendance_photo(
            file_storage=photo_data,
            worker_name=w_name,
            worker_role=w_role,
            site_name=site_name,
            site_code=site_code,
            lat=lat,
            lng=lng,
            accuracy=accuracy,
            att_date=att_date,
            check_type=check_type
        )

        results = []
        for wid in target_wids:
            res = database.save_worker_photo_attendance(
                worker_id=wid,
                site_id=site_id,
                lat=lat,
                lng=lng,
                photo_url=photo_url,
                att_date=att_date,
                check_type=check_type
            )
            results.append({"worker_id": wid, **res})

        # Silently record supervisor's live location ping during worker photo attendance
        if lat and lng:
            try:
                sup_name = session.get("worker_name") or (site.get("supervisor") if site else "Supervisor")
                sup_phone = session.get("worker_phone") or (site.get("contact") if site else "")
                database.log_supervisor_silent_ping(
                    site_id=site_id,
                    supervisor_name=sup_name,
                    phone=sup_phone,
                    lat=lat,
                    lng=lng,
                    accuracy=accuracy,
                    page_source=f"Photo Attendance ({check_type})"
                )
            except Exception:
                pass

        action_text = "Check-In" if check_type == 'check_in' else "Check-Out"
        msg = f"✅ Photo attendance ({action_text}) recorded with GPS for {len(target_wids)} worker(s)!"

        return jsonify({
            "success": True,
            "message": msg,
            "photo_url": photo_url,
            "updated_count": len(target_wids),
            "workers": results
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Error recording photo attendance: {str(e)}"}), 500


# ==========================================
# SILENT SUPERVISOR LOCATION TRACKING ROUTES
# ==========================================

@app.route("/api/supervisor/silent-ping", methods=["POST", "OPTIONS"])
def api_supervisor_silent_ping():
    """
    Silent background GPS tracking ping for site supervisors & incharges.
    Fires quietly in the background on any page visit without user interruption.
    """
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        if not data and request.form:
            data = request.form.to_dict()

        site_id = data.get("site_id") or session.get("site_id")
        if not site_id:
            return jsonify({"success": False, "message": "No site"}), 200

        site_id = int(site_id)
        sup_name = data.get("supervisor_name") or session.get("worker_name") or ""
        sup_phone = data.get("phone") or session.get("worker_phone") or ""
        lat = data.get("latitude")
        lng = data.get("longitude")
        acc = data.get("accuracy", 0)
        page = data.get("page", "background")

        if lat and lng:
            res = database.log_supervisor_silent_ping(
                site_id=site_id,
                supervisor_name=sup_name,
                phone=sup_phone,
                lat=lat,
                lng=lng,
                accuracy=acc,
                page_source=page
            )
            return jsonify({"success": True, "data": res})
        return jsonify({"success": False, "message": "No coordinates"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 200


@app.route("/api/supervisor/live-tracking")
@app.route("/api/supervisors/live-tracking")
def api_supervisor_live_tracking():
    """Owner-only API for live supervisor GPS status across all sites."""
    is_owner = session.get("is_owner", False) or session.get("role") == "owner"
    if not is_owner:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    date_str = request.args.get("date")
    data = database.get_supervisors_live_tracking_today(date_str)
    return jsonify({"success": True, "supervisors": data})


@app.route("/api/supervisor/route/<int:site_id>")
def api_supervisor_route(site_id):
    """Owner-only API for viewing today's movement trail for a supervisor."""
    is_owner = session.get("is_owner", False) or session.get("role") == "owner"
    if not is_owner:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    date_str = request.args.get("date")
    data = database.get_supervisor_route_today(site_id, date_str)
    return jsonify({"success": True, "route": data})


@app.route("/api/workers/quick-add", methods=["POST", "OPTIONS"])
def api_worker_quick_add():
    """Quickly register a new worker by name, phone and role (Accessible to Supervisor & Owner)."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or request.form
        site_id = int(data.get("site_id", 0) or session.get("site_id", 0))
        name = str(data.get("name", "")).strip()
        phone = str(data.get("phone", "")).strip()
        role = str(data.get("role", "Helper")).strip()

        if not site_id:
            return jsonify({"success": False, "message": "Please select a site."}), 400
        if not name:
            return jsonify({"success": False, "message": "Worker name is required."}), 400

        is_owner = session.get("is_owner", False) or session.get("role") == "owner"
        user_site_id = session.get("site_id")
        if not is_owner and user_site_id and int(user_site_id) != site_id:
            return jsonify({"success": False, "message": "You can only add workers to your authorized site."}), 403

        worker_id, token = database.add_worker(site_id, name, role, phone)
        site = database.get_site_by_id(site_id)
        return jsonify({
            "success": True,
            "message": f"✅ Worker '{name}' ({role}) added successfully!",
            "worker": {
                "id": worker_id,
                "site_id": site_id,
                "site_name": site["name"] if site else "Site",
                "name": name,
                "phone": phone,
                "role": role,
                "token": token
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Error adding worker: {str(e)}"}), 500


@app.route("/worker/<token>")
def worker_tracking_page(token):
    """Worker's personal GPS tracking page — opened on their phone."""
    worker = database.get_worker_by_token(token)
    if not worker:
        return "<h2 style='font-family:sans-serif;text-align:center;margin-top:40px;color:#c00'>❌ Link invalid hai ya worker inactive hai.<br>Admin se naya link maangein.</h2>", 404
    return render_template("worker_tracking.html", worker=worker)


@app.route("/api/workers", methods=["POST", "OPTIONS"])
def add_worker_api():
    """Add a new worker to a site (Owner or Supervisor of that site)."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        is_owner = (session.get("is_owner", False) or session.get("role") == "owner" or session.get("worker_phone") == "9835180075" or (str(pin).strip() in ["Sandip@@12"])) or session.get("role") == "owner"
        user_site_id = session.get("site_id")
        is_sup = session.get("role") in ["supervisor", "site_incharge"] or (user_site_id and not is_owner)

        if not is_owner and not is_sup:
            return jsonify({"success": False, "message": "❌ Only owner or supervisor can add workers."}), 403

        site_id = int(data.get("site_id", 0))
        if is_sup and not is_owner and user_site_id:
            site_id = int(user_site_id)

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
            "message": f"✅ {name} ({role}) ko successfully add kar diya!"
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
        is_owner = session.get("is_owner", False) or (str(pin).strip() in ["Sandip@@12"])
        if not is_owner:
            return jsonify({"success": False, "message": "❌ Incorrect Password! Only owner can delete workers."}), 403
        database.delete_worker(worker_id)
        return jsonify({"success": True, "message": "Worker hataya gaya."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/attendance/reset-today", methods=["POST", "OPTIONS"])
def reset_today_attendance_api():
    """Owner only: reset attendance records for today (or selected date) for a site or all sites."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        is_owner = (session.get("is_owner", False) or session.get("role") == "owner" or session.get("worker_phone") == "9835180075" or (str(pin).strip() in ["Sandip@@12"]))
        if not is_owner:
            return jsonify({"success": False, "message": "❌ Only authorized owner can reset attendance."}), 403

        ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
        date_str = data.get("date") or ist_now.strftime("%Y-%m-%d")
        site_id = data.get("site_id")
        site_id = int(site_id) if site_id else None

        database.reset_today_attendance(date_str, site_id)
        return jsonify({"success": True, "message": f"✅ Attendance for {date_str} reset successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/workers/reset-all", methods=["POST", "OPTIONS"])
def reset_all_workers_api():
    """Owner only: deactivates all workers for a specific site or all sites."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        pin = data.get("pin", "")
        is_owner = (session.get("is_owner", False) or session.get("role") == "owner" or session.get("worker_phone") == "9835180075" or (str(pin).strip() in ["Sandip@@12"]))
        if not is_owner:
            return jsonify({"success": False, "message": "❌ Only authorized owner can reset workers."}), 403

        site_id = data.get("site_id")
        site_id = int(site_id) if site_id else None

        database.reset_all_workers(site_id)
        return jsonify({"success": True, "message": "✅ Worker list reset successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/attendance/latest-data")
def api_attendance_latest_data():
    """Returns the most recent saved daily manpower attendance rows to pre-fill or restore."""
    date_req = request.args.get("date")
    conn = database.get_db()
    cur = conn.cursor()
    if date_req:
        latest_date = date_req
    else:
        # Prefer the most recent comprehensive register (with total > 5 or multiple sites)
        cur.execute("""
            SELECT att_date, count(*) as c_cnt, sum(total) as s_tot 
            FROM daily_manpower 
            GROUP BY att_date 
            HAVING s_tot > 5 
            ORDER BY att_date DESC LIMIT 1
        """)
        row = cur.fetchone()
        if not row:
            cur.execute("""
                SELECT att_date, count(*) as c_cnt, sum(total) as s_tot 
                FROM daily_manpower 
                GROUP BY att_date 
                HAVING s_tot > 0 
                ORDER BY att_date DESC LIMIT 1
            """)
            row = cur.fetchone()
        if not row:
            conn.close()
            return jsonify({"success": False, "message": "No previous records found"})
        latest_date = row["att_date"]

    rows, totals = database.get_daily_manpower(latest_date)
    conn.close()
    return jsonify({
        "success": True,
        "latest_date": latest_date,
        "rows": rows,
        "totals": totals
    })


@app.route("/api/attendance/auto-checkout", methods=["POST", "GET", "OPTIONS"])
def api_attendance_auto_checkout():
    """Triggers auto-checkout for workers who left work location after 5:00 PM (17:00 IST)."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        date_str = request.args.get("date") or (request.get_json(silent=True) or {}).get("date") or request.form.get("date")
        count = database.auto_checkout_workers_after_5pm(date_str)
        return jsonify({
            "success": True,
            "message": f"Auto-checked out {count} worker(s) outside site after 5:00 PM.",
            "checked_out_count": count
        })
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
        is_owner = session.get("is_owner", False) or (str(pin).strip() in ["Sandip@@12"])
        is_supervisor_of_site = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == site_id)
        if not (is_owner or is_supervisor_of_site):
            return jsonify({"success": False, "message": "❌ Only authorized supervisor or owner can configure GPS."}), 403

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
        is_owner = session.get("is_owner", False) or (str(pin).strip() in ["Sandip@@12"])
        is_supervisor_of_site = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == site_id)
        if not (is_owner or is_supervisor_of_site):
            return jsonify({"success": False, "message": "❌ Only authorized supervisor or owner can add GPS work locations."}), 403

        point_name = data.get("point_name", "").strip()
        lat = float(data.get("latitude", 0))
        lng = float(data.get("longitude", 0))
        radius = int(data.get("radius", 1000))

        if not point_name or not lat or not lng:
            return jsonify({"success": False, "message": "Point Name, Latitude, and Longitude are required."}), 400

        pid = database.add_site_geo_point(site_id, point_name, lat, lng, radius)
        return jsonify({
            "success": True,
            "point_id": pid,
            "message": f"✅ GPS point '{point_name}' ({lat:.4f}, {lng:.4f} — {radius}m) added successfully!"
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
            return jsonify({"success": False, "message": "GPS point not found."}), 404

        is_owner = session.get("is_owner", False) or (str(pin).strip() in ["Sandip@@12"])
        is_supervisor_of_site = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == int(point["site_id"]))
        if not (is_owner or is_supervisor_of_site):
            return jsonify({"success": False, "message": "❌ Only authorized supervisor or owner can remove GPS work locations."}), 403

        database.delete_site_geo_point(point_id)
        return jsonify({"success": True, "message": "GPS point removed successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# 1. DAILY ACTIVE WARDS (SUPERVISOR SELECTION FOR GEOFENCING)
# ==========================================
@app.route("/api/sites/<int:site_id>/active-wards", methods=["GET", "POST", "OPTIONS"])
def site_active_wards_api(site_id):
    """Supervisor / Owner: get or set today's active work wards for a site (1 KM geofence)."""
    if request.method == "OPTIONS":
        return "", 200
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%Y-%m-%d")

    if request.method == "GET":
        date_str = request.args.get("date") or today
        record = database.get_daily_active_wards(site_id, date_str)
        all_points = database.get_site_geo_points(site_id)
        return jsonify({
            "success": True,
            "site_id": site_id,
            "date": date_str,
            "active_wards": record,
            "all_points": all_points
        })

    try:
        data = request.get_json(silent=True) or {}
        work_date = data.get("date") or today
        active_point_ids = str(data.get("active_point_ids", "")).strip() or "all"
        active_ward_names = str(data.get("active_ward_names", "")).strip()

        is_owner = session.get("is_owner", False) or (str(data.get("pin", "")).strip() in ["Sandip@@12"])
        is_supervisor = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == site_id)
        if not (is_owner or is_supervisor):
            return jsonify({"success": False, "message": "❌ Only authorized supervisor or owner can set active ward."}), 403

        updater = session.get("worker_name") or session.get("supervisor_name") or ("Owner" if is_owner else "Supervisor")
        database.set_daily_active_wards(site_id, work_date, active_point_ids, active_ward_names, updater)

        return jsonify({
            "success": True,
            "message": f"✅ Active work location set to '{active_ward_names or 'All Wards'}' for {work_date}! Workers within 1 KM will be marked present.",
            "active_point_ids": active_point_ids,
            "active_ward_names": active_ward_names
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# 2. DPR (DAILY PROGRESS REPORT) ROUTES & APIS
# ==========================================
@app.route("/dpr")
def dpr_dashboard():
    """Jal Jeevan Mission DPR (Daily Progress Report) Dashboard."""
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    selected_date = request.args.get("date") or ist_now.strftime("%Y-%m-%d")
    selected_site = request.args.get("site_id")

    is_owner = session.get("is_owner", False)
    user_site_id = session.get("site_id")
    if not is_owner and user_site_id:
        selected_site = int(user_site_id)

    sites = database.get_all_sites()
    if not is_owner and user_site_id:
        sites = [s for s in sites if s["id"] == int(user_site_id)]

    dpr_list = database.get_dpr_list(site_id=int(selected_site) if selected_site else None, date_from=selected_date, date_to=selected_date)
    stats = database.get_dpr_summary_stats(selected_date)

    return render_template(
        "dpr.html",
        sites=sites,
        dpr_list=dpr_list,
        stats=stats,
        selected_date=selected_date,
        selected_site_id=int(selected_site) if selected_site else None,
        is_owner=is_owner,
        user_site_id=user_site_id
    )


@app.route("/api/dpr", methods=["GET", "POST", "OPTIONS"])
def dpr_api():
    """API for DPR (Daily Progress Report) - Read & Write."""
    if request.method == "OPTIONS":
        return "", 200
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%Y-%m-%d")

    if request.method == "GET":
        site_id = request.args.get("site_id")
        date_str = request.args.get("date") or today
        dpr = database.get_dpr(int(site_id), date_str) if site_id else None
        dpr_list = database.get_dpr_list(site_id=int(site_id) if site_id else None, date_from=date_str, date_to=date_str)
        stats = database.get_dpr_summary_stats(date_str)
        return jsonify({"success": True, "dpr": dpr, "dpr_list": dpr_list, "stats": stats})

    try:
        data = request.get_json(silent=True) or request.form
        site_id = int(data.get("site_id", 0))
        report_date = data.get("report_date") or today

        if not site_id:
            return jsonify({"success": False, "message": "Site ID zaruri hai."}), 400

        is_owner = session.get("is_owner", False) or (str(data.get("pin", "")).strip() in ["Sandip@@12"])
        is_supervisor = (session.get("role") == "supervisor" and int(session.get("site_id", 0)) == site_id)
        if not (is_owner or is_supervisor):
            return jsonify({"success": False, "message": "❌ Only authorized supervisor or owner can submit DPR."}), 403

        supervisor_name = data.get("supervisor_name") or session.get("worker_name") or session.get("supervisor_name") or "Staff"
        supervisor_phone = data.get("supervisor_phone") or session.get("worker_phone") or ""

        database.save_dpr(
            site_id=site_id,
            report_date=report_date,
            ward_no=data.get("ward_no", ""),
            pipe_laying_meters=float(data.get("pipe_laying_meters", 0) or 0),
            fhtc_connections=int(data.get("fhtc_connections", 0) or 0),
            boring_depth_feet=float(data.get("boring_depth_feet", 0) or 0),
            road_restoration_meters=float(data.get("road_restoration_meters", 0) or 0),
            civil_stage=data.get("civil_stage", ""),
            work_description=data.get("work_description", ""),
            supervisor_name=supervisor_name,
            supervisor_phone=supervisor_phone
        )
        return jsonify({"success": True, "message": f"✅ DPR (Daily Progress Report) for {report_date} saved successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)



# ==========================================
# 10. SITE COMPLAINTS & ISSUE REPORTING
# ==========================================
@app.route("/complaints")
def complaints_view():
    user_site_id = session.get("site_id")
    user_role = session.get("role")
    is_owner_admin = (session.get("is_owner", False) or user_role == "owner") and not user_site_id

    # STRICT SITE LOCK: Anyone on a specific site (supervisors) can ONLY see their assigned site!
    if user_site_id:
        selected_site_id = int(user_site_id)
        locked_site_id = int(user_site_id)
        selected_site = database.get_site_by_id(selected_site_id)
        sites = [selected_site] if selected_site else []
    elif is_owner_admin:
        site_id_arg = request.args.get("site_id")
        selected_site_id = int(site_id_arg) if (site_id_arg and site_id_arg.isdigit()) else None
        locked_site_id = None
        sites = database.get_all_sites()
        selected_site = database.get_site_by_id(selected_site_id) if selected_site_id else None
    else:
        return redirect(url_for("login_page"))

    selected_status = request.args.get("status", "all").strip().lower()
    complaints = database.get_site_complaints(site_id=selected_site_id, status=selected_status)

    # Summary metrics (strictly for this site if supervisor)
    total_count = len(complaints)
    open_count = sum(1 for c in complaints if c.get("status") == "open")
    urgent_count = sum(1 for c in complaints if c.get("priority") == "urgent" and c.get("status") == "open")
    resolved_count = sum(1 for c in complaints if c.get("status") == "resolved")

    return render_template(
        "complaints.html",
        complaints=complaints,
        sites=sites,
        selected_site=selected_site,
        selected_site_id=selected_site_id,
        selected_status=selected_status,
        locked_site_id=locked_site_id,
        is_master_owner=is_owner_admin,
        total_count=total_count,
        open_count=open_count,
        urgent_count=urgent_count,
        resolved_count=resolved_count
    )

@app.route("/api/complaints", methods=["POST", "OPTIONS"])
def api_create_complaint():
    """Submit a new site complaint with optional photo upload."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        is_master = (session.get("is_owner", False) or 
                     session.get("role") == "owner" or 
                     session.get("worker_phone") == "9835180075")
        user_site_id = session.get("site_id")

        if request.is_json:
            data = request.get_json(silent=True) or {}
            site_id = int(data.get("site_id", 0) or user_site_id or 0)
            category = data.get("category", "General Issue")
            subject = data.get("subject", "")
            description = data.get("description", "").strip()
            priority = data.get("priority", "normal")
            supervisor_name = data.get("supervisor_name") or session.get("worker_name", "")
            supervisor_phone = data.get("supervisor_phone") or session.get("worker_phone", "")
            photo_url = data.get("photo_url", "")
        else:
            site_id = int(request.form.get("site_id", 0) or user_site_id or 0)
            category = request.form.get("category", "General Issue")
            subject = request.form.get("subject", "")
            description = request.form.get("description", "").strip()
            priority = request.form.get("priority", "normal")
            supervisor_name = request.form.get("supervisor_name") or session.get("worker_name", "")
            supervisor_phone = request.form.get("supervisor_phone") or session.get("worker_phone", "")
            photo_url = ""

            photo_file = request.files.get("photo")
            if photo_file and photo_file.filename:
                import os, uuid
                complaints_dir = os.path.join(UPLOAD_FOLDER, "complaints")
                os.makedirs(complaints_dir, exist_ok=True)
                ext = os.path.splitext(photo_file.filename)[1].lower() or ".jpg"
                filename = f"issue_{site_id}_{uuid.uuid4().hex[:8]}{ext}"
                filepath = os.path.join(complaints_dir, filename)
                photo_file.save(filepath)
                photo_url = f"/uploads/complaints/{filename}"

        # STRICT ENFORCEMENT: If session is bound to a site, force that site_id!
        if user_site_id:
            site_id = int(user_site_id)

        if not site_id:
            return jsonify({"success": False, "message": "Site चुनना अनिवार्य है।"}), 400
        if not description:
            return jsonify({"success": False, "message": "समस्या का विवरण (क्या दिक्कत है) लिखना अनिवार्य है।"}), 400

        site = database.get_site_by_id(site_id)
        site_name = site["name"] if site else f"Site-{site_id}"
        site_code = site.get("code", "") if site else ""
        if not supervisor_name:
            supervisor_name = site.get("supervisor", "") if site else "Supervisor"
        if not supervisor_phone:
            supervisor_phone = site.get("contact", "") if site else ""

        cid = database.add_site_complaint(
            site_id=site_id,
            site_name=site_name,
            supervisor_name=supervisor_name,
            supervisor_phone=supervisor_phone,
            category=category,
            description=description,
            subject=subject,
            photo_url=photo_url,
            priority=priority
        )

        return jsonify({
            "success": True,
            "message": "✅ शिकायत सफलता-पूर्वक दर्ज हो गई! ऑफिस द्वारा जल्द ही संज्ञान लिया जाएगा।",
            "complaint_id": cid
        })
    except Exception as ex:
        return jsonify({"success": False, "message": f"Error: {str(ex)}"}), 500

@app.route("/api/complaints/<int:complaint_id>/resolve", methods=["POST", "OPTIONS"])
def api_resolve_complaint(complaint_id):
    """Mark complaint as resolved with optional resolution remarks."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.get_json(silent=True) or {}
        notes = data.get("notes", "Resolved by Office / Supervisor")
        success = database.update_complaint_status(complaint_id, "resolved", resolution_notes=notes)
        if success:
            return jsonify({"success": True, "message": "✅ समस्या का समाधान (Resolved) दर्ज हो गया!"})
        return jsonify({"success": False, "message": "Complaint not found."}), 404
    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500

@app.route("/api/complaints/<int:complaint_id>", methods=["DELETE", "OPTIONS"])
def api_delete_complaint(complaint_id):
    """Delete complaint entry (Owner only)."""
    if request.method == "OPTIONS":
        return "", 200
    try:
        is_master = (session.get("is_owner", False) or 
                     session.get("role") == "owner" or 
                     session.get("worker_phone") == "9835180075")
        if not is_master:
            return jsonify({"success": False, "message": "❌ Only owner can delete complaints."}), 403

        success = database.delete_complaint(complaint_id)
        if success:
            return jsonify({"success": True, "message": "Complaint removed successfully."})
        return jsonify({"success": False, "message": "Complaint not found."}), 404
    except Exception as ex:
        return jsonify({"success": False, "message": str(ex)}), 500
