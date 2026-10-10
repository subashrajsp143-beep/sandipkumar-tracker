# -*- coding: utf-8 -*-
"""
Add Daily Manpower Attendance table and database queries to database.py
"""

def patch_database():
    with open('database.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add table creation in init_db
    table_sql = '''
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
'''

    if 'daily_manpower' not in content:
        # insert right before conn.commit() in init_db()
        target = 'conn.commit()'
        content = content.replace(target, table_sql + '\n    ' + target, 1)

    # 2. Add functions for manpower
    manpower_functions = '''
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
'''

    if 'def get_daily_manpower' not in content:
        content += '\n' + manpower_functions

    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("database.py updated with daily manpower schema and functions!")

if __name__ == '__main__':
    patch_database()
