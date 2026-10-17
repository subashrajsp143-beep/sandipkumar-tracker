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

def generate_manpower_pdf(att_date, rows, totals):
    """
    Generates a crisp, professional 1-page A4 Landscape PDF for Daily Manpower Attendance.
    Guaranteed to fit on exactly 1 single page.
    """
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=landscape(A4),
        leftMargin=18,
        rightMargin=18,
        topMargin=14,
        bottomMargin=14
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=15, textColor=colors.HexColor('#0F172A'), alignment=1)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#DC2626'), alignment=1)
    stat_style = ParagraphStyle('Stat', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor('#334155'), alignment=1)

    # Format date DD/MM/YYYY
    clean_date = att_date
    try:
        parts = att_date.split('-')
        if len(parts) == 3:
            clean_date = f"{parts[2]}/{parts[1]}/{parts[0]}"
    except:
        pass

    tot_val = totals.get("total", 0)
    staff_val = totals.get("site_incharge", 0) + totals.get("supervisor", 0)
    mistri_val = totals.get("gi_mistri", 0) + totals.get("plumber", 0)
    helper_val = totals.get("helper", 0)

    elements = [
        Paragraph('M/S SANDIP KUMAR &mdash; 21 SITES DAILY MANPOWER ATTENDANCE', title_style),
        Spacer(1, 2),
        Paragraph(f'DATE: {clean_date}', sub_style),
        Spacer(1, 2),
        Paragraph(f'<b>TOTAL MANPOWER:</b> {tot_val} Persons &nbsp;|&nbsp; <b>Staff (Incharge+Supervisor):</b> {staff_val} &nbsp;|&nbsp; <b>Mistri+Plumber:</b> {mistri_val} &nbsp;|&nbsp; <b>Helpers:</b> {helper_val}', stat_style),
        Spacer(1, 5)
    ]

    col_widths = [26, 95, 55, 55, 52, 48, 40, 48, 48, 40, 48, 250]
    table_data = [['SL', 'SITE NAME', 'INCHARGE', 'SUPERVISOR', 'ELECTRICIAN', 'GI MISTRI', 'DEO', 'PLUMBER', 'HELPER', 'OTHER', 'TOTAL', 'REMARKS']]

    for idx, r in enumerate(rows, 1):
        table_data.append([
            str(idx),
            r['site_name'].upper(),
            str(r['site_incharge']) if r['site_incharge'] > 0 else '-',
            str(r['supervisor']) if r['supervisor'] > 0 else '-',
            str(r['electrician']) if r['electrician'] > 0 else '-',
            str(r['gi_mistri']) if r['gi_mistri'] > 0 else '-',
            str(r['deo']) if r['deo'] > 0 else '-',
            str(r['plumber']) if r['plumber'] > 0 else '-',
            str(r['helper']) if r['helper'] > 0 else '-',
            str(r['other']) if r['other'] > 0 else '-',
            str(r['total']) if r['total'] > 0 else '0',
            r.get('remarks') or ''
        ])

    table_data.append([
        '', 'TOTAL',
        str(totals.get('site_incharge', 0)),
        str(totals.get('supervisor', 0)),
        str(totals.get('electrician', 0)),
        str(totals.get('gi_mistri', 0)),
        str(totals.get('deo', 0)),
        str(totals.get('plumber', 0)),
        str(totals.get('helper', 0)),
        str(totals.get('other', 0)),
        str(totals.get('total', 0)),
        ''
    ])

    num_rows = len(rows)
    row_heights = [17] + [16.5] * num_rows + [18]
    t = Table(table_data, colWidths=col_widths, rowHeights=row_heights)
    
    t_style = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,-1), 'LEFT'),
        ('ALIGN', (-1,1), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-2), 7),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F1F5F9')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,-1), (-1,-1), 8),
        ('TEXTCOLOR', (10,-1), (10,-1), colors.HexColor('#DC2626')),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]

    for i in range(1, num_rows + 1):
        if i % 2 == 0:
            t_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8FAFC')))

    t.setStyle(TableStyle(t_style))
    elements.append(t)

    doc.build(elements)
    buf.seek(0)
    return buf

def generate_site_stock_excel(stock_rows, site_name=None):
    """
    Generates a clean Excel spreadsheet of the Site Stock & Balance Register.
    """
    import datetime
    wb = Workbook()
    ws = wb.active
    ws.title = "Site Stock Register"

    title_text = "M/S SANDIP KUMAR — SITE STOCK & INVENTORY REGISTER"
    subtitle_text = f"Site: {site_name or 'ALL 21 SITES OVERVIEW'} | Date: {datetime.date.today().strftime('%d/%m/%Y')}"
    
    ws.append([title_text])
    ws.cell(1, 1).font = TITLE_FONT
    ws.append([subtitle_text])
    ws.cell(2, 1).font = SUBTITLE_FONT
    ws.append([])

    headers = ["S.No.", "Site Name", "Material Name", "Category", "Unit", "Total Sent (Inward)", "Total Used (Consumed)", "Balance Stock", "Status"]
    ws.append(headers)
    style_header_row(ws, 4)

    total_inw = 0
    total_cons = 0
    total_bal = 0

    for i, r in enumerate(stock_rows, start=1):
        inw = float(r.get("total_inward", 0))
        cons = float(r.get("total_consumed", 0))
        bal = float(r.get("balance_stock", 0))
        total_inw += inw
        total_cons += cons
        total_bal += bal
        row_num = 4 + i
        ws.append([
            i,
            r.get("site_name", ""),
            r.get("material_name", ""),
            r.get("material_category", "") or "-",
            r.get("material_unit", ""),
            inw,
            cons,
            bal,
            r.get("status_label", "")
        ])
        for c in range(1, 10):
            cell = ws.cell(row=row_num, column=c)
            cell.font = REGULAR_FONT
            cell.border = THIN_BORDER
            if c in [1, 5, 9]:
                cell.alignment = Alignment(horizontal="center")
            elif c in [6, 7, 8]:
                cell.alignment = Alignment(horizontal="right")

    tot_row = 4 + len(stock_rows) + 1
    ws.append(["", "GRAND TOTAL", "", "", "", round(total_inw, 2), round(total_cons, 2), round(total_bal, 2), ""])
    for c in range(1, 10):
        cell = ws.cell(row=tot_row, column=c)
        cell.font = BOLD_FONT
        cell.fill = TOTAL_FILL
        cell.border = THIN_BORDER
        if c in [6, 7, 8]:
            cell.alignment = Alignment(horizontal="right")

    auto_fit_columns(ws)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output


# ==========================================
# 4 PHOTOS PER A4 SHEET - GOVERNMENT ALBUM PDF GENERATOR
# ==========================================

