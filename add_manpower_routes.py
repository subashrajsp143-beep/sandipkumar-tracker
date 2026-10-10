# -*- coding: utf-8 -*-
"""
Add Attendance / Daily Manpower routes to app.py
"""

def patch_app_routes():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_routes = '''
# ==========================================
# DAILY MANPOWER ATTENDANCE ROUTES
# ==========================================
@app.route("/attendance")
def attendance_view():
    selected_date = request.args.get("date")
    if not selected_date:
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        # Check if today has entries, else default to 2026-10-08 (seeded photo date) or today
        rows_today, totals_today = database.get_daily_manpower(today_str)
        if totals_today["total"] > 0:
            selected_date = today_str
        else:
            rows_sample, totals_sample = database.get_daily_manpower("2026-10-08")
            selected_date = "2026-10-08" if totals_sample["total"] > 0 else today_str

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

@app.route("/api/attendance", methods=["POST", "OPTIONS"])
def save_attendance_api():
    if request.method == "OPTIONS":
        return "", 200
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
    att_date = request.args.get("date") or datetime.date.today().strftime("%Y-%m-%d")
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
'''

    if '@app.route("/attendance")' not in content:
        target = 'if __name__ == "__main__":'
        content = content.replace(target, new_routes + '\n' + target, 1)

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.py updated with attendance routes and excel export!")

if __name__ == '__main__':
    patch_app_routes()
