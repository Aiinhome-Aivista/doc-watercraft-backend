from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from io import BytesIO

# ── Color Palette ─────────────────────────────────────────────────────────────
NAVY        = colors.HexColor("#0D2137")
NAVY_MED    = colors.HexColor("#1A3B5D")
LIGHT_BLUE  = colors.HexColor("#EBF4FF")
TEAL        = colors.HexColor("#0F7B8E")
GOLD        = colors.HexColor("#C8952A")
WHITE       = colors.white
OFF_WHITE   = colors.HexColor("#F7F9FC")
LIGHT_GREY  = colors.HexColor("#E8ECF0")
MID_GREY    = colors.HexColor("#8A9BB0")
DARK_GREY   = colors.HexColor("#3D4F63")
TEXT_DARK   = colors.HexColor("#1C2B3A")

PAGE_W, PAGE_H = A4
MARGIN = 22 * mm


def _make_page_decorator(voucher_number):
    """Returns an onPage callback that embeds the voucher number in the banner."""
    def _draw_page_decorations(c, doc):
        c.saveState()
        w, h = A4

        # Top navy banner
        banner_h = 58 * mm
        c.setFillColor(NAVY)
        c.rect(0, h - banner_h, w, banner_h, fill=1, stroke=0)

        # Diagonal accent stripe
        c.setFillColor(colors.HexColor("#0A1B2E"))
        p = c.beginPath()
        p.moveTo(w * 0.56, h)
        p.lineTo(w * 0.78, h)
        p.lineTo(w * 0.56, h - banner_h)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

        # Gold accent line under banner
        c.setStrokeColor(GOLD)
        c.setLineWidth(2.5)
        c.line(0, h - banner_h, w, h - banner_h)

        # Company name
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(WHITE)
        c.drawString(MARGIN, h - 30 * mm, "DOCK YARD")

        # Tagline
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#8BAED4"))
        c.drawString(MARGIN, h - 39 * mm, "MARITIME SERVICES & LOGISTICS")

        # Gold divider under tagline
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.line(MARGIN, h - 42 * mm, MARGIN + 80 * mm, h - 42 * mm)

        # INVOICE label (right side of banner)
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(colors.HexColor("#8BAED4"))
        c.drawRightString(w - MARGIN, h - 24 * mm, "INVOICE")

        # "VESSEL BILLING DOCUMENT" sub-label
        c.setFont("Helvetica", 8)
        c.setFillColor(GOLD)
        c.drawRightString(w - MARGIN, h - 33 * mm, voucher_number)

        # Footer
        footer_y = 14 * mm
        c.setStrokeColor(LIGHT_GREY)
        c.setLineWidth(0.5)
        c.line(MARGIN, footer_y + 5 * mm, w - MARGIN, footer_y + 5 * mm)

        c.setFont("Helvetica", 7.5)
        c.setFillColor(MID_GREY)
        c.drawString(MARGIN, footer_y, "DOCK YARD  |  Maritime Services & Logistics")
        c.drawRightString(w - MARGIN, footer_y, "This is a computer-generated invoice.")

        # Page number circle
        pg_x = w / 2
        c.setFillColor(NAVY)
        c.circle(pg_x, footer_y + 2.5 * mm, 5 * mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(WHITE)
        c.drawCentredString(pg_x, footer_y + 1 * mm, f"Page {doc.page}")

        c.restoreState()
    return _draw_page_decorations


def generate_invoice_pdf(data, file_path=None):
    """
    Returns BytesIO when file_path is None (view only, nothing saved).
    Saves to disk when file_path is a string path.
    """
    buffer = BytesIO() if file_path is None else file_path
    doc = BaseDocTemplate(
        buffer, pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=70 * mm, bottomMargin=28 * mm
    )
    frame = Frame(MARGIN, 28 * mm, PAGE_W - 2 * MARGIN, PAGE_H - 70 * mm - 28 * mm, id='main')
    template = PageTemplate(id='main', frames=[frame], onPage=_make_page_decorator(data['voucher_number']))
    doc.addPageTemplates([template])

    styles = getSampleStyleSheet()
    elements = []

    def S(name, **kw):
        return ParagraphStyle(name, parent=kw.pop('parent', styles['Normal']), **kw)

    # ── Meta Info Row (Bill To + Voucher Details) ─────────────────────────────
    lbl  = S('Lbl',  fontSize=7,   textColor=MID_GREY,  fontName='Helvetica-Bold', spaceAfter=1, leading=10)
    val  = S('Val',  fontSize=9.5, textColor=TEXT_DARK, fontName='Helvetica-Bold', spaceAfter=2, leading=13)
    val2 = S('Val2', fontSize=8.5, textColor=DARK_GREY, fontName='Helvetica',      spaceAfter=1, leading=12)

    meta_table = Table(
        [[
            [Paragraph("BILL TO", lbl), Paragraph(data.get('party_name', 'N/A'), val)],
            [Paragraph("VOUCHER NO.", lbl), Paragraph(data['voucher_number'], val),
             Spacer(1, 4),
             Paragraph("BILLING PERIOD", lbl),
             Paragraph(f"{data['period_start']}  \u2192  {data['period_end']}", val2)]
        ]],
        colWidths=[3.8 * inch, 3.0 * inch]
    )
    meta_table.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND',    (0, 0), (-1, -1), OFF_WHITE),
        ('BOX',           (0, 0), (-1, -1), 0.5, LIGHT_GREY),
        ('LINEAFTER',     (0, 0), (0, -1),  0.5, LIGHT_GREY),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 14),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 14),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 18))

    # ── Section Title ─────────────────────────────────────────────────────────
    elements.append(Paragraph(
        "\u25b8  VESSEL BILLING SUMMARY",
        S('Sec', fontSize=9, textColor=TEAL, fontName='Helvetica-Bold', leading=12)
    ))
    elements.append(Spacer(1, 8))

    # ── Vessel Table ──────────────────────────────────────────────────────────
    hdr_s = S('TH',  fontSize=8.5, textColor=WHITE,     fontName='Helvetica-Bold', alignment=TA_CENTER, leading=11)
    cel_l = S('CL',  fontSize=9,   textColor=TEXT_DARK, fontName='Helvetica',      alignment=TA_LEFT,   leading=12)
    cel_r = S('CR',  fontSize=9,   textColor=TEXT_DARK, fontName='Helvetica',      alignment=TA_RIGHT,  leading=12)
    cel_b = S('CRB', fontSize=9,   textColor=NAVY_MED,  fontName='Helvetica-Bold', alignment=TA_RIGHT,  leading=12)

    col_widths = [2.4*inch, 0.95*inch, 1.1*inch, 1.0*inch, 1.1*inch]

    table_data = [[
        Paragraph("VESSEL NAME", hdr_s),
        Paragraph("QTY",         hdr_s),
        Paragraph("TAXABLE AMT", hdr_s),
        Paragraph("GST AMT",     hdr_s),
        Paragraph("TOTAL AMT",   hdr_s),
    ]]

    vessel_map = {}
    for d in data["details"]:
        vessel = d.get("vessel_name", f"Vessel {d['vessel_id']}")
        if vessel not in vessel_map:
            vessel_map[vessel] = {'qty': 0, 'base': 0, 'gst': 0}
        vessel_map[vessel]['qty']  += d['qty']
        vessel_map[vessel]['base'] += d['amount']
        vessel_map[vessel]['gst']  += d['gst_amount']

    for name, vals in vessel_map.items():
        total = vals['base'] + vals['gst']
        table_data.append([
            Paragraph(name,                         cel_l),
            Paragraph(f"{vals['qty']:,.0f}",        cel_r),
            Paragraph(f"Rs {vals['base']:,.2f}",    cel_r),
            Paragraph(f"Rs {vals['gst']:,.2f}",     cel_r),
            Paragraph(f"Rs {total:,.2f}",           cel_b),
        ])

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  NAVY),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [WHITE, LIGHT_BLUE]),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.5, GOLD),
        ('LINEBEFORE',    (4, 0), (4, -1),  0.5, LIGHT_GREY),
        ('LINEBELOW',     (0, 1), (-1, -1), 0.4, LIGHT_GREY),
        ('BOX',           (0, 0), (-1, -1), 0.5, LIGHT_GREY),
        ('BACKGROUND',    (4, 1), (4, -1),  colors.HexColor("#EFF6FF")),
        ('TOPPADDING',    (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 22))

    # ── Totals Box ────────────────────────────────────────────────────────────
    lbl_s  = S('SumL', fontSize=8.5, textColor=DARK_GREY, fontName='Helvetica',      alignment=TA_LEFT,  leading=12)
    val_s  = S('SumR', fontSize=8.5, textColor=TEXT_DARK, fontName='Helvetica-Bold', alignment=TA_RIGHT, leading=12)
    lbl_gt = S('GtL',  fontSize=10,  textColor=WHITE,      fontName='Helvetica-Bold', alignment=TA_LEFT,  leading=14)
    val_gt = S('GtR',  fontSize=12,  textColor=WHITE,      fontName='Helvetica-Bold', alignment=TA_RIGHT, leading=14)

    total_base = data.get('total_base', 0)
    total_gst  = data.get('cgst', 0) + data.get('sgst', 0)
    grand      = data.get('total_bill', 0)

    summary_data = [
        [Paragraph("Taxable Amount (Base)", lbl_s), Paragraph(f"Rs {total_base:,.2f}",          val_s)],
        [Paragraph("CGST",                  lbl_s), Paragraph(f"Rs {data.get('cgst',0):,.2f}",  val_s)],
        [Paragraph("SGST",                  lbl_s), Paragraph(f"Rs {data.get('sgst',0):,.2f}",  val_s)],
        [Paragraph("Total GST",             lbl_s), Paragraph(f"Rs {total_gst:,.2f}",           val_s)],
        [Paragraph("GRAND TOTAL (ROUNDED)", lbl_gt), Paragraph(f"Rs {grand:,.2f}",              val_gt)],
    ]

    spacer_col = PAGE_W - 2 * MARGIN - 3.2 * inch
    summary_table = Table(summary_data, colWidths=[1.9*inch, 1.3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 3),  OFF_WHITE),
        ('BACKGROUND',    (0, 4), (-1, 4),  NAVY),
        ('LINEBELOW',     (0, 0), (-1, 3),  0.4, LIGHT_GREY),
        ('LINEABOVE',     (0, 4), (-1, 4),  1.5, GOLD),
        ('BOX',           (0, 0), (-1, -1), 0.5, LIGHT_GREY),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Push totals box to the right
    outer = Table([[" ", summary_table]], colWidths=[spacer_col, 3.2*inch])
    outer.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'BOTTOM')]))
    elements.append(outer)

    # ── Signature ─────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 36))
    sig_table = Table(
        [[Paragraph("________________________",  S('Sr',  fontSize=8,   textColor=MID_GREY,  fontName='Helvetica',      alignment=TA_RIGHT))],
         [Paragraph("Authorized Signatory",      S('Sb',  fontSize=8.5, textColor=DARK_GREY, fontName='Helvetica-Bold', alignment=TA_RIGHT))],
         [Paragraph("DOCK YARD",                 S('Sco', fontSize=7.5, textColor=MID_GREY,  fontName='Helvetica',      alignment=TA_RIGHT))]],
        colWidths=[PAGE_W - 2 * MARGIN]
    )
    sig_table.setStyle(TableStyle([
        ('TOPPADDING',    (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(sig_table)

    doc.build(elements)

    if file_path is None:
        buffer.seek(0)
        return buffer


# ──────────────────────────────────────────────────────────────────────────────
# USAGE EXAMPLES
# ──────────────────────────────────────────────────────────────────────────────
#
# ✅ Flask — view in browser (no download popup):
#
#   from flask import Flask, Response
#   app = Flask(__name__)
#
#   @app.route("/invoice/<voucher_no>")
#   def invoice(voucher_no):
#       data = fetch_data_from_db(voucher_no)   # your DB call
#       pdf = generate_invoice_pdf(data)
#       return Response(
#           pdf,
#           mimetype="application/pdf",
#           headers={"Content-Disposition": "inline; filename=invoice.pdf"}
#       )
#
# ✅ Django — view in browser:
#
#   from django.http import HttpResponse
#
#   def invoice_view(request, voucher_no):
#       data = fetch_data(voucher_no)
#       pdf = generate_invoice_pdf(data)
#       response = HttpResponse(pdf, content_type="application/pdf")
#       response["Content-Disposition"] = 'inline; filename="invoice.pdf"'
#       return response
#
# ✅ Save to disk:
#   generate_invoice_pdf(data, "/path/to/invoice.pdf")
#
# KEY: "inline" (not "attachment") is what tells the browser to DISPLAY, not download.
# ──────────────────────────────────────────────────────────────────────────────

