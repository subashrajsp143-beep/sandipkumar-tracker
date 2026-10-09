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

    conn.commit()
    conn.close()

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


