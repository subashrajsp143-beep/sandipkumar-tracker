# -*- coding: utf-8 -*-
"""
Database configuration and queries using SQLite.
"""

import sqlite3
import os
import time
from functools import wraps
from data_seed import INITIAL_SITES, get_unique_materials

def _notify_cloud_backup():
    try:
        import github_sync
        github_sync.trigger_cloud_backup_async()
    except Exception:
        pass

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_tracker.db")

def db_retry(max_retries=6, delay=0.25):
    """Decorator to retry SQLite operations if the database is busy or locked."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    err_str = str(e).lower()
                    if ("locked" in err_str or "busy" in err_str) and attempt < max_retries - 1:
                        last_err = e
                        time.sleep(delay * (attempt + 1))
                    else:
                        raise
            if last_err:
                raise last_err
        return wrapper
    return decorator

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=60000;")
        conn.execute("PRAGMA synchronous=NORMAL;")
    except Exception:
        pass
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA busy_timeout=60000;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
    except Exception:
        pass

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
    init_photo_tables()

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

def get_materials_sent_to_site(site_id):
    """
    Returns only the materials that have been dispatched (material_inward)
    by the Owner to the specified site, along with total inward count and current balance stock.
    """
    if not site_id:
        return []
    conn = get_db()
    cursor = conn.cursor()
    query = """
    SELECT 
        m.id, m.name, m.unit, m.rate, m.category, m.image_url,
        COALESCE(i.total_inward, 0) as total_inward,
        COALESCE(c.total_consumed, 0) as total_consumed,
        (COALESCE(i.total_inward, 0) - COALESCE(c.total_consumed, 0)) as balance_stock,
        i.last_inward_date
    FROM materials m
    INNER JOIN (
        SELECT material_id, SUM(quantity) as total_inward, MAX(inward_date) as last_inward_date
        FROM material_inward
        WHERE site_id = ?
        GROUP BY material_id
        HAVING SUM(quantity) > 0
    ) i ON m.id = i.material_id
    LEFT JOIN (
        SELECT material_id, SUM(quantity) as total_consumed
        FROM daily_consumption
        WHERE site_id = ?
        GROUP BY material_id
    ) c ON m.id = c.material_id
    ORDER BY m.category ASC, m.name ASC
    """
    cursor.execute(query, (int(site_id), int(site_id)))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

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
    _notify_cloud_backup()
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
        last_active TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
    );
    """)

    # Migration for site_workers: last_active if missing
    cursor.execute("PRAGMA table_info(site_workers)")
    worker_cols = [r[1] for r in cursor.fetchall()]
    if "last_active" not in worker_cols:
        cursor.execute("ALTER TABLE site_workers ADD COLUMN last_active TEXT")

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
        nearest_point_name TEXT,
        ping_time TEXT NOT NULL,
        FOREIGN KEY(worker_id) REFERENCES site_workers(id) ON DELETE CASCADE
    );
    """)

    # Migration for worker_location_pings: nearest_point_name if missing
    cursor.execute("PRAGMA table_info(worker_location_pings)")
    ping_cols = [r[1] for r in cursor.fetchall()]
    if "nearest_point_name" not in ping_cols:
        cursor.execute("ALTER TABLE worker_location_pings ADD COLUMN nearest_point_name TEXT")

    # Migration for geo_attendance: photo_url if missing
    cursor.execute("PRAGMA table_info(geo_attendance)")
    geo_cols = [r[1] for r in cursor.fetchall()]
    if "photo_url" not in geo_cols:
        cursor.execute("ALTER TABLE geo_attendance ADD COLUMN photo_url TEXT")

    # 5. Multi-location sub-points per site (e.g. Siwan 4-5 points: Pump House, Tank, Ward 4 Pipeline, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_geo_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        point_name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        radius_meters INTEGER DEFAULT 300,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
    );
    """)

    # 6. Daily active work wards selected by supervisor for geofencing
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_site_active_wards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        work_date TEXT NOT NULL,
        active_point_ids TEXT NOT NULL,
        active_ward_names TEXT,
        updated_by TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(site_id, work_date)
    );
    """)

    # 7. DPR (Daily Progress Report) - Jal Jeevan Mission physical progress
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_progress_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        report_date TEXT NOT NULL,
        ward_no TEXT,
        pipe_laying_meters REAL DEFAULT 0,
        fhtc_connections INTEGER DEFAULT 0,
        boring_depth_feet REAL DEFAULT 0,
        road_restoration_meters REAL DEFAULT 0,
        civil_stage TEXT,
        work_description TEXT,
        supervisor_name TEXT,
        supervisor_phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE,
        UNIQUE(site_id, report_date)
    );
    """)

    # 8. Silent Supervisor & Site Incharge Location Tracking Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supervisor_location_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        supervisor_name TEXT,
        supervisor_phone TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        accuracy REAL DEFAULT 0,
        distance_meters REAL,
        is_on_site INTEGER DEFAULT 0,
        nearest_point_name TEXT,
        page_source TEXT,
        ping_time TEXT NOT NULL,
        ping_date TEXT NOT NULL,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
    );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sup_logs_site_date ON supervisor_location_logs(site_id, ping_date);")

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


