# -*- coding: utf-8 -*-
"""
Database configuration and queries using SQLite.
"""

import sqlite3
import os
from data_seed import INITIAL_SITES, get_unique_materials

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_tracker.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Sites Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        location TEXT,
        supervisor TEXT,
        contact TEXT,
        status TEXT DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Materials Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        unit TEXT NOT NULL,
        rate REAL DEFAULT 0.0,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Daily Consumption Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_consumption (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        material_id INTEGER NOT NULL,
        usage_date TEXT NOT NULL,
        quantity REAL NOT NULL,
        rate REAL NOT NULL,
        total_amount REAL NOT NULL,
        purpose TEXT,
        entered_by TEXT,
        remarks TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE,
        FOREIGN KEY(material_id) REFERENCES materials(id) ON DELETE RESTRICT
    );
    """)

    # Material Inward / Receipt (Bonus feature for complete inventory)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS material_inward (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        material_id INTEGER NOT NULL,
        inward_date TEXT NOT NULL,
        quantity REAL NOT NULL,
        challan_no TEXT,
        supplier TEXT,
        remarks TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE,
        FOREIGN KEY(material_id) REFERENCES materials(id) ON DELETE RESTRICT
    );
    """)

    # Ensure incharge columns exist
    cursor.execute("PRAGMA table_info(sites)")
    existing_cols = [r[1] for r in cursor.fetchall()]
    if "incharge" not in existing_cols:
        cursor.execute("ALTER TABLE sites ADD COLUMN incharge TEXT")
    if "incharge_phone" not in existing_cols:
        cursor.execute("ALTER TABLE sites ADD COLUMN incharge_phone TEXT")

    # Ensure image_url column exists in materials
    cursor.execute("PRAGMA table_info(materials)")
    mat_cols = [r[1] for r in cursor.fetchall()]
    if "image_url" not in mat_cols:
        cursor.execute("ALTER TABLE materials ADD COLUMN image_url TEXT")

    # Seed Sites if not present
    cursor.execute("SELECT COUNT(*) FROM sites")
    if cursor.fetchone()[0] == 0:
        for s in INITIAL_SITES:
            cursor.execute("""
                INSERT INTO sites (code, name, location, supervisor, contact)
                VALUES (?, ?, ?, ?, ?)
            """, (s["code"], s["name"], s["location"], s["supervisor"], s["contact"]))

    # Seed Materials if not present
    cursor.execute("SELECT COUNT(*) FROM materials")
    if cursor.fetchone()[0] == 0:
        materials = get_unique_materials()
        for m in materials:
            cursor.execute("""
                INSERT INTO materials (name, unit, rate, category)
                VALUES (?, ?, ?, ?)
            """, (m["name"], m["unit"], m["rate"], m["category"]))

    
    # Daily Manpower Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_manpower (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        att_date TEXT NOT NULL,
        site_incharge INTEGER DEFAULT 0,
        supervisor INTEGER DEFAULT 0,
        electrician INTEGER DEFAULT 0,
        gi_mistri INTEGER DEFAULT 0,
        deo INTEGER DEFAULT 0,
        plumber INTEGER DEFAULT 0,
        helper INTEGER DEFAULT 0,
        other INTEGER DEFAULT 0,
        total INTEGER DEFAULT 0,
        remarks TEXT DEFAULT '',
        updated_by TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE,
        UNIQUE(site_id, att_date)
    );
    """)

    conn.commit()
    conn.close()

    # Initialize GPS attendance tables (added in v3.0 update)
    init_gps_tables()

# Helper query functions
def get_all_sites():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites ORDER BY id ASC")
    sites = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sites

def get_site_by_id(site_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sites WHERE id = ?", (site_id,))
    site = cursor.fetchone()
    conn.close()
    return dict(site) if site else None

def get_all_materials():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materials ORDER BY name ASC")
    materials = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return materials

def get_material_by_id(material_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materials WHERE id = ?", (material_id,))
    mat = cursor.fetchone()
    conn.close()
    return dict(mat) if mat else None

def add_consumption_entry(site_id, material_id, usage_date, quantity, rate=None, purpose="", entered_by="", remarks=""):
    conn = get_db()
    cursor = conn.cursor()
    
    if rate is None:
        cursor.execute("SELECT rate FROM materials WHERE id = ?", (material_id,))
        row = cursor.fetchone()
        rate = row[0] if row else 0.0

    total_amount = float(quantity) * float(rate)

    cursor.execute("""
        INSERT INTO daily_consumption (site_id, material_id, usage_date, quantity, rate, total_amount, purpose, entered_by, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (site_id, material_id, usage_date, quantity, rate, total_amount, purpose, entered_by, remarks))
    
    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return entry_id

