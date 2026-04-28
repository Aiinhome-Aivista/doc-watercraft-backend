from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


def generate_invoice_pdf(data, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # =========================
    # 🔹 HEADER (COMPANY)
    # =========================
    elements.append(Paragraph("<b>YOUR COMPANY NAME</b>", styles['Title']))
    elements.append(Paragraph("Port Logistics Billing System", styles['Normal']))
    elements.append(Paragraph("GSTIN: XXXXXXXX", styles['Normal']))
    elements.append(Spacer(1, 12))

    # =========================
    # 🔹 INVOICE INFO
    # =========================
    elements.append(Paragraph("<b>TAX INVOICE</b>", styles['Heading2']))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(f"Voucher No: {data['voucher_number']}", styles['Normal']))
    elements.append(Paragraph(f"Party: {data.get('party_name', '')}", styles['Normal']))
    elements.append(Paragraph(f"Period: {data['period_start']} to {data['period_end']}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # =========================
    # 🔹 GROUP BY VESSEL
    # =========================
    vessel_map = {}

    for d in data["details"]:
        vessel = d.get("vessel_name", f"Vessel {d['vessel_id']}")
        vessel_map.setdefault(vessel, []).append(d)

    # =========================
    # 🔹 TABLE PER VESSEL
    # =========================
    grand_total = 0

    for vessel_name, items in vessel_map.items():

        elements.append(Paragraph(f"<b>Vessel: {vessel_name}</b>", styles['Heading3']))
        elements.append(Spacer(1, 6))

        table_data = [["Activity", "Qty", "Rate", "Amount", "GST"]]

        vessel_total = 0

        for d in items:
            table_data.append([
                d["activity"],
                str(d["qty"]),
                str(d["rate"]),
                str(d["amount"]),
                str(d["gst_amount"])
            ])
            vessel_total += d["amount"] + d["gst_amount"]

        table = Table(table_data, repeatRows=1)

        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ]))

        elements.append(table)

        elements.append(Spacer(1, 5))
        elements.append(Paragraph(f"Vessel Total: ₹ {round(vessel_total, 2)}", styles['Normal']))
        elements.append(Spacer(1, 10))

        grand_total += vessel_total

    # =========================
    # 🔹 GST SUMMARY
    # =========================
    cgst = data.get("cgst", 0)
    sgst = data.get("sgst", 0)
    total_gst = cgst + sgst
    base = data.get("total_base", 0)
    final_total = data.get("total_bill", 0)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Summary</b>", styles['Heading3']))

    summary_table = [
        ["Base Amount", f"₹ {base}"],
        ["CGST", f"₹ {cgst}"],
        ["SGST", f"₹ {sgst}"],
        ["Total GST", f"₹ {total_gst}"],
        ["Final Amount", f"₹ {final_total}"],
    ]

    table = Table(summary_table, colWidths=[200, 200])

    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)

    # =========================
    # 🔹 FOOTER
    # =========================
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Authorized Signatory", styles['Normal']))

    doc.build(elements)