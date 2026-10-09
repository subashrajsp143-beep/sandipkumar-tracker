# -*- coding: utf-8 -*-
"""
Smart OCR & Text Extractor that parses text from uploaded paper slips / handwritten notes
and matches them to materials in the database with high accuracy.
"""

import os
import re
import subprocess
import difflib
import database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OCR_PS1 = os.path.join(BASE_DIR, "ocr_runner.ps1")

def run_native_ocr(image_path):
    """Run Windows Media OCR on image and return list of recognized lines."""
    try:
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", OCR_PS1, "-ImagePath", image_path]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print(f"OCR Error: {e}")
        return []

def extract_quantities_and_materials(ocr_lines):
    """
    Intelligently match OCR text lines or raw text against the master materials in SQLite.
    Accurately separates fraction sizes (1/2", 3/4") from actual quantities (5, 50 mtr).
    """
    materials = database.get_all_materials()
    results = []
    used_mat_ids = set()

    for line in ocr_lines:
        line_clean = line.strip()
        if len(line_clean) < 2:
            continue

        qty = 1.0
        text_part = line_clean

        # Pattern 1: Dash or colon followed by number: "- 5 pic", "- 50 mtr", "- 5", ": 10"
        m_dash = re.search(r'[-:=]\s*(\d+(?:\.\d+)?)\s*(?:pic|pcs|piece|mtr|meter|nos|no|pkt|packet)?\b', line_clean, re.IGNORECASE)
        if m_dash:
            qty = float(m_dash.group(1))
            text_part = line_clean[:m_dash.start()].strip()
        else:
            # Pattern 2: Number followed by unit: "50 mtr", "5 pic", "10 pcs"
            m_unit = re.search(r'\b(\d+(?:\.\d+)?)\s*(?:pic|pcs|piece|mtr|meter|nos|no|pkt|packet)\b', line_clean, re.IGNORECASE)
            if m_unit:
                qty = float(m_unit.group(1))
                text_part = (line_clean[:m_unit.start()] + " " + line_clean[m_unit.end():]).strip()
            else:
                # Pattern 3: Number at the end of the line (e.g. "Teflon tape 5")
                m_end = re.search(r'\b(\d+(?:\.\d+)?)\s*$', line_clean)
                if m_end:
                    # Make sure it's not a fraction denominator like 1/2
                    start_idx = m_end.start()
                    if start_idx > 0 and line_clean[start_idx-1] not in ['/', '*', 'x', 'X']:
                        qty = float(m_end.group(1))
                        text_part = line_clean[:start_idx].strip()

        # Clean text_part for matching
        text_upper = text_part.upper()
        # Normalize common abbreviations
        text_upper = text_upper.replace('MDPE', 'MDPE').replace('UPVC', 'UPVC').replace('CPVC', 'CPVC').replace('HDPE', 'HDPE')
        text_tokens = set([t for t in re.split(r'[\s\-]+', text_upper) if t and t not in ['PIC', 'PCS', 'PIECE', 'MTR', 'METER', 'NOS', 'NO']])

        best_match = None
        best_score = 0.0

        for mat in materials:
            mat_upper = mat["name"].upper()
            mat_tokens = set([t for t in re.split(r'[\s\-]+', mat_upper) if t])

            # 1. Exact token set equality (e.g., {'UPVC', 'FTA', '1/2"'} == {'1/2"', 'UPVC', 'FTA'})
            if text_tokens and mat_tokens == text_tokens:
                score = 1.0
            # 2. Complete subset
            elif text_tokens and text_tokens.issubset(mat_tokens):
                score = 0.92
            elif mat_tokens and mat_tokens.issubset(text_tokens):
                score = 0.90
            else:
                # 3. Token overlap ratio
                common = mat_tokens.intersection(text_tokens)
                if common:
                    overlap_ratio = len(common) / max(len(mat_tokens), len(text_tokens))
                    seq_ratio = difflib.SequenceMatcher(None, mat_upper, text_upper).ratio()
                    score = (overlap_ratio * 0.75) + (seq_ratio * 0.25)
                else:
                    score = difflib.SequenceMatcher(None, mat_upper, text_upper).ratio() * 0.5

            if score > best_score and score >= 0.50:
                best_score = score
                best_match = mat

        if best_match and best_match["id"] not in used_mat_ids:
            used_mat_ids.add(best_match["id"])
            results.append({
                "material_id": best_match["id"],
                "material_name": best_match["name"],
                "unit": best_match["unit"],
                "rate": best_match["rate"],
                "quantity": qty,
                "amount": round(qty * best_match["rate"], 2),
                "confidence": round(best_score * 100, 1),
                "original_text": line_clean
            })

    return results