def delete_consumption_entry(entry_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_consumption WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def update_consumption_entry(entry_id, site_id=None, material_id=None, usage_date=None, quantity=None, rate=None, purpose=None, entered_by=None, remarks=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_consumption WHERE id = ?", (entry_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    new_site_id = site_id if site_id is not None else row["site_id"]
    new_material_id = material_id if material_id is not None else row["material_id"]
    new_date = usage_date if usage_date is not None else row["usage_date"]
    new_qty = float(quantity) if quantity is not None else float(row["quantity"])
    new_rate = float(rate) if rate is not None else float(row["rate"])
    new_total = round(new_qty * new_rate, 2)
    new_purpose = purpose if purpose is not None else row["purpose"]
    new_entered_by = entered_by if entered_by is not None else row["entered_by"]
    new_remarks = remarks if remarks is not None else row["remarks"]

    cursor.execute("""
        UPDATE daily_consumption
        SET site_id = ?, material_id = ?, usage_date = ?, quantity = ?, rate = ?, total_amount = ?, purpose = ?, entered_by = ?, remarks = ?
        WHERE id = ?
    """, (new_site_id, new_material_id, new_date, new_qty, new_rate, new_total, new_purpose, new_entered_by, new_remarks, entry_id))
    conn.commit()
    conn.close()
    return True

def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM sites")
    total_sites = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM materials")
    total_materials = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM daily_consumption")
    row = cursor.fetchone()
    total_logs = row[0]
    total_cost = row[1]

    # Today's logs
    cursor.execute("SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM daily_consumption WHERE usage_date = date('now', 'localtime')")
    today_row = cursor.fetchone()
    today_logs = today_row[0]
    today_cost = today_row[1]

    # Top consumed materials (by frequency or quantity)
    cursor.execute("""
        SELECT m.name, m.unit, SUM(c.quantity) as total_qty, SUM(c.total_amount) as total_val
        FROM daily_consumption c
        JOIN materials m ON c.material_id = m.id
        GROUP BY m.id
        ORDER BY total_qty DESC
        LIMIT 6
    """)
    top_materials = [dict(r) for r in cursor.fetchall()]

    # Recent entries
    cursor.execute("""
        SELECT c.*, s.name as site_name, s.code as site_code, m.name as material_name, m.unit as material_unit
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        JOIN materials m ON c.material_id = m.id
        ORDER BY c.usage_date DESC, c.id DESC
        LIMIT 10
    """)
    recent_entries = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return {
        "total_sites": total_sites,
        "total_materials": total_materials,
        "total_logs": total_logs,
        "total_cost": total_cost,
        "today_logs": today_logs,
        "today_cost": today_cost,
        "top_materials": top_materials,
        "recent_entries": recent_entries
    }

def get_site_report(site_id=None, from_date=None, to_date=None, material_id=None):
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
        SELECT c.*, s.name as site_name, s.code as site_code, s.supervisor as site_supervisor, m.name as material_name, m.unit as material_unit, m.category
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        JOIN materials m ON c.material_id = m.id
        WHERE 1=1
    """
    params = []
    
    if site_id:
        query += " AND c.site_id = ?"
        params.append(site_id)
    if from_date:
        query += " AND c.usage_date >= ?"
        params.append(from_date)
    if to_date:
        query += " AND c.usage_date <= ?"
        params.append(to_date)
    if material_id:
        query += " AND c.material_id = ?"
        params.append(material_id)

    query += " ORDER BY c.usage_date DESC, c.id DESC"
    cursor.execute(query, params)
    entries = [dict(r) for r in cursor.fetchall()]

    # Summary grouped by material
    summary_query = """
        SELECT m.id as material_id, m.name as material_name, m.unit as material_unit, m.category,
               SUM(c.quantity) as total_quantity, 
               AVG(c.rate) as avg_rate,
               SUM(c.total_amount) as total_amount
        FROM daily_consumption c
        JOIN materials m ON c.material_id = m.id
        WHERE 1=1
    """
    summary_params = []
    if site_id:
        summary_query += " AND c.site_id = ?"
        summary_params.append(site_id)
    if from_date:
        summary_query += " AND c.usage_date >= ?"
        summary_params.append(from_date)
    if to_date:
        summary_query += " AND c.usage_date <= ?"
        summary_params.append(to_date)
    if material_id:
        summary_query += " AND c.material_id = ?"
        summary_params.append(material_id)

    summary_query += " GROUP BY m.id ORDER BY total_amount DESC"
    cursor.execute(summary_query, summary_params)
    material_summary = [dict(r) for r in cursor.fetchall()]

    # Attach date-wise logs to each material summary so user can see exact dates & quantities
    logs_by_material = {}
    for e in entries:
        mid = e["material_id"]
        if mid not in logs_by_material:
            logs_by_material[mid] = []
        logs_by_material[mid].append({
            "id": e["id"],
            "date": e["usage_date"],
            "quantity": e["quantity"],
            "rate": e["rate"],
            "total_amount": e["total_amount"],
            "purpose": e["purpose"],
            "entered_by": e["entered_by"]
        })

    for item in material_summary:
        item["date_logs"] = logs_by_material.get(item["material_id"], [])
        item["dates_used"] = sorted(list(set(l["date"] for l in item["date_logs"])), reverse=True)
        item["last_date"] = item["dates_used"][0] if item["dates_used"] else None
        item["dates_count"] = len(item["dates_used"])

    conn.close()
    return entries, material_summary

def get_item_date_timeline(material_id, site_id=None):
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT c.*, s.name as site_name, s.code as site_code, s.supervisor as site_supervisor, 
               s.contact as site_contact, s.incharge as site_incharge, s.incharge_phone as incharge_contact,
               m.name as material_name, m.unit as material_unit, m.rate as master_rate, m.category
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        JOIN materials m ON c.material_id = m.id
        WHERE c.material_id = ?
    """
    params = [material_id]
    if site_id:
        query += " AND c.site_id = ?"
        params.append(site_id)

    query += " ORDER BY c.usage_date DESC, c.id DESC"
    cursor.execute(query, params)
    timeline_logs = [dict(r) for r in cursor.fetchall()]

    grouped_by_date = {}
    total_qty = 0
    total_amount = 0
    for log in timeline_logs:
        d = log["usage_date"]
        if d not in grouped_by_date:
            grouped_by_date[d] = {
                "date": d,
                "day_qty": 0,
                "day_amount": 0,
                "entries": []
            }
        grouped_by_date[d]["day_qty"] += log["quantity"]
        grouped_by_date[d]["day_amount"] += (log["total_amount"] or 0)
        grouped_by_date[d]["entries"].append(log)
        total_qty += log["quantity"]
        total_amount += (log["total_amount"] or 0)

    date_cards = list(grouped_by_date.values())

    conn.close()
    return {
        "timeline_logs": timeline_logs,
        "date_cards": date_cards,
        "total_qty": total_qty,
        "total_amount": total_amount,
        "total_dates_count": len(date_cards),
        "latest_date": date_cards[0]["date"] if date_cards else None,
        "earliest_date": date_cards[-1]["date"] if date_cards else None
    }

def get_daily_report(report_date):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, s.name as site_name, s.code as site_code, m.name as material_name, m.unit as material_unit
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        JOIN materials m ON c.material_id = m.id
        WHERE c.usage_date = ?
        ORDER BY s.id ASC, c.id DESC
    """, (report_date,))
    entries = [dict(r) for r in cursor.fetchall()]

    # Group by site summary
    cursor.execute("""
        SELECT s.id as site_id, s.name as site_name, s.code as site_code,
               COUNT(c.id) as items_count,
               SUM(c.total_amount) as site_total_cost
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        WHERE c.usage_date = ?
        GROUP BY s.id
        ORDER BY s.id ASC
    """, (report_date,))
    site_summaries = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return entries, site_summaries

def get_material_distribution(material_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id as site_id, s.name as site_name, s.code as site_code,
               SUM(c.quantity) as total_quantity,
               SUM(c.total_amount) as total_cost,
               COUNT(c.id) as log_count
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        WHERE c.material_id = ?
        GROUP BY s.id
        ORDER BY total_quantity DESC
    """, (material_id,))
    sites_usage = [dict(r) for r in cursor.fetchall()]

    # Detailed logs
    cursor.execute("""
        SELECT c.*, s.name as site_name, s.code as site_code
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        WHERE c.material_id = ?
        ORDER BY c.usage_date DESC
    """, (material_id,))
    logs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return sites_usage, logs

def get_matrix_data():
    conn = get_db()
    cursor = conn.cursor()

    sites = get_all_sites()
    
    # Top 15 most used materials
    cursor.execute("""
        SELECT m.id, m.name, m.unit, SUM(c.quantity) as total_all_sites
        FROM daily_consumption c
        JOIN materials m ON c.material_id = m.id
        GROUP BY m.id
        ORDER BY total_all_sites DESC
        LIMIT 20
    """)
    top_mats = [dict(r) for r in cursor.fetchall()]

    matrix = {}
    for s in sites:
        matrix[s["id"]] = {}

    if top_mats:
        mat_ids = [m["id"] for m in top_mats]
        placeholders = ",".join("?" * len(mat_ids))
        cursor.execute(f"""
            SELECT site_id, material_id, SUM(quantity) as qty
            FROM daily_consumption
            WHERE material_id IN ({placeholders})
            GROUP BY site_id, material_id
        """, mat_ids)
        for r in cursor.fetchall():
            matrix[r["site_id"]][r["material_id"]] = r["qty"]

    conn.close()
    return sites, top_mats, matrix

def add_site(name, code=None, location="", supervisor="", contact="", incharge="", incharge_phone=""):
    conn = get_db()
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
    new_id = cursor.lastrowid
    conn.close()
    return new_id, code

def update_site(site_id, name, location="", supervisor="", contact="", incharge="", incharge_phone=""):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sites 
        SET name = ?, location = ?, supervisor = ?, contact = ?, incharge = ?, incharge_phone = ?
        WHERE id = ?
    """, (name, location, supervisor, contact, incharge, incharge_phone, site_id))
    conn.commit()
    conn.close()
    return True

def update_material_photo(material_id, image_url):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE materials SET image_url = ? WHERE id = ?", (image_url, material_id))
    conn.commit()
    conn.close()
    return True

def get_monthly_report(year_month=None):
    if not year_month:
        year_month = datetime.date.today().strftime("%Y-%m")
    
    conn = get_db()
    cursor = conn.cursor()

    # Available months list
    cursor.execute("""
        SELECT DISTINCT substr(usage_date, 1, 7) as m
        FROM daily_consumption
        WHERE usage_date IS NOT NULL AND length(usage_date) >= 7
        ORDER BY m DESC
    """)
    available_months = [r[0] for r in cursor.fetchall()]
    if year_month not in available_months and available_months:
        available_months.insert(0, year_month)

    # All entries for this month
    cursor.execute("""
        SELECT c.*, s.name as site_name, s.code as site_code, s.supervisor as site_supervisor,
               m.name as material_name, m.unit as material_unit, m.category
        FROM daily_consumption c
        JOIN sites s ON c.site_id = s.id
        JOIN materials m ON c.material_id = m.id
        WHERE substr(c.usage_date, 1, 7) = ?
        ORDER BY c.usage_date DESC, c.id DESC
    """, (year_month,))
    entries = [dict(r) for r in cursor.fetchall()]

    # 19 Sites monthly summary
    cursor.execute("""
        SELECT s.id as site_id, s.code as site_code, s.name as site_name, s.supervisor as site_supervisor,
               s.contact as site_contact, s.location as site_location,
               COALESCE(COUNT(c.id), 0) as items_count,
               COALESCE(SUM(c.quantity), 0) as total_qty,
               COALESCE(SUM(c.total_amount), 0) as site_total_cost
        FROM sites s
        LEFT JOIN daily_consumption c ON s.id = c.site_id AND substr(c.usage_date, 1, 7) = ?
        GROUP BY s.id
        ORDER BY site_total_cost DESC, s.id ASC
    """, (year_month,))
    site_summaries = [dict(r) for r in cursor.fetchall()]

    # Top materials consumed in month
    cursor.execute("""
        SELECT m.id as material_id, m.name as material_name, m.unit as material_unit, m.category,
               COUNT(c.id) as log_count,
               SUM(c.quantity) as total_quantity,
               SUM(c.total_amount) as total_cost
        FROM daily_consumption c
        JOIN materials m ON c.material_id = m.id
        WHERE substr(c.usage_date, 1, 7) = ?
        GROUP BY m.id
        ORDER BY total_cost DESC
        LIMIT 10
    """, (year_month,))
    top_materials = [dict(r) for r in cursor.fetchall()]

    # Daily trend in this month
    cursor.execute("""
        SELECT c.usage_date,
               COUNT(DISTINCT c.site_id) as active_sites,
               COUNT(c.id) as items_count,
               SUM(c.total_amount) as day_total
        FROM daily_consumption c
        WHERE substr(c.usage_date, 1, 7) = ?
        GROUP BY c.usage_date
        ORDER BY c.usage_date ASC
    """, (year_month,))
    daily_trend = [dict(r) for r in cursor.fetchall()]

    total_month_cost = sum(e["total_amount"] or 0 for e in entries)
    active_sites_count = sum(1 for s in site_summaries if s["site_total_cost"] and s["site_total_cost"] > 0)

    conn.close()

    return {
        "month": year_month,
        "entries": entries,
        "site_summaries": site_summaries,
        "top_materials": top_materials,
        "daily_trend": daily_trend,
        "total_month_cost": total_month_cost,
        "total_items_count": len(entries),
        "active_sites_count": active_sites_count,
        "available_months": available_months
    }




# ==========================================
# DAILY MANPOWER ATTENDANCE FUNCTIONS
# ==========================================

MANPOWER_SITE_ORDER = [
    "Madhubani", "Singhiya", "Sonpur", "Sheohar", "Jhanjharpur",
    "Ekma", "Siwan", "Chhapra", "Andar", "Mairwa",
    "Basantpur", "Hasanpura", "Kati", "Darbhanga", "Maharajganj",
    "Guthani", "Barhariya", "Sahebganj", "Mirganj", "Naubathpur", "Parsa"
]

def get_daily_manpower(att_date):
    """
    Returns manpower rows for all 21 sites for the given date (att_date) in exact photo order.
    Also returns grand totals for all columns.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Query all sites and left join with daily_manpower for this date
    cursor.execute("""
        SELECT s.id as site_id, s.name as site_name, s.code as site_code, s.supervisor as site_supervisor,
               COALESCE(m.site_incharge, 0) as site_incharge,
               COALESCE(m.supervisor, 0) as supervisor,
               COALESCE(m.electrician, 0) as electrician,
               COALESCE(m.gi_mistri, 0) as gi_mistri,
               COALESCE(m.deo, 0) as deo,
               COALESCE(m.plumber, 0) as plumber,
               COALESCE(m.helper, 0) as helper,
               COALESCE(m.other, 0) as other,
               COALESCE(m.total, 0) as total,
               COALESCE(m.remarks, '') as remarks
        FROM sites s
        LEFT JOIN daily_manpower m ON s.id = m.site_id AND m.att_date = ?
    """, (att_date,))
    
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    # Sort according to exact 21 photo order
    order_dict = {name.lower(): idx for idx, name in enumerate(MANPOWER_SITE_ORDER)}
    rows.sort(key=lambda r: order_dict.get(r["site_name"].lower(), 999))

    # Calculate Totals
    totals = {
        "site_incharge": sum(r["site_incharge"] for r in rows),
        "supervisor": sum(r["supervisor"] for r in rows),
        "electrician": sum(r["electrician"] for r in rows),
        "gi_mistri": sum(r["gi_mistri"] for r in rows),
        "deo": sum(r["deo"] for r in rows),
        "plumber": sum(r["plumber"] for r in rows),
        "helper": sum(r["helper"] for r in rows),
        "other": sum(r["other"] for r in rows),
        "total": sum(r["total"] for r in rows),
    }

    return rows, totals

def save_daily_manpower(att_date, rows_data, updated_by=""):
    """
    Upserts daily manpower rows for a date.
    rows_data: list of dicts with site_id, site_incharge, supervisor, etc.
    """
    conn = get_db()
    cursor = conn.cursor()

    for r in rows_data:
        site_id = int(r["site_id"])
        si = int(r.get("site_incharge") or 0)
        sup = int(r.get("supervisor") or 0)
        elec = int(r.get("electrician") or 0)
        gi = int(r.get("gi_mistri") or 0)
        deo = int(r.get("deo") or 0)
        plumb = int(r.get("plumber") or 0)
        help_cnt = int(r.get("helper") or 0)
        oth = int(r.get("other") or 0)
        tot = si + sup + elec + gi + deo + plumb + help_cnt + oth
        remarks = str(r.get("remarks") or "").strip()

        cursor.execute("""
            INSERT INTO daily_manpower 
            (site_id, att_date, site_incharge, supervisor, electrician, gi_mistri, deo, plumber, helper, other, total, remarks, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(site_id, att_date) DO UPDATE SET
                site_incharge = excluded.site_incharge,
                supervisor = excluded.supervisor,
                electrician = excluded.electrician,
                gi_mistri = excluded.gi_mistri,
                deo = excluded.deo,
                plumber = excluded.plumber,
                helper = excluded.helper,
                other = excluded.other,
                total = excluded.total,
                remarks = excluded.remarks,
                updated_by = excluded.updated_by
        """, (site_id, att_date, si, sup, elec, gi, deo, plumb, help_cnt, oth, tot, remarks, updated_by))

    conn.commit()
    conn.close()
    return True


def auto_sync_gps_to_manpower(att_date=None):
    """
    10:30 AM GPS Auto-Analyzer & Attendance Sync:
    Analyzes all GPS attendance pings of workers who checked in within 500m of their site,
    maps their roles (Incharge, Supervisor, Electrician, GI Mistri, DEO, Plumber, Helper, Other),
    and automatically populates/updates the daily_manpower table and 21-sites sheet.
    """
    import datetime as dt
    if not att_date:
        ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        att_date = ist_now.strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()

    # Query all GPS attendances for this date where worker checked in
    cursor.execute("""
        SELECT a.site_id, w.role, COUNT(*) as cnt
        FROM geo_attendance a
        JOIN site_workers w ON a.worker_id = w.id
        WHERE a.att_date = ? AND (a.status IN ('present', 'left') OR a.check_in_time IS NOT NULL)
        GROUP BY a.site_id, w.role
    """, (att_date,))
    rows = [dict(r) for r in cursor.fetchall()]

    # Aggregate counts per site
    site_counts = {}
    for r in rows:
        sid = r["site_id"]
        role = (r["role"] or "").strip().lower()
        cnt = int(r["cnt"])

        if sid not in site_counts:
            site_counts[sid] = {
                "site_incharge": 0, "supervisor": 0, "electrician": 0,
                "gi_mistri": 0, "deo": 0, "plumber": 0, "helper": 0, "other": 0
            }

        if "incharge" in role:
            site_counts[sid]["site_incharge"] += cnt
        elif "supervisor" in role:
            site_counts[sid]["supervisor"] += cnt
        elif "electrician" in role:
            site_counts[sid]["electrician"] += cnt
        elif "mistri" in role or "mason" in role:
            site_counts[sid]["gi_mistri"] += cnt
        elif "deo" in role or "data" in role:
            site_counts[sid]["deo"] += cnt
        elif "plumber" in role:
            site_counts[sid]["plumber"] += cnt
        elif "helper" in role or "labour" in role or "majdoor" in role:
            site_counts[sid]["helper"] += cnt
        else:
            site_counts[sid]["other"] += cnt

    # Now upsert into daily_manpower
    updated_sites = 0
    total_workers_synced = 0
    all_sites = get_all_sites()
    for s in all_sites:
        sid = s["id"]
        if sid in site_counts:
            c = site_counts[sid]
            tot = sum(c.values())
            if tot > 0:
                cursor.execute("""
                    INSERT INTO daily_manpower 
                    (site_id, att_date, site_incharge, supervisor, electrician, gi_mistri, deo, plumber, helper, other, total, remarks, updated_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'GPS Auto-Synced', 'GPS System 10:30')
                    ON CONFLICT(site_id, att_date) DO UPDATE SET
                        site_incharge = excluded.site_incharge,
                        supervisor = excluded.supervisor,
                        electrician = excluded.electrician,
                        gi_mistri = excluded.gi_mistri,
                        deo = excluded.deo,
                        plumber = excluded.plumber,
                        helper = excluded.helper,
                        other = excluded.other,
                        total = excluded.total,
                        remarks = 'GPS Auto-Synced',
                        updated_by = 'GPS System 10:30'
                """, (sid, att_date, c["site_incharge"], c["supervisor"], c["electrician"],
                      c["gi_mistri"], c["deo"], c["plumber"], c["helper"], c["other"], tot))
                updated_sites += 1
                total_workers_synced += tot

    conn.commit()
    conn.close()

    return {
        "att_date": att_date,
        "updated_sites": updated_sites,
        "total_workers": total_workers_synced,
        "site_counts": site_counts
    }


# ==========================================
# SITE STOCK & INVENTORY FUNCTIONS
# ==========================================

def add_inward_entry(site_id, material_id, inward_date, quantity, challan_no="", supplier="", remarks=""):
    """
    Records material dispatch / inward entry received at a specific site.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO material_inward (site_id, material_id, inward_date, quantity, challan_no, supplier, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (int(site_id), int(material_id), inward_date, float(quantity), str(challan_no).strip(), str(supplier).strip(), str(remarks).strip()))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def delete_inward_entry(entry_id):
    """
    Deletes an inward stock entry.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM material_inward WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return True

def get_site_stock_inventory(site_id=None):
    """
    Returns inventory list showing total sent (inward), total used (consumed),
    and current balance stock for materials at the given site (or all sites).
    """
    conn = get_db()
    cursor = conn.cursor()

    where_site_clause = "AND s.id = ?" if site_id else ""
    params = [site_id] if site_id else []

    query = f"""
    SELECT 
        s.id as site_id, s.name as site_name, s.code as site_code, s.supervisor as site_supervisor,
        m.id as material_id, m.name as material_name, m.unit as material_unit, m.rate as material_rate,
        m.category as material_category, m.image_url as material_image,
        COALESCE(i.total_inward, 0) as total_inward,
        COALESCE(c.total_consumed, 0) as total_consumed,
        (COALESCE(i.total_inward, 0) - COALESCE(c.total_consumed, 0)) as balance_stock,
        i.last_inward_date,
        c.last_usage_date,
        COALESCE(i.inward_count, 0) as inward_count,
        COALESCE(c.usage_count, 0) as usage_count
    FROM sites s
    CROSS JOIN materials m
    LEFT JOIN (
        SELECT site_id, material_id, SUM(quantity) as total_inward, MAX(inward_date) as last_inward_date, COUNT(id) as inward_count
        FROM material_inward
        GROUP BY site_id, material_id
    ) i ON s.id = i.site_id AND m.id = i.material_id
    LEFT JOIN (
        SELECT site_id, material_id, SUM(quantity) as total_consumed, MAX(usage_date) as last_usage_date, COUNT(id) as usage_count
        FROM daily_consumption
        GROUP BY site_id, material_id
    ) c ON s.id = c.site_id AND m.id = c.material_id
    WHERE (COALESCE(i.total_inward, 0) > 0 OR COALESCE(c.total_consumed, 0) > 0)
    {where_site_clause}
    ORDER BY s.id ASC, (COALESCE(i.total_inward, 0) - COALESCE(c.total_consumed, 0)) ASC, m.name ASC
    """
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]

    for r in rows:
        bal = r["balance_stock"]
        inw = r["total_inward"]
        cons = r["total_consumed"]
        if inw > 0 and bal <= 0:
            r["status"] = "out_of_stock"
            r["status_label"] = "खत्म (Out of Stock)"
            r["status_color"] = "red"
        elif inw == 0 and cons > 0:
            r["status"] = "untracked_inward"
            r["status_label"] = "बिना इनवर्ड दर्ज खर्च"
            r["status_color"] = "yellow"
        elif inw > 0 and bal <= max(5, inw * 0.15):
            r["status"] = "low_stock"
            r["status_label"] = "कम स्टॉक (Low Stock)"
            r["status_color"] = "amber"
        else:
            r["status"] = "healthy"
            r["status_label"] = "पर्याप्त स्टॉक (In Stock)"
            r["status_color"] = "green"

        if inw > 0:
            r["percent_remaining"] = max(0, min(100, round((bal / inw) * 100, 1)))
        else:
            r["percent_remaining"] = 0

    conn.close()
    return rows

