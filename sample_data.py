# -*- coding: utf-8 -*-
"""
Generate realistic sample consumption entries so the user immediately sees
how reports, summaries, and graphs work upon first launch.
"""

import random
from datetime import datetime, timedelta
import database

def seed_sample_consumption():
    conn = database.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM daily_consumption")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    cursor.execute("SELECT id, name FROM sites")
    sites = cursor.fetchall()

    cursor.execute("SELECT id, name, unit, rate FROM materials")
    materials = cursor.fetchall()

    if not sites or not materials:
        conn.close()
        return

    purposes = [
        "Main pipeline distribution",
        "House tap connection work",
        "Borewell pump installation",
        "Submersible starter testing & connection",
        "Valve fitting at junction point",
        "Overhead tank inlet connection",
        "Pipeline repair & jointing",
        "Electrical cable trenching & termination"
    ]

    supervisors = ["Ramesh Kumar", "Suresh Sharma", "Anil Verma", "Rajesh Singh", "Vikas Yadav"]

    today = datetime.now()

    # Generate 45 realistic entries across the past 7 days across various of the 19 sites
    for i in range(45):
        days_ago = random.randint(0, 6)
        date_str = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        site = random.choice(sites)
        mat = random.choice(materials)

        site_id = site["id"]
        mat_id = mat["id"]
        rate = mat["rate"] if mat["rate"] > 0 else random.choice([50.0, 120.0, 350.0, 850.0])
        
        # Quantity based on unit
        if "MTR" in mat["unit"].upper():
            qty = random.choice([15, 30, 45, 60, 100, 120])
        elif "PACKET" in mat["unit"].upper():
            qty = random.choice([1, 2, 3, 5])
        else:
            qty = random.choice([1, 2, 3, 4, 5, 8, 10, 12])

        total_amount = round(qty * rate, 2)
        purpose = random.choice(purposes)
        supervisor = random.choice(supervisors)
        remarks = f"Material issued for {purpose.lower()}"

        cursor.execute("""
            INSERT INTO daily_consumption (site_id, material_id, usage_date, quantity, rate, total_amount, purpose, entered_by, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (site_id, mat_id, date_str, qty, rate, total_amount, purpose, supervisor, remarks))

    conn.commit()
    conn.close()
    print("Sample consumption entries added successfully!")

if __name__ == "__main__":
    seed_sample_consumption()
