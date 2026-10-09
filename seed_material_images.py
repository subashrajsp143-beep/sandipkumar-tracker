# -*- coding: utf-8 -*-
"""
Populate default high-quality product images for all materials.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_tracker.db")

# High-resolution Unsplash curated stock photos for industrial & plumbing supplies
CATEGORY_IMAGES = {
    "Pipes": "https://images.unsplash.com/photo-1541888946425-d0fbb186c5f9?w=400&auto=format&fit=crop&q=80",
    "Motors & Starters": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400&auto=format&fit=crop&q=80",
    "Starter": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&auto=format&fit=crop&q=80",
    "Valves": "https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=400&auto=format&fit=crop&q=80",
    "Water Tanks": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400&auto=format&fit=crop&q=80",
    "Electrical": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=400&auto=format&fit=crop&q=80",
    "Fittings - Elbow": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&auto=format&fit=crop&q=80",
    "Fittings - Tee": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&auto=format&fit=crop&q=80",
    "Fittings - Socket": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&auto=format&fit=crop&q=80",
    "Fittings - MTA/FTA": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&auto=format&fit=crop&q=80",
    "Fittings - Union": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&auto=format&fit=crop&q=80",
    "Jointers & Couplings": "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?w=400&auto=format&fit=crop&q=80",
    "End Caps": "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?w=400&auto=format&fit=crop&q=80",
    "Reducers": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&auto=format&fit=crop&q=80",
    "Saddles": "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?w=400&auto=format&fit=crop&q=80",
    "Nipples & Bush": "https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&auto=format&fit=crop&q=80",
    "Accessories & Consumables": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=400&auto=format&fit=crop&q=80",
    "Repairs & Maintenance": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400&auto=format&fit=crop&q=80",
    "Tools & Machinery": "https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=400&auto=format&fit=crop&q=80"
}

# Specific keyword overrides for maximum visual accuracy
KEYWORD_IMAGES = {
    "STARTER": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400&auto=format&fit=crop&q=80",
    "MOTOR": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400&auto=format&fit=crop&q=80",
    "PUMP": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=400&auto=format&fit=crop&q=80",
    "TANK": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400&auto=format&fit=crop&q=80",
    "CABLE": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=400&auto=format&fit=crop&q=80",
    "WIRE": "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=400&auto=format&fit=crop&q=80",
    "VALVE": "https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=400&auto=format&fit=crop&q=80",
    "TEFLON": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=400&auto=format&fit=crop&q=80",
    "SOLVENT": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=400&auto=format&fit=crop&q=80",
    "PIPE": "https://images.unsplash.com/photo-1541888946425-d0fbb186c5f9?w=400&auto=format&fit=crop&q=80",
}

def seed_images():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category, image_url FROM materials")
    materials = cursor.fetchall()

    updated = 0
    for mat_id, name, category, cur_img in materials:
        if cur_img and cur_img.strip():
            continue  # Keep user's custom image

        img_url = None
        upper_name = name.upper()

        # Check keyword overrides
        for kw, kw_url in KEYWORD_IMAGES.items():
            if kw in upper_name:
                img_url = kw_url
                break

        # Fallback to category
        if not img_url:
            img_url = CATEGORY_IMAGES.get(category, "https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=400&auto=format&fit=crop&q=80")

        cursor.execute("UPDATE materials SET image_url = ? WHERE id = ?", (img_url, mat_id))
        updated += 1

    conn.commit()
    conn.close()
    print(f"Updated {updated} materials with default high-quality product images!")

if __name__ == "__main__":
    seed_images()