def get_material_stock_ledger(site_id, material_id):
    """
    Returns full chronological ledger of all inward deliveries and daily consumption
    for a single material on a specific site, with running balance at every transaction.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, inward_date as event_date, quantity, challan_no as ref_no, 
               supplier as source_person, remarks, 'INWARD' as event_type, created_at
        FROM material_inward
        WHERE site_id = ? AND material_id = ?
    """, (site_id, material_id))
    inwards = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
        SELECT id, usage_date as event_date, quantity, purpose as ref_no, 
               entered_by as source_person, remarks, 'OUTWARD' as event_type, created_at
        FROM daily_consumption
        WHERE site_id = ? AND material_id = ?
    """, (site_id, material_id))
    consumptions = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, name, code, supervisor, incharge FROM sites WHERE id = ?", (site_id,))
    site_row = cursor.fetchone()
    site_info = dict(site_row) if site_row else {}

    cursor.execute("SELECT id, name, unit, rate, category, image_url FROM materials WHERE id = ?", (material_id,))
    mat_row = cursor.fetchone()
    mat_info = dict(mat_row) if mat_row else {}

    conn.close()

    all_events = []
    for item in inwards:
        all_events.append({
            "id": item["id"],
            "date": item["event_date"],
            "type": "INWARD",
            "type_label": "🟢 भेजा गया (Inward)",
            "qty": item["quantity"],
            "signed_qty": item["quantity"],
            "ref": item["ref_no"] or "चालान / ऑफिस प्रेषण",
            "person": item["source_person"] or "मालिक / हेड ऑफिस",
            "remarks": item["remarks"] or "",
            "created_at": item["created_at"]
        })

    for item in consumptions:
        all_events.append({
            "id": item["id"],
            "date": item["event_date"],
            "type": "OUTWARD",
            "type_label": "🔴 खर्च हुआ (Daily Use)",
            "qty": item["quantity"],
            "signed_qty": -item["quantity"],
            "ref": item["ref_no"] or "दैनिक उपयोग",
            "person": item["source_person"] or site_info.get("supervisor", "सुपरवाइजर"),
            "remarks": item["remarks"] or "",
            "created_at": item["created_at"]
        })

    # Sort chronologically by date ASC, INWARD first on same date, then id ASC
    all_events.sort(key=lambda x: (x["date"], 0 if x["type"] == "INWARD" else 1, x["id"]))

    running_bal = 0.0
    for ev in all_events:
        running_bal += ev["signed_qty"]
        ev["running_balance"] = round(running_bal, 2)

    total_inward = sum(e["qty"] for e in all_events if e["type"] == "INWARD")
    total_consumed = sum(e["qty"] for e in all_events if e["type"] == "OUTWARD")
    balance_stock = round(total_inward - total_consumed, 2)

    return {
        "site": site_info,
        "material": mat_info,
        "total_inward": total_inward,
        "total_consumed": total_consumed,
        "balance_stock": balance_stock,
        "events": all_events
    }

def get_all_sites_stock_overview():
    """
    Returns high-level summary cards and site-wise aggregates.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COALESCE(SUM(i.quantity), 0) as grand_inward_units,
            COALESCE(COUNT(DISTINCT i.site_id), 0) as sites_with_inward
        FROM material_inward i
    """)
    inw_stat = dict(cursor.fetchone())

    cursor.execute("""
        SELECT 
            COALESCE(SUM(c.quantity), 0) as grand_consumed_units,
            COALESCE(COUNT(DISTINCT c.site_id), 0) as sites_with_consumption
        FROM daily_consumption c
    """)
    cons_stat = dict(cursor.fetchone())

    sites = get_all_sites()
    
    # Per site aggregates
    cursor.execute("""
        SELECT 
            s.id as site_id,
            COALESCE(i.site_inward_units, 0) as inward_units,
            COALESCE(c.site_consumed_units, 0) as consumed_units,
            (COALESCE(i.site_inward_units, 0) - COALESCE(c.site_consumed_units, 0)) as balance_units,
            COALESCE(i.inward_items_count, 0) as inward_items_count,
            COALESCE(c.consumed_items_count, 0) as consumed_items_count
        FROM sites s
        LEFT JOIN (
            SELECT site_id, SUM(quantity) as site_inward_units, COUNT(DISTINCT material_id) as inward_items_count
            FROM material_inward
            GROUP BY site_id
        ) i ON s.id = i.site_id
        LEFT JOIN (
            SELECT site_id, SUM(quantity) as site_consumed_units, COUNT(DISTINCT material_id) as consumed_items_count
            FROM daily_consumption
            GROUP BY site_id
        ) c ON s.id = c.site_id
        ORDER BY s.id ASC
    """)
    site_stats_map = {r["site_id"]: dict(r) for r in cursor.fetchall()}
    conn.close()

    site_cards = []
    for s in sites:
        st = site_stats_map.get(s["id"], {
            "inward_units": 0, "consumed_units": 0, "balance_units": 0,
            "inward_items_count": 0, "consumed_items_count": 0
        })
        site_cards.append({
            "id": s["id"],
            "code": s["code"],
            "name": s["name"],
            "location": s.get("location", ""),
            "supervisor": s.get("supervisor", ""),
            "contact": s.get("contact", ""),
            **st
        })

    return {
        "grand_inward_units": round(inw_stat.get("grand_inward_units", 0), 2),
        "grand_consumed_units": round(cons_stat.get("grand_consumed_units", 0), 2),
        "grand_balance_units": round(inw_stat.get("grand_inward_units", 0) - cons_stat.get("grand_consumed_units", 0), 2),
        "sites_with_stock": inw_stat.get("sites_with_inward", 0),
        "site_cards": site_cards
    }


# ==========================================
# GPS ATTENDANCE SYSTEM - DATABASE FUNCTIONS
# ==========================================

def init_gps_tables():
    """
    Creates GPS attendance tables if they don't already exist.
    Called on every app startup via init_db().
    """
    conn = get_db()
    cursor = conn.cursor()

    # 1. Add GPS lat/lng columns to sites table if missing
    cursor.execute("PRAGMA table_info(sites)")
    site_cols = [r[1] for r in cursor.fetchall()]
    if "latitude" not in site_cols:
        cursor.execute("ALTER TABLE sites ADD COLUMN latitude REAL")
    if "longitude" not in site_cols:
        cursor.execute("ALTER TABLE sites ADD COLUMN longitude REAL")
    if "geo_radius" not in site_cols:
        cursor.execute("ALTER TABLE sites ADD COLUMN geo_radius INTEGER DEFAULT 500")

    # 2. Workers table: individual worker profiles per site
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'Helper',
        phone TEXT,
        worker_token TEXT UNIQUE NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
    );
    """)

    # 3. GPS Attendance log: check-in / check-out events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geo_attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL,
        site_id INTEGER NOT NULL,
        att_date TEXT NOT NULL,
        check_in_time TEXT,
        check_out_time TEXT,
        total_minutes INTEGER DEFAULT 0,
        status TEXT DEFAULT 'absent',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(worker_id) REFERENCES site_workers(id) ON DELETE CASCADE,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE,
        UNIQUE(worker_id, att_date)
    );
    """)

    # 4. Live location pings from worker devices
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS worker_location_pings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        distance_meters REAL,
        is_on_site INTEGER DEFAULT 0,
        ping_time TEXT NOT NULL,
        FOREIGN KEY(worker_id) REFERENCES site_workers(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Returns distance in metres between two GPS coordinates.
    Uses Haversine formula.
    """
    import math
    R = 6371000.0  # Earth radius in metres
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def get_worker_by_token(token):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.*, s.name as site_name, s.code as site_code,
               s.latitude as site_lat, s.longitude as site_lng,
               s.geo_radius as site_radius
        FROM site_workers w
        JOIN sites s ON w.site_id = s.id
        WHERE w.worker_token = ? AND w.is_active = 1
    """, (token,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_workers_for_site(site_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.*, s.name as site_name
        FROM site_workers w
        JOIN sites s ON w.site_id = s.id
        WHERE w.site_id = ? AND w.is_active = 1
        ORDER BY w.role, w.name
    """, (site_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_all_workers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.*, s.name as site_name, s.code as site_code
        FROM site_workers w
        JOIN sites s ON w.site_id = s.id
        WHERE w.is_active = 1
        ORDER BY s.name, w.role, w.name
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def add_worker(site_id, name, role, phone=""):
    import uuid
    token = uuid.uuid4().hex
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO site_workers (site_id, name, role, phone, worker_token)
        VALUES (?, ?, ?, ?, ?)
    """, (site_id, name, role, phone, token))
    worker_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return worker_id, token


def get_or_create_worker(site_id, name, role, phone=""):
    """
    Finds existing worker by phone+site or name+site, or creates a new worker profile.
    Saves phone and role.
    """
    import uuid
    conn = get_db()
    cursor = conn.cursor()
    
    worker = None
    if phone:
        cursor.execute("SELECT * FROM site_workers WHERE phone = ? AND site_id = ? AND is_active = 1", (phone, site_id))
        row = cursor.fetchone()
        if row:
            worker = dict(row)

    if not worker:
        cursor.execute("SELECT * FROM site_workers WHERE LOWER(name) = LOWER(?) AND site_id = ? AND is_active = 1", (name.strip(), site_id))
        row = cursor.fetchone()
        if row:
            worker = dict(row)

    if worker:
        # Update phone or role if provided
        cursor.execute("UPDATE site_workers SET phone = ?, role = ? WHERE id = ?", (phone or worker.get("phone", ""), role or worker.get("role", "Helper"), worker["id"]))
        conn.commit()
        cursor.execute("""
            SELECT w.*, s.name as site_name, s.code as site_code, s.latitude as site_lat, s.longitude as site_lng, s.geo_radius as site_radius
            FROM site_workers w
            JOIN sites s ON w.site_id = s.id
            WHERE w.id = ?
        """, (worker["id"],))
        res = dict(cursor.fetchone())
        conn.close()
        return res
    else:
        token = uuid.uuid4().hex
        cursor.execute("""
            INSERT INTO site_workers (site_id, name, role, phone, worker_token)
            VALUES (?, ?, ?, ?, ?)
        """, (site_id, name.strip(), role, phone, token))
        wid = cursor.lastrowid
        conn.commit()
        cursor.execute("""
            SELECT w.*, s.name as site_name, s.code as site_code, s.latitude as site_lat, s.longitude as site_lng, s.geo_radius as site_radius
            FROM site_workers w
            JOIN sites s ON w.site_id = s.id
            WHERE w.id = ?
        """, (wid,))
        res = dict(cursor.fetchone())
        conn.close()
        return res


def get_worker_attendance_history(worker_id, limit=30):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, s.name as site_name
        FROM geo_attendance a
        JOIN sites s ON a.site_id = s.id
        WHERE a.worker_id = ?
        ORDER BY a.att_date DESC
        LIMIT ?
    """, (worker_id, limit))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_worker_today_status(worker_id):
    import datetime as dt
    ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%Y-%m-%d")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM geo_attendance WHERE worker_id = ? AND att_date = ?
    """, (worker_id, today))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_worker(worker_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE site_workers SET is_active = 0 WHERE id = ?", (worker_id,))
    conn.commit()
    conn.close()


def process_location_ping(worker_id, site_id, lat, lng, site_lat, site_lng, radius):
    """
    Called when a worker sends a location ping.
    - Calculates distance from site
    - Marks check-in if within radius and not already checked in today
    - Marks check-out if outside radius and currently checked in
    - Returns dict with status info
    """
    import datetime as dt
    distance = haversine_distance(lat, lng, site_lat, site_lng) if (site_lat and site_lng) else 99999
    is_on_site = distance <= radius

    ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%Y-%m-%d")
    now_str = ist_now.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()

    # Save location ping
    cursor.execute("""
        INSERT INTO worker_location_pings (worker_id, latitude, longitude, distance_meters, is_on_site, ping_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (worker_id, lat, lng, round(distance, 1), 1 if is_on_site else 0, now_str))

    # Fetch or create today's attendance record
    cursor.execute("""
        SELECT * FROM geo_attendance WHERE worker_id = ? AND att_date = ?
    """, (worker_id, today))
    att = cursor.fetchone()
    att = dict(att) if att else None

    action = "ping"
    if not att:
        # No record yet for today
        if is_on_site:
            cursor.execute("""
                INSERT INTO geo_attendance (worker_id, site_id, att_date, check_in_time, status)
                VALUES (?, ?, ?, ?, 'present')
            """, (worker_id, site_id, today, now_str))
            action = "checked_in"
        else:
            cursor.execute("""
                INSERT INTO geo_attendance (worker_id, site_id, att_date, status)
                VALUES (?, ?, ?, 'absent')
            """, (worker_id, site_id, today))
    else:
        # Record exists
        if is_on_site and att["status"] == "absent":
            # Worker arrived – check in
            cursor.execute("""
                UPDATE geo_attendance SET check_in_time = ?, status = 'present'
                WHERE worker_id = ? AND att_date = ?
            """, (now_str, worker_id, today))
            action = "checked_in"
        elif not is_on_site and att["status"] == "present" and att["check_in_time"] and not att["check_out_time"]:
            # Worker left – check out, compute minutes
            try:
                cin = dt.datetime.strptime(att["check_in_time"], "%Y-%m-%d %H:%M:%S")
                minutes = int((ist_now - cin).total_seconds() / 60)
            except Exception:
                minutes = 0
            cursor.execute("""
                UPDATE geo_attendance
                SET check_out_time = ?, total_minutes = ?, status = 'left'
                WHERE worker_id = ? AND att_date = ?
            """, (now_str, minutes, worker_id, today))
            action = "checked_out"

    conn.commit()
    conn.close()

    return {
        "distance_m": round(distance, 1),
        "is_on_site": is_on_site,
        "action": action,
        "timestamp": now_str
    }


