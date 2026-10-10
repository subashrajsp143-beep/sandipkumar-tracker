# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('material_tracker.db')
cursor = conn.cursor()

# Get existing sites
cursor.execute('SELECT id, code, name FROM sites')
existing_sites = cursor.fetchall()
site_dict = {s[2].strip().upper(): s for s in existing_sites}

# Exact 21 sites from the user's photo
photo_sites = [
    ("SITE-03", "MADHUBANI"),
    ("SITE-08", "SINGHIYA"),
    ("SITE-14", "SONPUR"),
    ("SITE-19", "SHEOHAR"),
    ("SITE-05", "JHANJHARPUR"),
    ("SITE-07", "EKMA"),
    ("SITE-04", "SIWAN"),
    ("SITE-18", "CHHAPRA"),
    ("SITE-09", "ANDAR"),
    ("SITE-01", "MAIRWA"),
    ("SITE-17", "BASANTPUR"),
    ("SITE-02", "HASANPURA"),
    ("SITE-20", "KATI"),
    ("SITE-15", "DARBHANGA"),
    ("SITE-11", "MAHARAJGANJ"),
    ("SITE-13", "GUTHANI"),
    ("SITE-06", "BARHARIYA"),
    ("SITE-10", "SAHEBGANJ"),
    ("SITE-12", "MIRGANJ"),
    ("SITE-16", "NAUBATHPUR"),
    ("SITE-21", "PARSA"),
]

# Map alternative spellings in DB
alias_map = {
    "SEOHAR": "SHEOHAR",
    "SONEPUR": "SONPUR",
    "MAHARAJGUNJ": "MAHARAJGANJ",
    "SAHEBGUNJ": "SAHEBGANJ",
    "MIRGUNJ": "MIRGANJ",
    "NAUBATPUR": "NAUBATHPUR"
}

for code, name in photo_sites:
    found = False
    for existing_name, s_data in site_dict.items():
        if existing_name == name or alias_map.get(existing_name) == name:
            found = True
            # Update name to exact photo spelling
            cursor.execute("UPDATE sites SET name = ? WHERE id = ?", (name.title(), s_data[0]))
            break
    if not found:
        print(f"Adding new site: {code} - {name}")
        cursor.execute("INSERT INTO sites (code, name, location, status) VALUES (?, ?, ?, 'Active')", (code, name.title(), name.title()))

conn.commit()

# Re-fetch all sites
cursor.execute('SELECT id, code, name FROM sites ORDER BY id')
all_sites = cursor.fetchall()
print(f"Total sites now: {len(all_sites)}")
for s in all_sites:
    print(s)

conn.close()
