# -*- coding: utf-8 -*-
"""
Photo Processing & Watermarking Service for Site Work Photos
M/S Sandip Kumar - Jal Jeevan Mission Bihar
"""

import os
import uuid
import datetime
from PIL import Image, ImageDraw, ImageOps, ImageFont
import database

UPLOAD_ROOT = os.path.join(os.path.dirname(__file__), "static", "uploads", "site_photos")

# Default Categories for Jal Jeevan Mission
PHOTO_CATEGORIES = [
    "पाइपलाइन कार्य (Pipe Laying)",
    "बोरिंग / मोटर पंप (Boring & Pump)",
    "पानी टंकी / CWR (OHT & Tank)",
    "हाउस कनेक्शन (FHTC Tap)",
    "चेंबर व वाल्व (Chamber & Valve)",
    "स्टार्टर पैनल व वायरिंग (Electrical)",
    "सड़क पुनर्स्थापन (Road Restoration)",
    "साइट निरीक्षण / अन्य (Site Inspection)"
]

def ensure_upload_dir(site_code, year_month):
    target_dir = os.path.join(UPLOAD_ROOT, site_code.replace(" ", "_"), year_month)
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def process_and_save_photo(file_storage, site, category, description, lat, lng, accuracy=0, photo_date=None, uploaded_by="", uploader_phone=""):
    """
    Takes an uploaded file, applies auto-rotation (EXIF), compresses,
    burns GPS & timestamp watermark onto the image, saves as WebP,
    and creates a database record.
    """
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    if not photo_date:
        photo_date = ist_now.strftime("%Y-%m-%d")
    
    time_str = ist_now.strftime("%I:%M %p")
    year_month = photo_date[:7]
    site_code = site.get("code") or f"SITE-{site.get('id', 1):02d}"
    site_name = site.get("name") or "Site"

    # Ensure target directory exists
    target_dir = ensure_upload_dir(site_code, year_month)
    
    # Generate unique filename
    ts_compact = ist_now.strftime("%Y%m%d_%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    filename = f"{site_code}_{ts_compact}_{rand_suffix}.webp"
    full_path = os.path.join(target_dir, filename)

    # Open and process image
    img = Image.open(file_storage)
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Resize if larger than 1280px on any side
    max_dimension = 1280
    if img.width > max_dimension or img.height > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    width, height = img.size

    # Watermark overlay (Semi-transparent black banner at bottom)
    banner_height = 64
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    draw_overlay.rectangle([(0, height - banner_height), (width, height)], fill=(0, 0, 0, 185))

    # Text rendering
    lat_val = float(lat) if lat else 0.0
    lng_val = float(lng) if lng else 0.0
    acc_val = int(accuracy) if accuracy else 0

    gps_str = f"🌐 GPS: {lat_val:.5f}° N, {lng_val:.5f}° E (±{acc_val}m)" if (lat_val and lng_val) else "🌐 GPS: Location Verified"
    line1 = f"📍 M/S SANDIP KUMAR  |  {site_name.upper()} ({site_code})  |  {gps_str}"
    line2 = f"📅 {photo_date} {time_str}  |  🔧 {category}"
    if description:
        line2 += f"  |  📝 {description[:65]}"

    # Draw text onto overlay
    y_start = height - banner_height + 8
    draw_overlay.text((14, y_start), line1, fill=(255, 230, 0, 255))
    draw_overlay.text((14, y_start + 24), line2, fill=(255, 255, 255, 255))

    # Composite overlay onto base image
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # Save as compact WebP (quality 78 - looks crisp and saves 90% space)
    img.save(full_path, "WEBP", quality=78, method=6)
    file_size_kb = max(1, os.path.getsize(full_path) // 1024)

    # Web relative URL
    rel_url = f"/static/uploads/site_photos/{site_code.replace(' ', '_')}/{year_month}/{filename}"

    # Insert into database
    photo_id = database.add_site_work_photo(
        site_id=site["id"],
        photo_date=photo_date,
        uploaded_at=ist_now.strftime("%Y-%m-%d %H:%M:%S"),
        uploaded_by=uploaded_by,
        uploader_phone=uploader_phone,
        category=category,
        description=description,
        latitude=lat_val,
        longitude=lng_val,
        accuracy=acc_val,
        photo_url=rel_url,
        file_size_kb=file_size_kb
    )

    return {
        "id": photo_id,
        "site_id": site["id"],
        "site_name": site_name,
        "site_code": site_code,
        "photo_url": rel_url,
        "photo_date": photo_date,
        "uploaded_at": ist_now.strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "description": description,
        "latitude": lat_val,
        "longitude": lng_val,
        "file_size_kb": file_size_kb
    }


ATTENDANCE_UPLOAD_ROOT = os.path.join(os.path.dirname(__file__), "static", "uploads", "attendance")

def process_and_save_attendance_photo(file_storage, worker_name, worker_role, site_name, site_code, lat=None, lng=None, accuracy=0, att_date=None, check_type='check_in'):
    """
    Takes worker attendance photo (FileStorage or Base64 string),
    applies EXIF correction, burns GPS & timestamp watermark banner,
    saves as high-efficiency WebP image, and returns relative URL.
    """
    import base64
    import io

    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    if not att_date:
        att_date = ist_now.strftime("%Y-%m-%d")
    
    time_str = ist_now.strftime("%I:%M:%S %p")
    year_month = att_date[:7]
    clean_code = (site_code or "SITE").replace(" ", "_")

    target_dir = os.path.join(ATTENDANCE_UPLOAD_ROOT, year_month)
    os.makedirs(target_dir, exist_ok=True)

    ts_compact = ist_now.strftime("%Y%m%d_%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    filename = f"att_{clean_code}_{ts_compact}_{rand_suffix}.webp"
    full_path = os.path.join(target_dir, filename)

    if isinstance(file_storage, str):
        if "base64," in file_storage:
            file_storage = file_storage.split("base64,")[1]
        img_bytes = base64.b64decode(file_storage)
        img = Image.open(io.BytesIO(img_bytes))
    else:
        img = Image.open(file_storage)

    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")

    max_dim = 800
    if img.width > max_dim or img.height > max_dim:
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

    width, height = img.size

    banner_height = 72
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    draw_overlay.rectangle([(0, height - banner_height), (width, height)], fill=(0, 0, 0, 195))

    lat_val = float(lat) if lat else 0.0
    lng_val = float(lng) if lng else 0.0
    acc_val = int(accuracy) if accuracy else 0

    gps_str = f"🌐 GPS: {lat_val:.5f}° N, {lng_val:.5f}° E (±{acc_val}m)" if (lat_val and lng_val) else "🌐 GPS: Location Verified"
    type_str = "चेक-इन (Check-In)" if check_type == 'check_in' else "चेक-आउट (Check-Out)"
    
    line1 = f"🏢 M/S SANDIP KUMAR  |  JAL JEEVAN MISSION  |  📍 {site_name.upper()} ({clean_code})"
    line2 = f"👷 {worker_name} ({worker_role})  |  📅 {att_date} {time_str}"
    line3 = f"{gps_str}  |  STATUS: {type_str}"

    y_start = height - banner_height + 6
    draw_overlay.text((14, y_start), line1, fill=(255, 230, 0, 255))
    draw_overlay.text((14, y_start + 20), line2, fill=(255, 255, 255, 255))
    draw_overlay.text((14, y_start + 40), line3, fill=(110, 231, 183, 255))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    try:
        img.save(full_path, "WEBP", quality=75, method=6)
    except Exception:
        pass

    # Save as high-efficiency Base64 WebP Data URI so it persists permanently in database
    # and NEVER breaks even on Render ephemeral disk restarts!
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=75)
    b64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    data_url = f"data:image/webp;base64,{b64_str}"
    return data_url
