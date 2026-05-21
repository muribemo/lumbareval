# pdf_report.py
import io
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

DARK = colors.HexColor("#1A1A2E")
BLUE = colors.HexColor("#1A3A6E")
LOGO_PATH = Path(__file__).parent / "assets" / "logo_transparent.png"


def _styles() -> dict:
    return {
        "subtitle": ParagraphStyle(
            "subtitle", fontName="Helvetica", fontSize=8,
            textColor=colors.gray, spaceAfter=10, alignment=TA_CENTER,
        ),
        "section": ParagraphStyle(
            "section", fontName="Helvetica-Bold", fontSize=10,
            textColor=BLUE, spaceBefore=14, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9,
            textColor=DARK, spaceAfter=3,
        ),
        "finding": ParagraphStyle(
            "finding", fontName="Helvetica-Bold", fontSize=9,
            textColor=BLUE, spaceAfter=3,
        ),
        "score_title": ParagraphStyle(
            "score_title", fontName="Helvetica-Bold", fontSize=13,
            textColor=BLUE, alignment=TA_CENTER, spaceAfter=6, spaceBefore=8,
        ),
        "warning": ParagraphStyle(
            "warning", fontName="Helvetica-Oblique", fontSize=8,
            textColor=colors.HexColor("#7a6000"), spaceAfter=0,
        ),
        "brand": ParagraphStyle(
            "brand", fontName="Helvetica", fontSize=7,
            textColor=colors.gray, alignment=TA_CENTER, spaceBefore=10,
        ),
    }


def generate_pdf(
    patient_name: str,
    patient_age: str,
    answers: dict,
    score: dict,
    interpretation: dict,
    key_findings: list,
    mode: str = "medico",
) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.6 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )
    s = _styles()
    story = []

    # Logo
    if LOGO_PATH.exists():
        logo = RLImage(str(LOGO_PATH), width=2.4 * inch, height=0.56 * inch, kind="proportional")
        story.append(logo)

    story.append(Paragraph("EVALUACIÓN DIFERENCIAL · DOLOR LUMBAR", s["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=DARK, spaceAfter=6))

    # Datos del paciente
    today = date.today().strftime("%d/%m/%Y")
    info_data = [
        ["Paciente:", patient_name or "—", "Fecha:", today],
        ["Edad:", f"{patient_age} años" if patient_age else "—", "Modo:", "Médico" if mode == "medico" else "Paciente"],
    ]
    info_table = Table(info_data, colWidths=[1 * inch, 2.4 * inch, 0.8 * inch, 1.8 * inch])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(info_table)
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceBefore=10, spaceAfter=4))

    # Resultado principal
    story.append(Paragraph(f"Patrón compatible con: {interpretation['diagnosis']}", s["score_title"]))
    story.append(Paragraph(f"Confianza: {interpretation['confidence']}", s["body"]))

    score_data = [
        ["FACETAS", f"{score['pct_facetas']}%"],
        ["CANAL ESTRECHO", f"{score['pct_canal']}%"],
    ]
    score_table = Table(score_data, colWidths=[4.5 * inch, 1 * inch])
    score_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), DARK),
        ("TEXTCOLOR", (1, 0), (1, -1), BLUE),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#f5f7fa"), colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (0, -1), 8),
        ("RIGHTPADDING", (1, 0), (1, -1), 8),
    ]))
    story.append(Spacer(1, 6))
    story.append(score_table)

    # Hallazgos de alto peso
    if key_findings:
        story.append(Paragraph("Hallazgos de alto peso clínico:", s["section"]))
        for f in key_findings:
            story.append(Paragraph(f, s["finding"]))

    # Advertencia y branding
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=6))
    story.append(Paragraph(
        "⚠ Esta herramienta es de apoyo clínico. No reemplaza la historia clínica completa, "
        "el examen físico ni el juicio del médico tratante. "
        "El estándar de oro para dolor facetario son los bloqueos de ramas mediales; "
        "para canal estrecho, la RMN correlacionada con la clínica.",
        s["warning"],
    ))
    story.append(Paragraph("mateouribe · Your Pain, Our Purpose.", s["brand"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
