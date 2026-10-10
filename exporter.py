# -*- coding: utf-8 -*-
"""
Excel export utility using openpyxl for clean, professional reports.
"""

import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Calibri", size=14, bold=True, color="1E3A8A")
SUBTITLE_FONT = Font(name="Calibri", size=10, italic=True, color="4B5563")
BOLD_FONT = Font(name="Calibri", size=11, bold=True)
REGULAR_FONT = Font(name="Calibri", size=10)
TOTAL_FILL = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")

THIN_BORDER = Border(
    left=Side(style='thin', color='D1D5DB'),
    right=Side(style='thin', color='D1D5DB'),
    top=Side(style='thin', color='D1D5DB'),
    bottom=Side(style='thin', color='D1D5DB')
)

def style_header_row(ws, row_num):
    for cell in ws[row_num]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER

def auto_fit_columns(ws, max_cols=20):
    for col in range(1, min(ws.max_column + 1, max_cols + 1)):
        col_letter = get_column_letter(col)
        max_len = 0
        for cell in ws[col_letter]:
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

def generate_site_report_excel(site_name, entries, material_summary, from_date=None, to_date=None):
    wb = Workbook()
    
    # Sheet 1: Material Consumption Summary
    ws_sum = wb.active
    ws_sum.title = "Material Summary"

    ws_sum.append(["SITE MATERIAL CONSUMPTION REPORT"])
    ws_sum.cell(1, 1).font = TITLE_FONT
    
    date_info = f"Date Range: {from_date or 'Start'} to {to_date or 'Present'}"
    ws_sum.append([f"Site: {site_name} | {date_info}"])
    ws_sum.cell(2, 1).font = SUBTITLE_FONT
    ws_sum.append([])

    headers = ["S.No.", "Material Name", "Category", "Total Quantity", "Unit", "Avg Rate (₹)", "Total Amount (₹)"]
    ws_sum.append(headers)
    style_header_row(ws_sum, 4)

    total_cost = 0
    row_idx = 5
    for i, item in enumerate(material_summary, start=1):
        amt = item["total_amount"] or 0
        total_cost += amt
        ws_sum.append([
            i,
            item["material_name"],
            item["category"] or "-",
            item["total_quantity"],
            item["material_unit"],
            round(item["avg_rate"], 2) if item["avg_rate"] else 0,
            round(amt, 2)
        ])
        for c in range(1, 8):
            cell = ws_sum.cell(row_idx, c)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            if c in [1, 5]:
                cell.alignment = Alignment(horizontal="center")
            elif c in [4, 6, 7]:
                cell.alignment = Alignment(horizontal="right")
        row_idx += 1

    # Total Row
    ws_sum.append(["", "GRAND TOTAL", "", "", "", "", round(total_cost, 2)])
    ws_sum.cell(row_idx, 2).font = BOLD_FONT
    ws_sum.cell(row_idx, 7).font = BOLD_FONT
    for c in range(1, 8):
        cell = ws_sum.cell(row_idx, c)
        cell.fill = TOTAL_FILL
        cell.border = THIN_BORDER
        if c == 7:
            cell.alignment = Alignment(horizontal="right")

    auto_fit_columns(ws_sum)

    # Sheet 2: Daily Log History
    ws_log = wb.create_sheet(title="Daily Logs")
    ws_log.append(["DAILY MATERIAL USAGE LOG HISTORY"])
    ws_log.cell(1, 1).font = TITLE_FONT
    ws_log.append([f"Site: {site_name} | Total Logs: {len(entries)}"])
    ws_log.cell(2, 1).font = SUBTITLE_FONT
    ws_log.append([])

    log_headers = ["S.No.", "Date", "Material Name", "Quantity", "Unit", "Rate (₹)", "Amount (₹)", "Work / Purpose", "Supervisor", "Remarks"]
    ws_log.append(log_headers)
    style_header_row(ws_log, 4)

    log_row = 5
    for i, e in enumerate(entries, start=1):
        ws_log.append([
            i,
            e["usage_date"],
            e["material_name"],
            e["quantity"],
            e["material_unit"],
            e["rate"],
            e["total_amount"],
            e["purpose"] or "",
            e["entered_by"] or "",
            e["remarks"] or ""
        ])
        for c in range(1, 11):
            cell = ws_log.cell(log_row, c)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            if c in [1, 2, 5]:
                cell.alignment = Alignment(horizontal="center")
            elif c in [4, 6, 7]:
                cell.alignment = Alignment(horizontal="right")
        log_row += 1

    auto_fit_columns(ws_log)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def generate_daily_report_excel(report_date, entries, site_summaries):
    wb = Workbook()
    ws = wb.active
    ws.title = f"Daily Report {report_date}"

    ws.append([f"DAILY MATERIAL CONSUMPTION REPORT - {report_date}"])
    ws.cell(1, 1).font = TITLE_FONT
    ws.append([f"Consolidated 19 Sites Report for Date: {report_date}"])
    ws.cell(2, 1).font = SUBTITLE_FONT
    ws.append([])

    headers = ["S.No.", "Site Code", "Site Name", "Material Name", "Quantity", "Unit", "Rate (₹)", "Amount (₹)", "Work / Purpose", "Supervisor"]
    ws.append(headers)
    style_header_row(ws, 4)

    row_idx = 5
    total_val = 0
    for i, e in enumerate(entries, start=1):
        total_val += (e["total_amount"] or 0)
        ws.append([
            i,
            e["site_code"],
            e["site_name"],
            e["material_name"],
            e["quantity"],
            e["material_unit"],
            e["rate"],
            e["total_amount"],
            e["purpose"] or "",
            e["entered_by"] or ""
        ])
        for c in range(1, 11):
            cell = ws.cell(row_idx, c)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            if c in [1, 2, 6]:
                cell.alignment = Alignment(horizontal="center")
            elif c in [5, 7, 8]:
                cell.alignment = Alignment(horizontal="right")
        row_idx += 1

    # Total row
    ws.append(["", "", "GRAND TOTAL", "", "", "", "", round(total_val, 2), "", ""])
    ws.cell(row_idx, 3).font = BOLD_FONT
    ws.cell(row_idx, 8).font = BOLD_FONT
    for c in range(1, 11):
        cell = ws.cell(row_idx, c)
        cell.fill = TOTAL_FILL
        cell.border = THIN_BORDER

    auto_fit_columns(ws)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def generate_monthly_report_excel(month_str, entries, site_summaries, top_materials):
    wb = Workbook()

    # Sheet 1: 19 Sites Monthly Summary
    ws_sites = wb.active
    ws_sites.title = "Sites Monthly Summary"

    ws_sites.append(["M/S SANDIP KUMAR - MONTHLY MATERIAL EXPENSE REPORT"])
    ws_sites.cell(1, 1).font = TITLE_FONT
    ws_sites.append([f"Report Month: {month_str} | Total Sites: {len(site_summaries)}"])
    ws_sites.cell(2, 1).font = SUBTITLE_FONT
    ws_sites.append([])

    headers_sites = ["#", "Site Code", "Site Name", "Supervisor", "Contact", "Items Count", "Total Monthly Amount (₹)"]
    ws_sites.append(headers_sites)
    style_header_row(ws_sites, 4)

    row_idx = 5
    total_sites_val = 0
    total_sites_items = 0
    for i, s in enumerate(site_summaries, start=1):
        cost = s["site_total_cost"] or 0
        total_sites_val += cost
        items_cnt = s["items_count"] or 0
        total_sites_items += items_cnt
        ws_sites.append([
            i,
            s["code"],
            s["name"],
            s.get("supervisor", "") or "",
            s.get("contact", "") or "",
            items_cnt,
            cost
        ])
        for c in range(1, 8):
            cell = ws_sites.cell(row_idx, c)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            if c in [1, 2]:
                cell.alignment = Alignment(horizontal="center")
            elif c in [6, 7]:
                cell.alignment = Alignment(horizontal="right")
        row_idx += 1

    # Total row
    ws_sites.append(["", "", "GRAND TOTAL", "", "", total_sites_items, round(total_sites_val, 2)])
    ws_sites.cell(row_idx, 3).font = BOLD_FONT
    ws_sites.cell(row_idx, 6).font = BOLD_FONT
    ws_sites.cell(row_idx, 7).font = BOLD_FONT
    for c in range(1, 8):
        cell = ws_sites.cell(row_idx, c)
        cell.fill = TOTAL_FILL
        cell.border = THIN_BORDER
    auto_fit_columns(ws_sites)

    # Sheet 2: Top Materials Consumed
    ws_mats = wb.create_sheet(title="Top Materials")
    ws_mats.append(["TOP MATERIALS CONSUMED THIS MONTH"])
    ws_mats.cell(1, 1).font = TITLE_FONT
    ws_mats.append([f"Month: {month_str}"])
    ws_mats.cell(2, 1).font = SUBTITLE_FONT
    ws_mats.append([])

    headers_mats = ["#", "Material Name", "Category", "Unit", "Total Qty Consumed", "Total Amount (₹)"]
    ws_mats.append(headers_mats)
    style_header_row(ws_mats, 4)

    row_m = 5
    for i, m in enumerate(top_materials, start=1):
        ws_mats.append([
            i,
            m["material_name"],
            m.get("category", ""),
            m["material_unit"],
            m["total_quantity"],
            m["total_cost"]
        ])
        for c in range(1, 7):
            cell = ws_mats.cell(row_m, c)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            if c in [1, 4]:
                cell.alignment = Alignment(horizontal="center")
            elif c in [5, 6]:
                cell.alignment = Alignment(horizontal="right")
        row_m += 1
    auto_fit_columns(ws_mats)

    # Sheet 3: Detailed Entries Log
    ws_entries = wb.create_sheet(title="All Transactions")
    ws_entries.append(["MONTHLY DETAILED CONSUMPTION TRANSACTIONS"])
    ws_entries.cell(1, 1).font = TITLE_FONT
    ws_entries.append([f"Month: {month_str} | Total Records: {len(entries)}"])
    ws_entries.cell(2, 1).font = SUBTITLE_FONT
    ws_entries.append([])

    headers_entries = ["#", "Date", "Site Code", "Site Name", "Material Description", "Qty", "Unit", "Rate (₹)", "Amount (₹)", "Purpose / Work", "Supervisor"]
    ws_entries.append(headers_entries)
    style_header_row(ws_entries, 4)

    row_e = 5
    total_entry_val = 0
    for i, e in enumerate(entries, start=1):
        total_entry_val += (e["total_amount"] or 0)
        ws_entries.append([
            i,
            e["usage_date"],
            e["site_code"],
            e["site_name"],
            e["material_name"],
            e["quantity"],
            e["material_unit"],
            e["rate"],
            e["total_amount"],
            e.get("purpose", "") or "",
            e.get("entered_by", "") or ""
        ])
        for c in range(1, 12):
            cell = ws_entries.cell(row_e, c)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            if c in [1, 2, 3, 7]:
                cell.alignment = Alignment(horizontal="center")
            elif c in [6, 8, 9]:
                cell.alignment = Alignment(horizontal="right")
        row_e += 1

    ws_entries.append(["", "", "", "GRAND TOTAL", "", "", "", "", round(total_entry_val, 2), "", ""])
    ws_entries.cell(row_e, 4).font = BOLD_FONT
    ws_entries.cell(row_e, 9).font = BOLD_FONT
    for c in range(1, 12):
        cell = ws_entries.cell(row_e, c)
        cell.fill = TOTAL_FILL
        cell.border = THIN_BORDER
    auto_fit_columns(ws_entries)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output


