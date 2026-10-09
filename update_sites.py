# -*- coding: utf-8 -*-
"""
Update SQLite database with the exact 19 sites from M/S SANDIP KUMAR.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_tracker.db")

REAL_SITES = [
    {"sl": 1, "code": "SITE-01", "name": "Mairwa", "supervisor": "Amresh kumar", "contact": "7006861251", "incharge": "", "incharge_phone": ""},
    {"sl": 2, "code": "SITE-02", "name": "Hasanpura", "supervisor": "Pradeep kumar", "contact": "8235914916", "incharge": "", "incharge_phone": ""},
    {"sl": 3, "code": "SITE-03", "name": "Madhubani", "supervisor": "Satyajit jha", "contact": "8789437567", "incharge": "Deepak kumar", "incharge_phone": "7319758929"},
    {"sl": 4, "code": "SITE-04", "name": "Siwan", "supervisor": "Azad Hussain", "contact": "6002074305", "incharge": "Ankit singh", "incharge_phone": "7481813476"},
    {"sl": 5, "code": "SITE-05", "name": "Jhanjharpur", "supervisor": "Pawan kumar", "contact": "6205433166", "incharge": "Baccha kr yadav", "incharge_phone": "9128850850"},
    {"sl": 6, "code": "SITE-06", "name": "Barhariya", "supervisor": "Aditya kumar", "contact": "8709995412", "incharge": "SK Sasank", "incharge_phone": "9525712171"},
    {"sl": 7, "code": "SITE-07", "name": "Ekma", "supervisor": "Devsaran kumar", "contact": "8882145857", "incharge": "Sunil kumar", "incharge_phone": "7488884776"},
    {"sl": 8, "code": "SITE-08", "name": "Singhiya", "supervisor": "Vikash kumar", "contact": "7979903651", "incharge": "Abhisekh kumar", "incharge_phone": "8874517729"},
    {"sl": 9, "code": "SITE-09", "name": "Andar", "supervisor": "Sonu Kumar", "contact": "9123265466", "incharge": "", "incharge_phone": ""},
    {"sl": 10, "code": "SITE-10", "name": "Sahebgunj", "supervisor": "Sanjeev kumar", "contact": "8579939794", "incharge": "", "incharge_phone": ""},
    {"sl": 11, "code": "SITE-11", "name": "Maharajgunj", "supervisor": "Satyam Kumar", "contact": "6289419893", "incharge": "Rahul kumar", "incharge_phone": "7909070329"},
    {"sl": 12, "code": "SITE-12", "name": "Mirgunj", "supervisor": "Chandraprakash pandey", "contact": "7033998700", "incharge": "", "incharge_phone": ""},
    {"sl": 13, "code": "SITE-13", "name": "Guthani", "supervisor": "Ramchandra ram", "contact": "9608074915", "incharge": "", "incharge_phone": ""},
    {"sl": 14, "code": "SITE-14", "name": "Sonepur", "supervisor": "Raju kumar", "contact": "9341881571", "incharge": "Raviranjan kumar", "incharge_phone": "7654313040"},
    {"sl": 15, "code": "SITE-15", "name": "Darbhanga", "supervisor": "Taj hussain", "contact": "8539998913", "incharge": "Mritunjay kumar", "incharge_phone": "9661528560"},
    {"sl": 16, "code": "SITE-16", "name": "Naubatpur", "supervisor": "Amit kumar", "contact": "7250894194", "incharge": "Diptanshu kumar", "incharge_phone": "8809395678"},
    {"sl": 17, "code": "SITE-17", "name": "Basantpur", "supervisor": "Abhisekh kumar", "contact": "8002505036", "incharge": "", "incharge_phone": ""},
    {"sl": 18, "code": "SITE-18", "name": "Chhapra", "supervisor": "Kundan kumar", "contact": "7371819939", "incharge": "Srikant kumar", "incharge_phone": "9852316947"},
    {"sl": 19, "code": "SITE-19", "name": "Seohar", "supervisor": "Amit kumar", "contact": "9102853181", "incharge": "", "incharge_phone": ""},
]

def update_sites():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if incharge columns exist, add if not
    cursor.execute("PRAGMA table_info(sites)")
    columns = [row[1] for row in cursor.fetchall()]
    if "incharge" not in columns:
        cursor.execute("ALTER TABLE sites ADD COLUMN incharge TEXT")
    if "incharge_phone" not in columns:
        cursor.execute("ALTER TABLE sites ADD COLUMN incharge_phone TEXT")

    # Update each site 1 to 19
    for s in REAL_SITES:
        cursor.execute("""
            UPDATE sites 
            SET name = ?, supervisor = ?, contact = ?, incharge = ?, incharge_phone = ?
            WHERE id = ?
        """, (s["name"], s["supervisor"], s["contact"], s["incharge"], s["incharge_phone"], s["sl"]))

    conn.commit()
    conn.close()
    print("All 19 sites updated with M/S SANDIP KUMAR site directory!")

if __name__ == "__main__":
    update_sites()
