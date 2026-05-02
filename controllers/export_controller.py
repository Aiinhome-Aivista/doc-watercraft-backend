from flask import request, jsonify, send_from_directory
import pandas as pd
from datetime import datetime
import os

from app.db import get_db_connection

EXPORT_FOLDER = "exports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)


def export_full_report():
    try:
        conn = get_db_connection()

        # =========================
        # FILTERS
        # =========================
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

        # =========================
        # 🔥 MASTER QUERY (ALL DATA)
        # =========================
        query = f"""
        SELECT 
            v.vessel_name,
            pm.party_name,
            v.cargo_type,
            v.quantity,
            v.status,

            ge.gate_in_no,
            ge.gate_in_datetime,
            ge.gate_out_datetime,
            ge.direction,

            vm.vehicle_no,

            wr.gross_weight,
            wr.tare_weight,
            (wr.gross_weight - wr.tare_weight) AS net_weight,

            co.operation_type,
            co.start_datetime,
            co.end_datetime,

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

        # =========================
        # KPI SHEET
        # =========================
        kpi = {
            "Total Vessels": df["vessel_name"].nunique(),
            "Total Parties": df["party_name"].nunique(),
            "Total Quantity": df["quantity"].sum(),
            "Total Revenue": df["total_bill_value"].sum()
        }

        df_kpi = pd.DataFrame(list(kpi.items()), columns=["Metric", "Value"])

        # =========================
        # FILE CREATE
        # =========================
        file_name = f"FULL_REPORT_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        file_path = os.path.join(EXPORT_FOLDER, file_name)

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="MASTER_REPORT", index=False)
            df_kpi.to_excel(writer, sheet_name="KPI_SUMMARY", index=False)

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
    return send_from_directory(
        EXPORT_FOLDER,
        filename,
        as_attachment=True
    )