def generate_manpower_excel(att_date, rows, totals):
    """
    Generates Excel matching the user's photo:
    Top Title: DATE DD/MM/YYYY (Red bold)
    Columns: SL.NO | SITE NAME | SITE INCHARGE | SUPERVISOR | ELECTRICIAN | GI MISTRI | D E O | PLUMBER | HELPER | OTHER | TOTAL | REMARKS
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Daily Manpower"
    ws.views.sheetView[0].showGridLines = True

    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )
    double_bottom_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='double', color='000000')
    )

    # Format date: YYYY-MM-DD -> DD/MM/YYYY
    try:
        parts = att_date.split('-')
        if len(parts) == 3:
            formatted_date = f"{parts[2]}/{parts[1]}/{parts[0]}"
        else:
            formatted_date = att_date
    except:
        formatted_date = att_date

    # Row 1: Big Centered Red Date Header (Merged across columns C to K)
    ws.row_dimensions[1].height = 28
    ws.merge_cells("A1:L1")
    title_cell = ws["A1"]
    title_cell.value = f"DATE {formatted_date}"
    title_cell.font = Font(name="Calibri", size=16, bold=True, color="FF0000") # Red
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    for col in range(1, 13):
        ws.cell(row=1, column=col).border = thin_border

    # Row 2: Table Column Headers (matching photo exactly)
    headers = [
        "SL.NO", "SITE NAME", "SITE INCHARGE", "SUPERVISOR",
        "ELECTRICIAN", "GI MISTRI", "D E O", "PLUMBER",
        "HELPER", "OTHER", "TOTAL", "REMARKS"
    ]
    ws.row_dimensions[2].height = 24
    for col_idx, h in enumerate(headers, start=1):
        c = ws.cell(row=2, column=col_idx, value=h)
        c.font = Font(name="Calibri", size=10, bold=True, color="000000")
        c.fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border

    # Data Rows
    current_row = 3
    for idx, r in enumerate(rows, start=1):
        ws.row_dimensions[current_row].height = 20

        # Numbers: display blank if 0, matching the photo style
        def fmt_val(v):
            return v if v > 0 else ""

        row_vals = [
            idx,
            r["site_name"].upper(),
            fmt_val(r["site_incharge"]),
            fmt_val(r["supervisor"]),
            fmt_val(r["electrician"]),
            fmt_val(r["gi_mistri"]),
            fmt_val(r["deo"]),
            fmt_val(r["plumber"]),
            fmt_val(r["helper"]),
            fmt_val(r["other"]),
            r["total"] if r["total"] > 0 else "",
            r["remarks"].upper() if r["remarks"] else ""
        ]

        for col_idx, val in enumerate(row_vals, start=1):
            c = ws.cell(row=current_row, column=col_idx, value=val)
            c.border = thin_border
            
            # Formatting
            if col_idx == 1:
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.font = Font(name="Calibri", size=10)
            elif col_idx == 2:
                c.alignment = Alignment(horizontal="left", vertical="center")
                c.font = Font(name="Calibri", size=10, bold=False)
            elif col_idx == 11: # Total
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.font = Font(name="Calibri", size=10, bold=True)
            elif col_idx == 12: # Remarks
                c.alignment = Alignment(horizontal="left", vertical="center")
                c.font = Font(name="Calibri", size=9, bold=True, color="000000")
            else: # Count columns
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.font = Font(name="Calibri", size=10, bold=(val != ""))

        current_row += 1

    # Bottom Grand Total Row
    ws.row_dimensions[current_row].height = 24
    total_vals = [
        "", "TOTAL",
        totals.get("site_incharge", 0),
        totals.get("supervisor", 0),
        totals.get("electrician", 0),
        totals.get("gi_mistri", 0),
        totals.get("deo", 0),
        totals.get("plumber", 0),
        totals.get("helper", 0),
        totals.get("other", 0),
        totals.get("total", 0),
        ""
    ]
    for col_idx, val in enumerate(total_vals, start=1):
        c = ws.cell(row=current_row, column=col_idx, value=val)
        c.font = Font(name="Calibri", size=10, bold=True, color="000000")
        c.fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
        c.border = double_bottom_border
        if col_idx == 2:
            c.alignment = Alignment(horizontal="center", vertical="center")
        else:
            c.alignment = Alignment(horizontal="center", vertical="center")

    # Column Widths
    col_widths = {
        1: 8,   # SL.NO
        2: 18,  # SITE NAME
        3: 15,  # SITE INCHARGE
        4: 14,  # SUPERVISOR
        5: 14,  # ELECTRICIAN
        6: 12,  # GI MISTRI
        7: 10,  # D E O
        8: 11,  # PLUMBER
        9: 11,  # HELPER
        10: 10, # OTHER
        11: 10, # TOTAL
        12: 36  # REMARKS
    }
    for col_idx, w in col_widths.items():
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = w

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output
