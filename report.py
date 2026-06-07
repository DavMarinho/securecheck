from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from io import BytesIO


DARK = colors.HexColor("#1e3a5f")
GOLD = colors.HexColor("#f0a500")
OK = colors.HexColor("#22c55e")
WARN = colors.HexColor("#f59e0b")
FAIL = colors.HexColor("#ef4444")
GREY = colors.HexColor("#f5f5f5")
WHITE = colors.white


STATUS_MAP = {
    "ok": ("APROVADO", OK),
    "warn": ("ATENÇÃO", WARN),
    "fail": ("FALHOU", FAIL),
}


def generate_pdf(report: dict) -> bytes:
    """Gera o PDF do relatório e retorna como bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=14*mm, bottomMargin=14*mm,
        leftMargin=14*mm, rightMargin=14*mm,
    )

    base = getSampleStyleSheet()
    s_title = ParagraphStyle("title", parent=base["Normal"],
                              fontSize=16, fontName="Helvetica-Bold",
                              textColor=WHITE, leading=20)
    s_sub = ParagraphStyle("sub", parent=base["Normal"],
                            fontSize=9, fontName="Helvetica",
                            textColor=GOLD, leading=12)
    s_cell = ParagraphStyle("cell", parent=base["Normal"],
                             fontSize=8.5, fontName="Helvetica", leading=11)
    s_cell_b = ParagraphStyle("cellb", parent=base["Normal"],
                               fontSize=8.5, fontName="Helvetica-Bold", leading=11)

    story = []
    W = A4[0] - 28*mm

    # Header
    header = Table([
        [Paragraph("SECURECHECK — RELATÓRIO DE AUDITORIA", s_title)],
        [Paragraph(f"URL: {report['url']}  |  Data: {report['scanned_at']}", s_sub)],
    ], colWidths=[W])
    header.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("LINEBELOW", (0,-1), (-1,-1), 2, GOLD),
    ]))
    story.append(header)
    story.append(Spacer(1, 6*mm))

    # Score
    score = report["score"]
    score_color = OK if score >= 80 else (WARN if score >= 50 else FAIL)
    score_table = Table([
        [Paragraph(f"<font size=24><b>{score}/100</b></font>",
                   ParagraphStyle("score", parent=base["Normal"],
                                  textColor=WHITE, alignment=1, leading=28))],
        [Paragraph(f"{report['passed']} de {report['total']} verificações aprovadas",
                   ParagraphStyle("scorelbl", parent=base["Normal"],
                                  textColor=WHITE, alignment=1, fontSize=9))],
    ], colWidths=[W])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), score_color),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 6*mm))

    # Tabela de verificações
    rows = [[
        Paragraph("<b>VERIFICAÇÃO</b>", s_cell_b),
        Paragraph("<b>STATUS</b>", s_cell_b),
        Paragraph("<b>DETALHE</b>", s_cell_b),
    ]]
    for c in report["checks"]:
        label, color = STATUS_MAP.get(c["status"], ("—", colors.grey))
        rows.append([
            Paragraph(c["name"], s_cell_b),
            Paragraph(f"<font color='{color.hexval()}'><b>{label}</b></font>", s_cell),
            Paragraph(c["detail"], s_cell),
        ])

    t = Table(rows, colWidths=[55*mm, 25*mm, W - 80*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, GREY]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("LINEBELOW", (0,0), (-1,0), 1.5, GOLD),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(t)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()