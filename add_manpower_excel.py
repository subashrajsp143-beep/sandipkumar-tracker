# -*- coding: utf-8 -*-
"""
Add generate_manpower_excel to exporter.py
Matches the exact style, red date header, columns and layout of the user's photo.
"""

def patch_exporter():
    with open('exporter.py', 'r', encoding='utf-8') as f:
        content = f.read()

    manpower_excel_func = '''
def generate_manpower_excel(att_date, rows, totals):
    """
    Generates Excel matching the user's photo:
    Top Title: DATE DD/MM/YYYY (Red bold)
    Columns: SL.NO | SITE NAME | SITE INCHARGE | SUPERVISOR | ELECTRICIAN | GI MISTRI | D E O | PLUMBER | HELPER | OTHER | TOTAL | REMARKS
    """
    wb = openpyxl.Workbook()
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
'''

    if 'def generate_manpower_excel' not in content:
        content += '\n' + manpower_excel_func

    with open('exporter.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("exporter.py updated with generate_manpower_excel function!")

if __name__ == '__main__':
    patch_exporter()
