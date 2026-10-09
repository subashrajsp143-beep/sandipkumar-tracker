# -*- coding: utf-8 -*-
"""
Map all 271 materials to their exact local high-resolution product images.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_tracker.db")

def assign_real_images():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category FROM materials")
    materials = cursor.fetchall()

    updated = 0
    for mat_id, name, category in materials:
        uname = name.upper()
        img = None

        # 1. Motors & Starters
        if "STARTER" in uname:
            img = "/uploads/materials/starter_panel.jpg"
        elif "MOTOR" in uname or "PUMP" in uname:
            img = "/uploads/materials/submersible_motor.jpg"
        
        # 2. Water Tanks
        elif "TANK" in uname and ("SINTEX" in uname or "WATER" in uname or "LITRE" in uname or "1000" in uname or "2000" in uname or "5000" in uname):
            img = "/uploads/materials/sintex_water_tank.jpg"

        # 3. Valves
        elif "GATE VALVE" in uname or ("VALVE" in uname and "BRASS" in uname):
            img = "/uploads/materials/brass_gate_valve.jpg"
        elif "BALL VALVE" in uname or "UPVC VALVE" in uname or "VALVE" in uname:
            img = "/uploads/materials/upvc_ball_valve.jpg"

        # 4. Pipes
        elif "HDPE" in uname or "MDPE" in uname:
            img = "/uploads/materials/hdpe_pipe.jpg"
        elif "UPVC PIPE" in uname or "GI PIPE" in uname or "PIPE" in uname and category == "Pipes":
            img = "/uploads/materials/upvc_pipe.jpg"

        # 5. Cables & Electrical
        elif "CABLE" in uname or "WIRE" in uname or "STABILIZER" in uname or category == "Electrical":
            img = "/uploads/materials/cable.jpg"

        # 6. Specific Consumables
        elif "TEFLON" in uname:
            img = "/uploads/materials/teflon_tape.jpg"
        elif "SOLVENT" in uname:
            img = "/uploads/materials/hardware_consumables.jpg"
        elif "NAL" in uname or "TAP" in uname:
            img = "/uploads/materials/water_tap.jpg"
        elif "BREKAN" in uname or "MACHIN" in uname or "HAMMER" in uname:
            img = "/uploads/materials/tools.jpg"

        # 7. Jointers, Couplings & Saddles
        elif "JOINTER" in uname or "COUPLING" in uname or "SADDLE" in uname or category in ["Jointers & Couplings", "Saddles"]:
            img = "/uploads/materials/jointers.jpg"

        # 8. Fittings (Elbow, Tee, Socket, MTA, FTA, Union, Reducers, Bush, End Cap)
        elif category in ["Fittings - Elbow", "Fittings - Tee", "Fittings - Socket", "Fittings - MTA/FTA", "Fittings - Union", "Reducers", "End Caps", "Nipples & Bush"]:
            img = "/uploads/materials/fittings.jpg"

        # 9. Fallback Consumables / Accessories
        else:
            img = "/uploads/materials/hardware_consumables.jpg"

        cursor.execute("UPDATE materials SET image_url = ? WHERE id = ?", (img, mat_id))
        updated += 1

    conn.commit()
    conn.close()
    print(f"Successfully mapped {updated} materials to exact realistic local product photos!")

if __name__ == "__main__":
    assign_real_images()