def get_geo_attendance_today(date_str=None):
    """
    Returns today's GPS attendance status for all workers across all sites.
    """
    import datetime as dt
    if not date_str:
        ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        date_str = ist_now.strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.id as worker_id, w.name as worker_name, w.role, w.phone, w.worker_token,
               s.id as site_id, s.name as site_name, s.code as site_code,
               a.check_in_time, a.check_out_time, a.total_minutes,
               a.status as att_status,
               p.latitude as last_lat, p.longitude as last_lng,
               p.distance_meters as last_dist, p.ping_time as last_ping,
               p.is_on_site as last_on_site
        FROM site_workers w
        JOIN sites s ON w.site_id = s.id
        LEFT JOIN geo_attendance a ON a.worker_id = w.id AND a.att_date = ?
        LEFT JOIN worker_location_pings p ON p.id = (
            SELECT id FROM worker_location_pings WHERE worker_id = w.id ORDER BY id DESC LIMIT 1
        )
        WHERE w.is_active = 1
        ORDER BY s.name, w.role, w.name
    """, (date_str,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows, date_str


def get_geo_attendance_monthly(site_id, month_str):
    """
    Returns monthly geo-attendance summary for a site.
    month_str format: YYYY-MM
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.id as worker_id, w.name as worker_name, w.role,
               a.att_date, a.check_in_time, a.check_out_time, a.total_minutes, a.status
        FROM site_workers w
        LEFT JOIN geo_attendance a ON a.worker_id = w.id AND a.att_date LIKE ?
        WHERE w.site_id = ? AND w.is_active = 1
        ORDER BY a.att_date, w.role, w.name
    """, (month_str + "%", site_id))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def update_site_gps(site_id, latitude, longitude, radius=500):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sites SET latitude = ?, longitude = ?, geo_radius = ?
        WHERE id = ?
    """, (latitude, longitude, radius, site_id))
    conn.commit()
    conn.close()


def backup_database():
    """
    Creates a timestamped snapshot copy of material_tracker.db in backups directory.
    """
    import shutil, datetime
    backup_dir = os.path.join(os.path.dirname(DB_PATH), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"material_tracker_backup_{ts}.db")
    shutil.copy2(DB_PATH, backup_file)
    return backup_file

def reset_stock_to_zero(site_id=None):
    """
    Resets all item inward quantities and daily consumption logs to 0.
    Does NOT delete materials master or sites list.
    """
    conn = get_db()
    cursor = conn.cursor()
    if site_id:
        cursor.execute("DELETE FROM material_inward WHERE site_id = ?", (site_id,))
        cursor.execute("DELETE FROM daily_consumption WHERE site_id = ?", (site_id,))
    else:
        cursor.execute("DELETE FROM material_inward")
        cursor.execute("DELETE FROM daily_consumption")
    conn.commit()
    conn.close()
    return True


