from flask import request, jsonify, send_from_directory
import pandas as pd
from datetime import datetime
import os

from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from database.db_connection import get_db_connection

EXPORT_FOLDER = "exports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)


def export_full_report():
    try:
        conn = get_db_connection()

        # ================= FILTERS =================
        party_id = request.args.get("party_id")
        vessel_id = request.args.get("vessel_id")
        start = request.args.get("period_start")
        end = request.args.get("period_end")

        conditions = []
        params = []

        if party_id:
            conditions.append("v.party_id = %s")
            params.append(party_id)

        if vessel_id:
            conditions.append("v.id = %s")
            params.append(vessel_id)

        if start and end:
            conditions.append("DATE(v.created_at) BETWEEN %s AND %s")
            params.extend([start, end])

        where = " AND ".join(conditions)
        if where:
            where = "WHERE " + where

        # ================= QUERY =================
        query = f"""
        SELECT 
    v.vessel_name,
    pm.party_name,

    ge.gate_in_datetime,
    ge.gate_out_datetime,
    vm.vehicle_no,

    wr.gross_weight,
    wr.tare_weight,
    (wr.gross_weight - wr.tare_weight) AS net_weight,

    co.start_datetime,
    co.end_datetime,

    -- BILLING
    bm.voucher_number,
    bm.bill_date,
    bm.total_bill_value,

    bd.activity_name,
    bd.qty,
    bd.rate,
    bd.amount,
    bd.gst_amount

FROM vessels v
LEFT JOIN party_masters pm ON pm.id = v.party_id
LEFT JOIN gate_entries ge ON ge.party_id = v.party_id
LEFT JOIN vehicle_master vm ON vm.id = ge.vehicle_id
LEFT JOIN wbin_records wr ON wr.gate_entry_id = ge.id
LEFT JOIN cargo_operations co ON co.vessel_id = v.id
LEFT JOIN bill_details bd ON bd.vessel_id = v.id
LEFT JOIN bill_main bm ON bm.id = bd.bill_main_id
        {where}
        """

        df = pd.read_sql(query, conn, params=params)

        # ================= COLUMN RENAME =================
        df.columns = [
    "Vessel",
    "Party",
    "Gate In",
    "Gate Out",
    "Vehicle",
    "Gross",
    "Tare",
    "Net",
    "Start",
    "End",

    # BILLING
    "Voucher",
    "Bill Date",
    "Total Bill",
    "Activity",
    "Qty",
    "Rate",
    "Amount",
    "GST"
]

        # ================= FILE =================
        file_name = f"REPORT_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        file_path = os.path.join(EXPORT_FOLDER, file_name)

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="REPORT", index=False, startrow=4)

            ws = writer.book["REPORT"]

            # ================= HEADER =================
            ws.merge_cells("A1:K1")
            ws["A1"] = df["Vessel"].iloc[0] if not df.empty else "VESSEL REPORT"
            ws["A1"].font = Font(size=14, bold=True)
            ws["A1"].alignment = Alignment(horizontal="center")

            ws.merge_cells("A2:K2")
            ws["A2"] = "Daily Loading & Unloading Data"
            ws["A2"].alignment = Alignment(horizontal="center")

            # ================= STYLES =================
            header_font = Font(bold=True)
            center_align = Alignment(horizontal="center")
            yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

            thin_border = Border(
                left=Side(style="thin"),
                right=Side(style="thin"),
                top=Side(style="thin"),
                bottom=Side(style="thin")
            )

            # Header styling
            for col in range(1, len(df.columns) + 1):
                cell = ws.cell(row=5, column=col)
                cell.font = header_font
                cell.alignment = center_align
                cell.border = thin_border

            # ================= HIGHLIGHT (LIKE YOUR SHEET) =================
            net_col = df.columns.get_loc("Net") + 1

            for row in range(6, ws.max_row + 1):
                ws.cell(row=row, column=net_col).fill = yellow_fill

            # ================= AUTO WIDTH =================
            for col in ws.columns:
                max_length = 0
                col_letter = get_column_letter(col[0].column)

                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass

                ws.column_dimensions[col_letter].width = max_length + 2

            # ================= TOTAL =================
            total_row = ws.max_row + 2
            ws[f"H{total_row}"] = "Total Net:"
            ws[f"I{total_row}"] = df["Net"].sum()

            ws[f"H{total_row}"].font = Font(bold=True)
            ws[f"I{total_row}"].font = Font(bold=True)

        conn.close()

        return jsonify({
            "success": True,
            "download_url": f"/api/v1/export/download/{file_name}"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


def download_export(filename):
    return send_from_directory(EXPORT_FOLDER, filename, as_attachment=True)