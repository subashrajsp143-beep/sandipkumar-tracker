# -*- coding: utf-8 -*-
"""
Seed the exact daily manpower data from the user's photo for date 2026-10-08
"""
import database

# Initialize DB table
database.init_db()

conn = database.get_db()
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM sites")
site_map = {row["name"].strip().lower(): row["id"] for row in cursor.fetchall()}

# Alias map
alias = {
    "sonepur": "sonpur",
    "seohar": "sheohar",
    "maharajgunj": "maharajganj",
    "sahebgunj": "sahebganj",
    "mirgunj": "mirganj",
    "naubatpur": "naubathpur"
}

photo_data = [
    # (site_name, incharge, sup, elec, gi, deo, plumb, helper, other, remarks)
    ("Madhubani", 1, 1, 1, 0, 1, 2, 3, 0, "RAINING"),
    ("Singhiya", 1, 0, 0, 0, 0, 2, 2, 0, ""),
    ("Sonpur", 1, 1, 0, 0, 0, 1, 3, 0, ""),
    ("Sheohar", 0, 0, 0, 0, 0, 0, 0, 0, "NOT REACHABLE"),
    ("Jhanjharpur", 1, 1, 0, 1, 0, 0, 1, 0, "RAINING"),
    ("Ekma", 1, 1, 0, 1, 0, 0, 2, 0, ""),
    ("Siwan", 1, 1, 0, 3, 0, 0, 3, 0, "SITE CLOSED(WORKERS IN OWNER HOME)"),
    ("Chhapra", 1, 2, 0, 4, 0, 0, 0, 0, ""),
    ("Andar", 0, 0, 0, 0, 0, 0, 0, 0, "SITE CLOSED DUE TO MANPOWER"),
    ("Mairwa", 0, 1, 0, 0, 0, 2, 1, 0, ""),
    ("Basantpur", 0, 1, 0, 1, 0, 0, 1, 0, "SITE CLOSED(WORKERS IN OWNER HOME)"),
    ("Hasanpura", 0, 1, 0, 3, 0, 0, 2, 0, ""),
    ("Kati", 0, 0, 0, 0, 0, 0, 0, 0, ""),
    ("Darbhanga", 1, 1, 0, 0, 1, 4, 4, 0, ""),
    ("Maharajganj", 1, 1, 0, 3, 0, 0, 2, 0, "SITE CLOSED(WORKERS IN OWNER HOME)"),
    ("Guthani", 1, 1, 0, 1, 0, 0, 2, 0, ""),
    ("Barhariya", 0, 1, 0, 0, 0, 2, 2, 0, "SITE CLOSED(WORKERS IN OWNER HOME)"),
    ("Sahebganj", 0, 1, 0, 1, 0, 0, 2, 0, ""),
    ("Mirganj", 1, 1, 0, 0, 0, 4, 2, 0, ""),
    ("Naubathpur", 1, 1, 0, 1, 0, 0, 2, 0, ""),
    ("Parsa", 0, 0, 0, 0, 0, 0, 0, 0, "")
]

rows_to_save = []
for item in photo_data:
    name, si, sup, elec, gi, deo, plumb, help_cnt, oth, rem = item
    lookup_name = alias.get(name.lower(), name.lower())
    s_id = site_map.get(lookup_name)
    if not s_id:
        # try direct
        s_id = site_map.get(name.lower())
    
    if s_id:
        rows_to_save.append({
            "site_id": s_id,
            "site_incharge": si,
            "supervisor": sup,
            "electrician": elec,
            "gi_mistri": gi,
            "deo": deo,
            "plumber": plumb,
            "helper": help_cnt,
            "other": oth,
            "remarks": rem
        })
    else:
        print(f"Warning: site {name} not found in DB!")

print(f"Prepared {len(rows_to_save)} rows to seed.")
database.save_daily_manpower("2026-10-08", rows_to_save, updated_by="Photo Seed")
print("Successfully seeded 2026-10-08 manpower attendance matching the photo!")

# Verify
rows, totals = database.get_daily_manpower("2026-10-08")
print(f"Verified {len(rows)} sites in report. Grand Total Manpower: {totals['total']}")
conn.close()