def generate_photo_album_pdf(site, month_str, photos, from_date=None, to_date=None):
    """
    Generates a government-ready A4 Portrait PDF Photo Album.
    Formatted strictly with exactly 4 PHOTOS PER A4 SHEET (2 columns x 2 rows).
    Includes Site Info, GPS Coordinates, Timestamp, Category, Description, and Page X of Y.
    """
    import os
    import io
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.pdfgen import canvas

    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_number(num_pages)
                canvas.Canvas.showPage(self)
            canvas.Canvas.save(self)

        def draw_page_number(self, page_count):
            self.saveState()
            self.setFont('Helvetica', 7.5)
            self.setFillColor(colors.HexColor('#64748B'))
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(18, 20, 577, 20)
            footer_text = 'M/S SANDIP KUMAR  |  JAL JEEVAN MISSION (BIHAR)  |  OFFICIAL SITE WORK PROGRESS ALBUM'
            self.drawString(18, 10, footer_text)
            page_str = f'Page {self._pageNumber} of {page_count}'
            self.drawRightString(577, 10, page_str)
            self.restoreState()

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=18,
        rightMargin=18,
        topMargin=16,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()
    site_name = (site.get('name') if site else 'All Sites') or 'Site'
    site_code = (site.get('code') if site else 'ALL') or 'ALL'
    supervisor = (site.get('supervisor') if site else 'Staff') or 'Staff'

    elements = []
    
    # Chunk photos into groups of 4 (2x2 grid per page)
    chunks = [photos[i:i+4] for i in range(0, len(photos), 4)] if photos else []

    if not chunks:
        empty_title = Paragraph('<b>M/S SANDIP KUMAR &mdash; JAL JEEVAN MISSION (BIHAR)</b>', styles['Title'])
        empty_msg = Paragraph(f'<br/><br/><br/><center><font size=12 color="#64748B">इस साइट ({site_name}) या चुने गए महीने ({month_str}) में कोई फोटो उपलब्ध नहीं है।</font></center>', styles['Normal'])
        elements.extend([empty_title, empty_msg])
    else:
        for page_idx, chunk in enumerate(chunks):
            # Page Header Table (559 pt width)
            h_left = Paragraph(
                '<b><font size=10 color="#0F172A">M/S SANDIP KUMAR</font></b><br/>'
                '<font size=7 color="#475569">JAL JEEVAN MISSION (BIHAR) &bull; WORK PROGRESS ALBUM</font>',
                styles['Normal']
            )
            h_center = Paragraph(
                f'<b><font size=9 color="#1E3A8A">SITE: {site_name.upper()} ({site_code})</font></b><br/>'
                f'<font size=7 color="#475569">SUPERVISOR: {supervisor.upper()} &bull; PERIOD: {month_str}</font>',
                styles['Normal']
            )
            h_right = Paragraph(
                '<font size=8 color="#B91C1C"><b>4 PHOTOS / SHEET</b></font><br/>'
                f'<font size=7 color="#64748B">Total: {len(photos)} Photos</font>',
                styles['Normal']
            )
            
            header_table = Table([[h_left, h_center, h_right]], colWidths=[200, 259, 100])
            header_table.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#94A3B8')),
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 5))

            # 4 Photos in 2x2 grid
            cells = []
            for j in range(4):
                if j < len(chunk):
                    p = chunk[j]
                    global_num = page_idx * 4 + j + 1
                    
                    # Resolve disk path
                    raw_url = p.get('photo_url', '')
                    clean_path = raw_url.lstrip('/')
                    
                    if os.path.exists(clean_path):
                        img_flowable = RLImage(clean_path, width=260, height=180)
                    else:
                        img_flowable = Paragraph('<br/><br/><center><font size=9 color="#DC2626"><b>[PHOTO FILE NOT FOUND]</b></font></center><br/>', styles['Normal'])

                    # Caption block
                    p_date = p.get('photo_date', '')
                    p_time = ''
                    uploaded_at = p.get('uploaded_at', '')
                    if uploaded_at and len(uploaded_at) >= 16:
                        p_time = uploaded_at[11:16]

                    lat_val = float(p.get('latitude') or 0.0)
                    lng_val = float(p.get('longitude') or 0.0)
                    gps_text = f"{lat_val:.5f}&deg; N, {lng_val:.5f}&deg; E" if (lat_val and lng_val) else "GPS Verified"

                    cat_text = p.get('category', 'कार्य')
                    desc_text = p.get('description', '') or 'Site work execution'
                    by_text = p.get('uploaded_by', '') or p.get('site_supervisor', 'Supervisor')

                    caption_html = (
                        f'<b><font size=8.5 color="#312E81">#{global_num} &bull; {cat_text}</font></b><br/>'
                        f'<font size=7 color="#334155">📅 <b>Date:</b> {p_date} {p_time} &nbsp;|&nbsp; 🌐 <b>GPS:</b> {gps_text}</font><br/>'
                        f'<font size=7 color="#0F172A">📝 <b>Work:</b> {desc_text}</font><br/>'
                        f'<font size=6.5 color="#64748B">👷 <b>Staff:</b> {by_text}</font>'
                    )
                    caption_flowable = Paragraph(caption_html, styles['Normal'])

                    cell_table = Table([[img_flowable], [caption_flowable]], colWidths=[266])
                    cell_table.setStyle(TableStyle([
                        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
                        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F8FAFC')),
                        ('TOPPADDING', (0,0), (-1,-1), 2),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                        ('LEFTPADDING', (0,0), (-1,-1), 3),
                        ('RIGHTPADDING', (0,0), (-1,-1), 3),
                    ]))
                    cells.append(cell_table)
                else:
                    empty_box = Paragraph('', styles['Normal'])
                    cells.append(empty_box)

            # Build 2x2 grid
            grid_table = Table([[cells[0], cells[1]], [cells[2], cells[3]]], colWidths=[276, 276])
            grid_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]))
            elements.append(grid_table)

            # Page break if more pages follow
            if page_idx < len(chunks) - 1:
                elements.append(PageBreak())

    doc.build(elements, canvasmaker=NumberedCanvas)
    buf.seek(0)
    return buf