def get_worker_by_id(worker_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.*, s.name as site_name, s.code as site_code,
               s.latitude as site_lat, s.longitude as site_lng,
               s.geo_radius as site_radius
        FROM site_workers w
        JOIN sites s ON w.site_id = s.id
        WHERE w.id = ?
    """, (worker_id,))
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
    _notify_cloud_backup()
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
    _notify_cloud_backup()

def reset_today_attendance(date_str, site_id=None):
    """
    Resets GPS trial attendance records for the given date.
    Clears ONLY geo_attendance (preserves official manual daily_manpower sheet).
    """
    conn = get_db()
    cursor = conn.cursor()
    if site_id:
        cursor.execute("DELETE FROM geo_attendance WHERE att_date = ? AND site_id = ?", (date_str, site_id))
    else:
        cursor.execute("DELETE FROM geo_attendance WHERE att_date = ?", (date_str,))
    conn.commit()
    conn.close()
    return True


def reset_all_workers(site_id=None):
    """
    Deactivates all workers (or all workers of a specific site) by setting is_active = 0.
    """
    conn = get_db()
    cursor = conn.cursor()
    if site_id:
        cursor.execute("UPDATE site_workers SET is_active = 0 WHERE site_id = ?", (site_id,))
    else:
        cursor.execute("UPDATE site_workers SET is_active = 0")
    conn.commit()
    conn.close()
    _notify_cloud_backup()
    return True


# ==========================================
# MULTI-POINT GPS SUB-LOCATIONS (WIDE RADIUS WORK)
# ==========================================

def get_site_geo_points(site_id):
    """
    Returns all sub-location GPS points configured for a site
    (e.g. Siwan 4-5 points: Pump House, Tank, Ward 4 Pipeline, Store, etc.)
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM site_geo_points
        WHERE site_id = ?
        ORDER BY id ASC
    """, (site_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def add_site_geo_point(site_id, point_name, latitude, longitude, radius_meters=1000):
    """
    Adds a new GPS sub-location point for a site with customized geofence radius (default 1 KM / 1000m).
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO site_geo_points (site_id, point_name, latitude, longitude, radius_meters)
        VALUES (?, ?, ?, ?, ?)
    """, (site_id, point_name.strip(), float(latitude), float(longitude), int(radius_meters)))
    pid = cursor.lastrowid
    conn.commit()
    conn.close()
    return pid


def get_site_geo_point(point_id):
    """
    Returns single GPS sub-location point by ID.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM site_geo_points WHERE id = ?", (point_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_site_geo_point(point_id):
    """
    Removes a GPS sub-location point.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM site_geo_points WHERE id = ?", (point_id,))
    conn.commit()
    conn.close()
    return True


def get_geo_points_counts_by_site():
    """
    Returns a dict mapping site_id -> count of configured geo-points.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT site_id, COUNT(*) as cnt
        FROM site_geo_points
        GROUP BY site_id
    """)
    res = {r["site_id"]: r["cnt"] for r in cursor.fetchall()}
    conn.close()
    return res


# ==========================================
# DAILY ACTIVE WARDS SELECTION (SUPERVISOR CONTROL)
# ==========================================

def set_daily_active_wards(site_id, work_date, active_point_ids, active_ward_names="", updated_by="Supervisor"):
    """
    Sets today's active work wards / points for a site.
    active_point_ids: comma-separated string e.g. "1,2" or "all"
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO daily_site_active_wards (site_id, work_date, active_point_ids, active_ward_names, updated_by, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(site_id, work_date) DO UPDATE SET
            active_point_ids = excluded.active_point_ids,
            active_ward_names = excluded.active_ward_names,
            updated_by = excluded.updated_by,
            updated_at = CURRENT_TIMESTAMP
    """, (int(site_id), str(work_date), str(active_point_ids).strip(), str(active_ward_names).strip(), str(updated_by).strip()))
    conn.commit()
    conn.close()
    return True


def get_daily_active_wards(site_id, work_date):
    """
    Returns active ward configuration for a site on a specific date.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM daily_site_active_wards
        WHERE site_id = ? AND work_date = ?
    """, (int(site_id), str(work_date)))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ==========================================
# DAILY PROGRESS REPORT (DPR) - JAL JEEVAN MISSION
# ==========================================

def save_dpr(site_id, report_date, ward_no="", pipe_laying_meters=0.0, fhtc_connections=0,
             boring_depth_feet=0.0, road_restoration_meters=0.0, civil_stage="",
             work_description="", supervisor_name="", supervisor_phone=""):
    """
    Saves or updates daily work progress report (DPR) for a site and date.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO daily_progress_reports (
            site_id, report_date, ward_no, pipe_laying_meters, fhtc_connections,
            boring_depth_feet, road_restoration_meters, civil_stage,
            work_description, supervisor_name, supervisor_phone, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(site_id, report_date) DO UPDATE SET
            ward_no = excluded.ward_no,
            pipe_laying_meters = excluded.pipe_laying_meters,
            fhtc_connections = excluded.fhtc_connections,
            boring_depth_feet = excluded.boring_depth_feet,
            road_restoration_meters = excluded.road_restoration_meters,
            civil_stage = excluded.civil_stage,
            work_description = excluded.work_description,
            supervisor_name = excluded.supervisor_name,
            supervisor_phone = excluded.supervisor_phone,
            updated_at = CURRENT_TIMESTAMP
    """, (
        int(site_id), str(report_date), str(ward_no or "").strip(),
        float(pipe_laying_meters or 0), int(fhtc_connections or 0),
        float(boring_depth_feet or 0), float(road_restoration_meters or 0),
        str(civil_stage or "").strip(), str(work_description or "").strip(),
        str(supervisor_name or "").strip(), str(supervisor_phone or "").strip()
    ))
    conn.commit()
    conn.close()
    return True


def get_dpr(site_id, report_date):
    """
    Returns single DPR for site and date.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.*, s.name as site_name, s.code as site_code, s.location as site_location
        FROM daily_progress_reports d
        JOIN sites s ON d.site_id = s.id
        WHERE d.site_id = ? AND d.report_date = ?
    """, (int(site_id), str(report_date)))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_dpr_list(site_id=None, date_from=None, date_to=None, limit=100):
    """
    Returns list of DPR entries with optional site and date filters.
    """
    conn = get_db()
    cursor = conn.cursor()
    query = """
        SELECT d.*, s.name as site_name, s.code as site_code, s.location as site_location
        FROM daily_progress_reports d
        JOIN sites s ON d.site_id = s.id
        WHERE 1=1
    """
    params = []
    if site_id:
        query += " AND d.site_id = ?"
        params.append(int(site_id))
    if date_from:
        query += " AND d.report_date >= ?"
        params.append(str(date_from))
    if date_to:
        query += " AND d.report_date <= ?"
        params.append(str(date_to))
    
    query += " ORDER BY d.report_date DESC, d.id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_dpr_summary_stats(report_date=None):
    """
    Returns aggregated metrics for DPR on a specific date (or overall if None).
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COALESCE(SUM(pipe_laying_meters), 0) as total_pipe,
            COALESCE(SUM(fhtc_connections), 0) as total_fhtc,
            COALESCE(SUM(boring_depth_feet), 0) as total_boring,
            COALESCE(SUM(road_restoration_meters), 0) as total_road,
            COUNT(DISTINCT site_id) as total_active_sites,
            COUNT(*) as total_dpr_count
        FROM daily_progress_reports
    """)
    overall = dict(cursor.fetchone() or {})

    today_stats = {"pipe": 0, "fhtc": 0, "boring": 0, "road": 0, "sites_reported": 0}
    if report_date:
        cursor.execute("""
            SELECT 
                COALESCE(SUM(pipe_laying_meters), 0) as pipe,
                COALESCE(SUM(fhtc_connections), 0) as fhtc,
                COALESCE(SUM(boring_depth_feet), 0) as boring,
                COALESCE(SUM(road_restoration_meters), 0) as road,
                COUNT(DISTINCT site_id) as sites_reported
            FROM daily_progress_reports
            WHERE report_date = ?
        """, (str(report_date),))
        row = cursor.fetchone()
        if row:
            today_stats = dict(row)

    conn.close()
    return {
        "overall": overall,
        "today": today_stats
    }


def calculate_worker_site_proximity(site_id, lat, lng, default_site_lat=None, default_site_lng=None, default_radius=1000, work_date=None):
    """
    Calculates proximity of worker (lat, lng) against all sub-location points of the site.
    - If supervisor has selected active ward(s) for today (work_date), evaluates ONLY against those active wards!
    - If worker is within radius of ANY active point (Ward 1/2/3, Tank, etc.), is_on_site = True!
    - Defaults to 1000m (1 KM) geofence radius.
    - Returns (min_distance, is_on_site, nearest_point_name, effective_radius, all_points_summary)
    """
    import datetime as dt
    if not work_date:
        ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        work_date = ist_now.strftime("%Y-%m-%d")

    all_points = get_site_geo_points(site_id)
    active_record = get_daily_active_wards(site_id, work_date)
    points = all_points

    if active_record and active_record.get("active_point_ids"):
        raw_ids = active_record["active_point_ids"].strip()
        if raw_ids != "all":
            active_ids = set()
            for x in raw_ids.split(","):
                if x.strip().isdigit():
                    active_ids.add(int(x.strip()))
            if active_ids:
                filtered = [p for p in all_points if p["id"] in active_ids]
                if filtered:
                    points = filtered

    candidates = []

    # 1. Add sub-points
    for pt in points:
        candidates.append({
            "id": pt["id"],
            "name": pt["point_name"],
            "lat": float(pt["latitude"]),
            "lng": float(pt["longitude"]),
            "radius": int(pt.get("radius_meters") or default_radius or 1000)
        })

    # 2. Add main site GPS if configured and either no active record or set to 'all' or no candidate points
    if not candidates or not active_record or (active_record and active_record.get("active_point_ids") == "all"):
        if default_site_lat and default_site_lng:
            candidates.append({
                "id": 0,
                "name": "मुख्य केंद्र (Main Center)",
                "lat": float(default_site_lat),
                "lng": float(default_site_lng),
                "radius": int(default_radius or 1000)
            })

    if not candidates:
        return 99999.0, False, "GPS सेट नहीं", int(default_radius or 1000), []

    evaluated = []
    for c in candidates:
        dist = haversine_distance(lat, lng, c["lat"], c["lng"])
        is_in = (dist <= c["radius"])
        evaluated.append({
            "id": c.get("id"),
            "name": c["name"],
            "distance": round(dist, 1),
            "radius": c["radius"],
            "is_within": is_in,
            "lat": c["lat"],
            "lng": c["lng"]
        })

    # Sort by closest distance
    evaluated.sort(key=lambda x: x["distance"])
    closest = evaluated[0]

    # Check if worker is inside ANY of the candidate points
    inside_point = next((p for p in evaluated if p["is_within"]), None)
    if inside_point:
        return inside_point["distance"], True, inside_point["name"], inside_point["radius"], evaluated
    else:
        return closest["distance"], False, closest["name"], closest["radius"], evaluated


def process_location_ping(worker_id, site_id, lat, lng, site_lat=None, site_lng=None, radius=1000):
    """
    Called when a worker sends a location ping.
    - Supports multi-point GPS coordinates for wide-radius sites
    - Evaluates against supervisor's selected active wards for today
    - Calculates distance from closest sub-point
    - Marks check-in if within radius of ANY active site point and not already checked in today
    - Marks check-out if outside all points and currently checked in
    - Returns dict with status info
    """
    import datetime as dt

    ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today = ist_now.strftime("%Y-%m-%d")
    now_str = ist_now.strftime("%Y-%m-%d %H:%M:%S")

    distance, is_on_site, nearest_point, eff_radius, _ = calculate_worker_site_proximity(
        site_id, lat, lng, default_site_lat=site_lat, default_site_lng=site_lng, default_radius=radius, work_date=today
    )

    conn = get_db()
    cursor = conn.cursor()

    # Save location ping with lat, lng, nearest_point_name
    cursor.execute("""
        INSERT INTO worker_location_pings (worker_id, latitude, longitude, distance_meters, is_on_site, nearest_point_name, ping_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (worker_id, lat, lng, round(distance, 1), 1 if is_on_site else 0, nearest_point, now_str))

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
            # Auto-checkout rule: Only checkout if time is at or after 5:00 PM (17:00 IST)
            is_after_5pm = (ist_now.hour >= 17)
            if is_after_5pm:
                # Worker left after 5:00 PM -> auto check out, compute minutes
                try:
                    cin = dt.datetime.strptime(att["check_in_time"], "%Y-%m-%d %H:%M:%S")
                    minutes = int((ist_now - cin).total_seconds() / 60)
                except Exception:
                    minutes = 0
                cursor.execute("""
                    UPDATE geo_attendance
                    SET check_out_time = ?, total_minutes = ?, status = 'left'
                    WHERE worker_id = ? AND att_date = ?
                """, (now_str, max(0, minutes), worker_id, today))
                action = "checked_out"
            else:
                # Before 5:00 PM -> worker is temporarily outside work area (tea, lunch, shifting materials)
                # Keep status as 'present' and do not check out prematurely
                action = "temporarily_off_site"

    conn.commit()
    conn.close()

    return {
        "distance_m": round(distance, 1),
        "is_on_site": is_on_site,
        "nearest_point_name": nearest_point,
        "lat": lat,
        "lng": lng,
        "action": action,
        "timestamp": now_str
    }


def auto_checkout_workers_after_5pm(att_date=None):
    """
    Automatic 5:00 PM+ Exit Analyzer:
    Checks out any worker who has left their work location after 5:00 PM (17:00 IST).
    - If current time is < 17:00 IST for today's date, does nothing (preserves active work hours).
    - Finds all workers who checked in (status = 'present', check_in_time set, check_out_time empty).
    - Checks their latest location ping in worker_location_pings:
      * If ping is outside work site (is_on_site = 0):
        Automatically checks them out with check_out_time = ping_time (or now_str if ping was after 5pm),
        computes total_minutes, and sets status = 'left'.
    Returns count of workers auto-checked out.
    """
    import datetime as dt
    ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    now_str = ist_now.strftime("%Y-%m-%d %H:%M:%S")
    today = ist_now.strftime("%Y-%m-%d")

    target_date = att_date or today

    # Only run auto-checkout if target date is a previous date, or if today and time is >= 17:00 IST
    if target_date == today and ist_now.hour < 17:
        return 0

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, a.worker_id, a.site_id, a.check_in_time, a.status
        FROM geo_attendance a
        WHERE a.att_date = ? AND a.status = 'present' AND a.check_in_time IS NOT NULL AND (a.check_out_time IS NULL OR a.check_out_time = '')
    """, (target_date,))
    active_rows = [dict(r) for r in cursor.fetchall()]

    checked_out_count = 0
    for row in active_rows:
        wid = row["worker_id"]
        cursor.execute("""
            SELECT latitude, longitude, distance_meters, is_on_site, ping_time
            FROM worker_location_pings
            WHERE worker_id = ?
            ORDER BY id DESC LIMIT 1
        """, (wid,))
        last_ping = cursor.fetchone()
        last_ping = dict(last_ping) if last_ping else None

        should_checkout = False
        checkout_timestamp = now_str

        if last_ping:
            if last_ping.get("is_on_site") == 0:
                should_checkout = True
                ping_time = last_ping.get("ping_time")
                if ping_time:
                    try:
                        p_dt = dt.datetime.strptime(ping_time, "%Y-%m-%d %H:%M:%S")
                        if p_dt.hour >= 17:
                            checkout_timestamp = ping_time
                    except Exception:
                        pass
        elif target_date != today:
            should_checkout = True
            checkout_timestamp = f"{target_date} 17:00:00"

        if should_checkout:
            try:
                cin = dt.datetime.strptime(row["check_in_time"], "%Y-%m-%d %H:%M:%S")
                cout = dt.datetime.strptime(checkout_timestamp, "%Y-%m-%d %H:%M:%S")
                minutes = int((cout - cin).total_seconds() / 60)
            except Exception:
                minutes = 0

            cursor.execute("""
                UPDATE geo_attendance
                SET check_out_time = ?, total_minutes = ?, status = 'left'
                WHERE id = ?
            """, (checkout_timestamp, max(0, minutes), row["id"]))
            checked_out_count += 1

    conn.commit()
    conn.close()
    return checked_out_count


def get_geo_attendance_today(date_str=None):
    """
    Returns today's GPS attendance status for all workers across all sites.
    Includes exact last_lat, last_lng, last_dist, last_point_name, last_ping.
    """
    import datetime as dt
    if not date_str:
        ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        date_str = ist_now.strftime("%Y-%m-%d")

    # Automatically check out any workers who exited their work location after 5:00 PM
    try:
        auto_checkout_workers_after_5pm(date_str)
    except Exception:
        pass

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT w.id as worker_id, w.name as worker_name, w.role, w.phone, w.worker_token,
               s.id as site_id, s.name as site_name, s.code as site_code,
               a.check_in_time, a.check_out_time, a.total_minutes,
               a.status as att_status,
               a.photo_url,
               p.latitude as last_lat, p.longitude as last_lng,
               p.distance_meters as last_dist, p.ping_time as last_ping,
               p.is_on_site as last_on_site,
               p.nearest_point_name as last_point_name
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


@db_retry(max_retries=6, delay=0.25)
def save_worker_photo_attendance(worker_id, site_id, lat, lng, photo_url, att_date=None, check_type='check_in'):
    """
    Saves an attendance photo entry for a worker:
    - Records GPS coordinates into worker_location_pings
    - Updates or inserts geo_attendance with photo_url and check_in_time/check_out_time
    """
    import datetime as dt
    ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    if not att_date:
        att_date = ist_now.strftime("%Y-%m-%d")
    now_str = ist_now.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sites WHERE id = ?", (site_id,))
        site = cursor.fetchone()
        site_lat = site["latitude"] if site and "latitude" in site.keys() else None
        site_lng = site["longitude"] if site and "longitude" in site.keys() else None
        radius = site["geo_radius"] if site and "geo_radius" in site.keys() and site["geo_radius"] else 1000

        distance = 0.0
        is_on_site = True
        nearest_point = "फोटो हाजिरी"

        if lat and lng:
            try:
                distance, is_on_site, nearest_point, eff_radius, _ = calculate_worker_site_proximity(
                    site_id, float(lat), float(lng), default_site_lat=site_lat, default_site_lng=site_lng, default_radius=radius, work_date=att_date
                )
            except Exception:
                distance = 0.0
                is_on_site = True
                nearest_point = "फोटो हाजिरी"

            cursor.execute("""
                INSERT INTO worker_location_pings (worker_id, latitude, longitude, distance_meters, is_on_site, nearest_point_name, ping_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (worker_id, float(lat), float(lng), round(distance, 1), 1 if is_on_site else 0, f"📸 फोटो हाजिरी ({nearest_point})", now_str))

        cursor.execute("""
            SELECT * FROM geo_attendance WHERE worker_id = ? AND att_date = ?
        """, (worker_id, att_date))
        att = cursor.fetchone()

        action = "checked_in"
        if not att:
            cursor.execute("""
                INSERT INTO geo_attendance (worker_id, site_id, att_date, check_in_time, status, photo_url)
                VALUES (?, ?, ?, ?, 'present', ?)
            """, (worker_id, site_id, att_date, now_str, photo_url))
            action = "checked_in"
        else:
            att = dict(att)
            if check_type == 'check_out':
                try:
                    cin = dt.datetime.strptime(att["check_in_time"], "%Y-%m-%d %H:%M:%S") if att.get("check_in_time") else ist_now
                    minutes = int((ist_now - cin).total_seconds() / 60)
                except Exception:
                    minutes = 0
                cursor.execute("""
                    UPDATE geo_attendance
                    SET check_out_time = ?, total_minutes = ?, status = 'left', photo_url = COALESCE(?, photo_url)
                    WHERE worker_id = ? AND att_date = ?
                """, (now_str, max(0, minutes), photo_url, worker_id, att_date))
                action = "checked_out"
            else:
                new_cin = att["check_in_time"] if att.get("check_in_time") else now_str
                cursor.execute("""
                    UPDATE geo_attendance
                    SET check_in_time = ?, status = 'present', photo_url = ?
                    WHERE worker_id = ? AND att_date = ?
                """, (new_cin, photo_url, worker_id, att_date))
                action = "photo_saved"

        try:
            cursor.execute("UPDATE site_workers SET last_active = ? WHERE id = ?", (now_str, worker_id))
        except Exception:
            try:
                cursor.execute("ALTER TABLE site_workers ADD COLUMN last_active TEXT")
                cursor.execute("UPDATE site_workers SET last_active = ? WHERE id = ?", (now_str, worker_id))
            except Exception:
                pass

        conn.commit()
    finally:
        conn.close()

    _notify_cloud_backup()

    return {
        "success": True,
        "action": action,
        "photo_url": photo_url,
        "is_on_site": is_on_site,
        "distance": round(distance, 1),
        "distance_m": round(distance, 1),
        "nearest_point": nearest_point,
        "timestamp": now_str
    }


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


# ==========================================
# SITE WORK PHOTOS & A4 4-PHOTO ALBUM DATABASE LAYER
# ==========================================

def init_photo_tables():
    """
    Initializes site_work_photos table for Jal Jeevan Mission photo documentation & A4 4-photo albums.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_work_photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER NOT NULL,
        photo_date TEXT NOT NULL,
        uploaded_at TEXT NOT NULL,
        uploaded_by TEXT DEFAULT '',
        uploader_phone TEXT DEFAULT '',
        category TEXT NOT NULL DEFAULT 'सामान्य कार्य',
        description TEXT DEFAULT '',
        latitude REAL,
        longitude REAL,
        accuracy REAL DEFAULT 0,
        photo_url TEXT NOT NULL,
        file_size_kb INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()


def add_site_work_photo(site_id, photo_date, uploaded_at, uploaded_by, uploader_phone, category, description, latitude, longitude, accuracy, photo_url, file_size_kb):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO site_work_photos 
        (site_id, photo_date, uploaded_at, uploaded_by, uploader_phone, category, description, latitude, longitude, accuracy, photo_url, file_size_kb)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (site_id, photo_date, uploaded_at, uploaded_by, uploader_phone, category, description, latitude, longitude, accuracy, photo_url, file_size_kb))
    photo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return photo_id


def get_site_work_photos(site_id=None, month_str=None, date_str=None, category=None, limit=1000):
    conn = get_db()
    cursor = conn.cursor()
    query = """
        SELECT p.*, s.name as site_name, s.code as site_code, s.supervisor as site_supervisor
        FROM site_work_photos p
        JOIN sites s ON p.site_id = s.id
        WHERE 1=1
    """
    params = []
    if site_id:
        query += " AND p.site_id = ?"
        params.append(site_id)
    if date_str:
        query += " AND p.photo_date = ?"
        params.append(date_str)
    elif month_str:
        query += " AND p.photo_date LIKE ?"
        params.append(month_str + "%")
    if category and category != "all" and category != "":
        query += " AND p.category = ?"
        params.append(category)
    
    query += " ORDER BY p.photo_date ASC, p.uploaded_at ASC, p.id ASC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_site_work_photo_by_id(photo_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, s.name as site_name, s.code as site_code, s.supervisor as site_supervisor
        FROM site_work_photos p
        JOIN sites s ON p.site_id = s.id
        WHERE p.id = ?
    """, (photo_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_site_work_photo(photo_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT photo_url FROM site_work_photos WHERE id = ?", (photo_id,))
    row = cursor.fetchone()
    url = row[0] if row else None
    cursor.execute("DELETE FROM site_work_photos WHERE id = ?", (photo_id,))
    conn.commit()
    conn.close()
    return url


def get_available_photo_months(site_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if site_id:
        cursor.execute("""
            SELECT DISTINCT substr(photo_date, 1, 7) as ym, COUNT(*) as cnt
            FROM site_work_photos
            WHERE site_id = ?
            GROUP BY ym
            ORDER BY ym DESC
        """, (site_id,))
    else:
        cursor.execute("""
            SELECT DISTINCT substr(photo_date, 1, 7) as ym, COUNT(*) as cnt
            FROM site_work_photos
            GROUP BY ym
            ORDER BY ym DESC
        """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_photo_category_counts(site_id=None, month_str=None):
    conn = get_db()
    cursor = conn.cursor()
    query = """
        SELECT category, COUNT(*) as cnt
        FROM site_work_photos
        WHERE 1=1
    """
    params = []
    if site_id:
        query += " AND site_id = ?"
        params.append(site_id)
    if month_str:
        query += " AND photo_date LIKE ?"
        params.append(month_str + "%")
    query += " GROUP BY category ORDER BY cnt DESC"
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


# ==========================================
# SILENT SUPERVISOR & INCHARGE LOCATION TRACKING
# ==========================================

@db_retry(max_retries=6, delay=0.25)
def log_supervisor_silent_ping(site_id, supervisor_name="", phone="", lat=0.0, lng=0.0, accuracy=0, page_source="background"):
    """
    Silently records the live GPS location of a site supervisor / incharge.
    Calculates distance to site's designated GPS coordinate or active work wards.
    """
    import datetime as dt
    if not lat or not lng:
        return {"success": False, "message": "Invalid coordinates"}

    ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today_str = ist_now.strftime("%Y-%m-%d")
    now_str = ist_now.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    try:
        cursor = conn.cursor()

        # Look up site info
        cursor.execute("""
            SELECT id, name, code, supervisor, contact, incharge, incharge_phone, latitude, longitude, geo_radius
            FROM sites WHERE id = ?
        """, (site_id,))
        site = cursor.fetchone()
        if not site:
            return {"success": False, "message": "Site not found"}

        site_dict = dict(site)
        if not supervisor_name:
            supervisor_name = site_dict.get("supervisor") or site_dict.get("incharge") or f"Supervisor Site {site_id}"
        if not phone:
            phone = site_dict.get("contact") or site_dict.get("incharge_phone") or ""

        site_lat = site_dict.get("latitude")
        site_lng = site_dict.get("longitude")
        radius = site_dict.get("geo_radius") or 1000

        # Calculate proximity
        distance = 0.0
        is_on_site = 0
        nearest_point = "कार्य स्थल"
        try:
            distance, on_site_bool, nearest_point, eff_radius, _ = calculate_worker_site_proximity(
                site_id, float(lat), float(lng), default_site_lat=site_lat, default_site_lng=site_lng, default_radius=radius, work_date=today_str
            )
            is_on_site = 1 if on_site_bool else 0
        except Exception:
            if site_lat and site_lng:
                distance = haversine_distance(float(lat), float(lng), float(site_lat), float(site_lng))
                is_on_site = 1 if distance <= radius else 0
                nearest_point = site_dict.get("name", "Site")

        cursor.execute("""
            INSERT INTO supervisor_location_logs (
                site_id, supervisor_name, supervisor_phone, latitude, longitude,
                accuracy, distance_meters, is_on_site, nearest_point_name, page_source,
                ping_time, ping_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            site_id, str(supervisor_name), str(phone), float(lat), float(lng),
            float(accuracy or 0), round(distance, 1), is_on_site, str(nearest_point), str(page_source),
            now_str, today_str
        ))
        conn.commit()
    finally:
        conn.close()

    return {
        "success": True,
        "site_id": site_id,
        "supervisor_name": supervisor_name,
        "distance_meters": round(distance, 1),
        "is_on_site": bool(is_on_site),
        "nearest_point": nearest_point,
        "ping_time": now_str
    }


def get_supervisors_live_tracking_today(date_str=None):
    """
    Returns the latest live GPS tracking status of every site's supervisor for today.
    Used exclusively by the owner to monitor supervisors across all 21 sites.
    """
    import datetime as dt
    if not date_str:
        ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        date_str = ist_now.strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()

    # Get all sites
    cursor.execute("""
        SELECT id, code, name, location, supervisor, contact, incharge, incharge_phone,
               latitude, longitude, geo_radius
        FROM sites
        ORDER BY name
    """)
    sites = [dict(s) for s in cursor.fetchall()]

    results = []
    for s in sites:
        sid = s["id"]
        # Fetch latest ping for today
        cursor.execute("""
            SELECT * FROM supervisor_location_logs
            WHERE site_id = ? AND ping_date = ?
            ORDER BY id DESC LIMIT 1
        """, (sid, date_str))
        last_ping_row = cursor.fetchone()

        is_today = True
        if not last_ping_row:
            # Fallback to absolute latest ping for reference
            cursor.execute("""
                SELECT * FROM supervisor_location_logs
                WHERE site_id = ?
                ORDER BY id DESC LIMIT 1
            """, (sid,))
            last_ping_row = cursor.fetchone()
            is_today = False

        # Total pings today count
        cursor.execute("""
            SELECT COUNT(*) FROM supervisor_location_logs
            WHERE site_id = ? AND ping_date = ?
        """, (sid, date_str))
        today_pings_count = cursor.fetchone()[0]

        last_ping = dict(last_ping_row) if last_ping_row else None

        sup_name = (last_ping.get("supervisor_name") if last_ping else None) or s.get("supervisor") or s.get("incharge") or "सुपरवाइजर"
        sup_phone = (last_ping.get("supervisor_phone") if last_ping else None) or s.get("contact") or s.get("incharge_phone") or ""

        results.append({
            "site_id": sid,
            "site_code": s.get("code"),
            "site_name": s.get("name"),
            "site_location": s.get("location"),
            "supervisor_name": sup_name,
            "supervisor_phone": sup_phone,
            "incharge": s.get("incharge"),
            "incharge_phone": s.get("incharge_phone"),
            "site_lat": s.get("latitude"),
            "site_lng": s.get("longitude"),
            "geo_radius": s.get("geo_radius") or 1000,
            "has_ping": bool(last_ping and is_today),
            "is_today": is_today,
            "today_pings_count": today_pings_count,
            "last_lat": last_ping.get("latitude") if last_ping else None,
            "last_lng": last_ping.get("longitude") if last_ping else None,
            "last_accuracy": last_ping.get("accuracy") if last_ping else None,
            "last_distance_m": last_ping.get("distance_meters") if last_ping else None,
            "is_on_site": bool(last_ping.get("is_on_site")) if (last_ping and is_today) else False,
            "nearest_point": last_ping.get("nearest_point_name") if last_ping else None,
            "page_source": last_ping.get("page_source") if last_ping else None,
            "last_ping_time": last_ping.get("ping_time") if last_ping else None,
        })

    conn.close()
    return results


def get_supervisor_route_today(site_id, date_str=None):
    """
    Returns all location points for a supervisor on a given date to view their movement trail.
    """
    import datetime as dt
    if not date_str:
        ist_now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        date_str = ist_now.strftime("%Y-%m-%d")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM supervisor_location_logs
        WHERE site_id = ? AND ping_date = ?
        ORDER BY id ASC
    """, (site_id, date_str))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows




