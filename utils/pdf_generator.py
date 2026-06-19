from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os

# ── Logo path (relative to project root) ──────────────────────────────────────
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(os.path.dirname(_SCRIPT_DIR), 'assets', 'logo.jpeg')

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
GREEN_DARK  = colors.HexColor("#1B6B3A")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


def _fmt(n):
    """Number formatting with 2 decimals."""
    if n is None:
        return "0.00"
    n = float(n)
    return f"{n:,.2f}"


def _fmt_date(date_str):
    """Convert YYYY-MM-DD or similar to DD/MM/YYYY."""
    if not date_str:
        return "—"
    s = str(date_str).strip()
    # Handle YYYY-MM-DD
    if len(s) >= 10 and s[4] == '-':
        parts = s[:10].split('-')
        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
    return s


def _make_page_decorator(voucher_number):
    """Returns an onPage callback that embeds the voucher number in the banner."""
    def _draw_page_decorations(c, doc):
        c.saveState()
        w, h = A4

        # Top navy banner (compact)
        banner_h = 42 * mm
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
        c.setLineWidth(2)
        c.line(0, h - banner_h, w, h - banner_h)

        # Logo (left side of banner)
        logo_x = MARGIN
        logo_h = 28 * mm
        logo_w = 28 * mm  # square aspect
        logo_y = h - banner_h + (banner_h - logo_h) / 2  # vertically centered
        try:
            if os.path.exists(LOGO_PATH):
                c.drawImage(LOGO_PATH, logo_x, logo_y, width=logo_w, height=logo_h,
                            preserveAspectRatio=True, mask='auto')
        except Exception:
            pass  # skip logo if it fails

        # Company name — next to logo
        text_x = MARGIN + logo_w + 6 * mm
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(WHITE)
        c.drawString(text_x, h - 20 * mm, "IRC GROUP")

        # Tagline
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#8BAED4"))
        c.drawString(text_x, h - 27 * mm, "MARITIME SERVICES & LOGISTICS")

        # Gold divider under tagline
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(text_x, h - 30 * mm, text_x + 60 * mm, h - 30 * mm)

        # INVOICE label (right side of banner)
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.HexColor("#8BAED4"))
        c.drawRightString(w - MARGIN, h - 18 * mm, "INVOICE")

        # Voucher number sub-label
        c.setFont("Helvetica", 7)
        c.setFillColor(GOLD)
        c.drawRightString(w - MARGIN, h - 25 * mm, voucher_number)

        # Footer
        footer_y = 10 * mm
        c.setStrokeColor(LIGHT_GREY)
        c.setLineWidth(0.4)
        c.line(MARGIN, footer_y + 4 * mm, w - MARGIN, footer_y + 4 * mm)

        c.setFont("Helvetica", 6.5)
        c.setFillColor(MID_GREY)
        c.drawString(MARGIN, footer_y, "IRC GROUP  |  Maritime Services & Logistics")
        c.drawRightString(w - MARGIN, footer_y, "This is a computer-generated invoice.")

        c.restoreState()
    return _draw_page_decorations


def generate_invoice_pdf(data, file_path=None):
    """
    Generates a detailed 1-page invoice PDF with full itemized activities.
    Returns BytesIO when file_path is None (view only, nothing saved).
    Saves to disk when file_path is a string path.
    """
    buffer = BytesIO() if file_path is None else file_path
    doc = BaseDocTemplate(
        buffer, pagesize=A4,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=50 * mm, bottomMargin=18 * mm
    )
    content_w = PAGE_W - 2 * MARGIN
    frame = Frame(MARGIN, 18 * mm, content_w, PAGE_H - 50 * mm - 18 * mm, id='main')
    template = PageTemplate(id='main', frames=[frame], onPage=_make_page_decorator(data['voucher_number']))
    doc.addPageTemplates([template])

    styles = getSampleStyleSheet()
    elements = []

    def S(name, **kw):
        return ParagraphStyle(name, parent=kw.pop('parent', styles['Normal']), **kw)

    # ── Style definitions (compact) ───────────────────────────────────────────
    lbl   = S('Lbl',  fontSize=6,   textColor=MID_GREY,  fontName='Helvetica-Bold', spaceAfter=1, leading=8)
    val   = S('Val',  fontSize=8,   textColor=TEXT_DARK,  fontName='Helvetica-Bold', spaceAfter=1, leading=11)
    val2  = S('Val2', fontSize=7,   textColor=DARK_GREY,  fontName='Helvetica',      spaceAfter=1, leading=10)

    # ── Meta Info Row (Bill To + Voucher + Period) ────────────────────────────
    meta_table = Table(
        [[
            [Paragraph("BILL TO", lbl), Paragraph(data.get('party_name', 'N/A'), val)],
            [Paragraph("VOUCHER NO.", lbl), Paragraph(data['voucher_number'], val)],
            [Paragraph("BILLING PERIOD", lbl),
             Paragraph(f"{_fmt_date(data['period_start'])}  \u2192  {_fmt_date(data['period_end'])}", val2)]
        ]],
        colWidths=[content_w * 0.42, content_w * 0.30, content_w * 0.28]
    )
    meta_table.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND',    (0, 0), (-1, -1), OFF_WHITE),
        ('BOX',           (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ('LINEAFTER',     (0, 0), (1, -1),  0.4, LIGHT_GREY),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 10))

    # ── Section Title ─────────────────────────────────────────────────────────
    elements.append(Paragraph(
        "\u25b8  BILL DETAILS / ITEMIZED ACTIVITIES",
        S('Sec', fontSize=7.5, textColor=TEAL, fontName='Helvetica-Bold', leading=10)
    ))
    elements.append(Spacer(1, 5))

    # ── Itemized Activities Table ─────────────────────────────────────────────
    hdr_s  = S('TH',   fontSize=6.5, textColor=WHITE,     fontName='Helvetica-Bold', alignment=TA_CENTER, leading=9)
    cel_l  = S('CL',   fontSize=7,   textColor=TEXT_DARK,  fontName='Helvetica',      alignment=TA_LEFT,   leading=9)
    cel_r  = S('CR',   fontSize=7,   textColor=TEXT_DARK,  fontName='Helvetica',      alignment=TA_RIGHT,  leading=9)
    cel_rb = S('CRB',  fontSize=7,   textColor=NAVY_MED,   fontName='Helvetica-Bold', alignment=TA_RIGHT,  leading=9)

    # Column widths: Vessel Name | Activity | Qty | Rate | Base Amt | GST % | GST Amt | Total
    col_w = [
        content_w * 0.18,   # Vessel Name
        content_w * 0.17,   # Activity
        content_w * 0.08,   # Qty
        content_w * 0.10,   # Rate
        content_w * 0.14,   # Base Amount
        content_w * 0.08,   # GST Rate (%)
        content_w * 0.12,   # GST Amount
        content_w * 0.13,   # Total
    ]

    table_data = [[
        Paragraph("VESSEL NAME",  hdr_s),
        Paragraph("ACTIVITY",     hdr_s),
        Paragraph("QTY",          hdr_s),
        Paragraph("RATE",         hdr_s),
        Paragraph("BASE AMT",     hdr_s),
        Paragraph("GST %",        hdr_s),
        Paragraph("GST AMT",      hdr_s),
        Paragraph("TOTAL",        hdr_s),
    ]]

    grand_base = 0
    grand_gst = 0
    grand_total = 0

    for d in data["details"]:
        vessel_name = d.get("vessel_name", f"Vessel {d.get('vessel_id', '?')}")
        activity    = d.get("activity", "—")
        qty         = d.get("qty", 0)
        rate        = d.get("rate", 0)
        amount      = d.get("amount", 0)
        gst_rate    = d.get("gst_rate", 0)
        gst_amount  = d.get("gst_amount", 0)
        total       = amount + gst_amount

        grand_base  += amount
        grand_gst   += gst_amount
        grand_total += total

        table_data.append([
            Paragraph(vessel_name,                   cel_l),
            Paragraph(activity,                      cel_l),
            Paragraph(_fmt(qty).rstrip('0').rstrip('.') if qty == int(qty) else _fmt(qty), cel_r),
            Paragraph(_fmt(rate),                    cel_r),
            Paragraph(_fmt(amount),                  cel_r),
            Paragraph(f"{gst_rate:g}%",              S('pct', fontSize=7, textColor=TEAL, fontName='Helvetica-Bold', alignment=TA_CENTER, leading=9)),
            Paragraph(_fmt(gst_amount),              cel_r),
            Paragraph(_fmt(total),                   cel_rb),
        ])

    # Totals row
    tot_lbl = S('TotL', fontSize=7.5, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_RIGHT, leading=10)
    tot_val = S('TotV', fontSize=7.5, textColor=WHITE, fontName='Helvetica-Bold', alignment=TA_RIGHT, leading=10)

    table_data.append([
        Paragraph("", tot_lbl),
        Paragraph("", tot_lbl),
        Paragraph("", tot_lbl),
        Paragraph("TOTAL", tot_lbl),
        Paragraph(_fmt(grand_base), tot_val),
        Paragraph("", tot_lbl),
        Paragraph(_fmt(grand_gst), tot_val),
        Paragraph(_fmt(grand_total), tot_val),
    ])

    num_detail_rows = len(data["details"])
    last_row = num_detail_rows + 1   # header=0, data=1..N, total=N+1

    t = Table(table_data, colWidths=col_w, repeatRows=1)

    style_cmds = [
        # Header
        ('BACKGROUND',    (0, 0), (-1, 0),  NAVY),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.2, GOLD),

        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [WHITE, LIGHT_BLUE]),

        # Total row
        ('BACKGROUND',    (0, last_row), (-1, last_row), NAVY_MED),
        ('LINEABOVE',     (0, last_row), (-1, last_row), 1, GOLD),

        # Grid lines
        ('LINEBELOW',     (0, 1), (-1, -2), 0.3, LIGHT_GREY),
        ('BOX',           (0, 0), (-1, -1), 0.5, LIGHT_GREY),

        # Last column highlight
        ('BACKGROUND',    (7, 1), (7, -2),  colors.HexColor("#EFF6FF")),

        # Padding (compact)
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]

    t.setStyle(TableStyle(style_cmds))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # ── Tax Breakup + Grand Total Box ─────────────────────────────────────────
    lbl_s  = S('SumL', fontSize=7.5, textColor=DARK_GREY, fontName='Helvetica',      alignment=TA_LEFT,  leading=10)
    val_s  = S('SumR', fontSize=7.5, textColor=TEXT_DARK,  fontName='Helvetica-Bold', alignment=TA_RIGHT, leading=10)
    lbl_gt = S('GtL',  fontSize=9,   textColor=WHITE,      fontName='Helvetica-Bold', alignment=TA_LEFT,  leading=12)
    val_gt = S('GtR',  fontSize=10,  textColor=WHITE,      fontName='Helvetica-Bold', alignment=TA_RIGHT, leading=12)

    total_base = data.get('total_base', 0)
    cgst_val   = data.get('cgst', 0)
    sgst_val   = data.get('sgst', 0)
    total_gst  = cgst_val + sgst_val
    grand      = data.get('total_bill', 0)

    summary_data = [
        [Paragraph("Taxable Amount (Base)", lbl_s), Paragraph(f"Rs {_fmt(total_base)}",  val_s)],
        [Paragraph("CGST",                  lbl_s), Paragraph(f"Rs {_fmt(cgst_val)}",    val_s)],
        [Paragraph("SGST",                  lbl_s), Paragraph(f"Rs {_fmt(sgst_val)}",    val_s)],
        [Paragraph("Total GST",             lbl_s), Paragraph(f"Rs {_fmt(total_gst)}",   val_s)],
        [Paragraph("GRAND TOTAL",           lbl_gt), Paragraph(f"Rs {_fmt(grand)}",      val_gt)],
    ]

    summary_w = 3.0 * inch
    spacer_col = content_w - summary_w

    summary_table = Table(summary_data, colWidths=[summary_w * 0.55, summary_w * 0.45])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 3),  OFF_WHITE),
        ('BACKGROUND',    (0, 4), (-1, 4),  NAVY),
        ('LINEBELOW',     (0, 0), (-1, 3),  0.3, LIGHT_GREY),
        ('LINEABOVE',     (0, 4), (-1, 4),  1.2, GOLD),
        ('BOX',           (0, 0), (-1, -1), 0.4, LIGHT_GREY),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Push totals box to the right
    outer = Table([["", summary_table]], colWidths=[spacer_col, summary_w])
    outer.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'BOTTOM')]))
    elements.append(outer)

    # ── Signature ─────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 20))
    sig_table = Table(
        [[Paragraph("________________________",  S('Sr',  fontSize=7,   textColor=MID_GREY,  fontName='Helvetica',      alignment=TA_RIGHT))],
         [Paragraph("Authorized Signatory",      S('Sb',  fontSize=7.5, textColor=DARK_GREY, fontName='Helvetica-Bold', alignment=TA_RIGHT))],
         [Paragraph("DOCK YARD",                 S('Sco', fontSize=6.5, textColor=MID_GREY,  fontName='Helvetica',      alignment=TA_RIGHT))]],
        colWidths=[content_w]
    )
    sig_table.setStyle(TableStyle([
        ('TOPPADDING',    (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    elements.append(sig_table)

    doc.build(elements)

    if file_path is None:
        buffer.seek(0)
        return buffer
