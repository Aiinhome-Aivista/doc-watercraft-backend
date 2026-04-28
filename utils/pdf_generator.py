from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

def generate_invoice_pdf(data, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("INVOICE", styles['Title']))
    elements.append(Spacer(1, 10))

    # Header
    elements.append(Paragraph(f"Voucher: {data['voucher_number']}", styles['Normal']))
    elements.append(Paragraph(f"Total Bill: ₹ {data['total_bill']}", styles['Normal']))
    elements.append(Spacer(1, 10))

    # Table
    table_data = [["Vessel", "Activity", "Qty", "Rate", "Amount", "GST"]]

    for d in data["details"]:
        table_data.append([
            str(d["vessel_id"]),
            d["activity"],
            str(d["qty"]),
            str(d["rate"]),
            str(d["amount"]),
            str(d["gst_amount"])
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ]))

    elements.append(table)

    # Totals
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Base: ₹ {data['total_base']}", styles['Normal']))
    elements.append(Paragraph(f"GST: ₹ {data['total_gst']}", styles['Normal']))
    elements.append(Paragraph(f"Final: ₹ {data['total_bill']}", styles['Normal']))

    doc.build(elements)