# app.py
import base64
from pathlib import Path

import streamlit as st

from questions import QUESTIONS, SECTIONS
from scoring import calculate_score, get_key_findings, interpret
from pdf_report import generate_pdf

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="LumbarEval · mateouribe",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS (mobile-first) ────────────────────────────────────────────────────────
CSS = """
<style>
    /* Contenedor centrado y estrecho para móvil */
    .main .block-container {
        padding: 0.5rem 1rem 2rem;
        max-width: 680px;
    }
    /* Botones grandes y táctiles */
    .stButton > button {
        min-height: 48px;
        font-size: 15px;
        border-radius: 8px;
        width: 100%;
        margin-bottom: 6px;
        white-space: normal;
        line-height: 1.3;
    }
    /* Header */
    .lumbar-header {
        text-align: center;
        padding: 16px 0 12px;
        border-bottom: 1px solid #dde3ee;
        margin-bottom: 20px;
    }
    /* Subtítulo de sección */
    .section-label {
        font-size: 12px;
        color: #888;
        margin-bottom: 4px;
        font-family: sans-serif;
    }
    /* Tarjeta de pregunta */
    .question-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 18px 16px 12px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.07);
        margin-bottom: 16px;
    }
    /* Nota clínica (solo modo médico) */
    .clinical-note {
        background: #eef2f9;
        border-left: 3px solid #1A3A6E;
        border-radius: 4px;
        padding: 7px 10px;
        font-size: 12px;
        color: #1A3A6E;
        margin-top: 10px;
        font-family: sans-serif;
    }
    /* Resultado: etiqueta de barra */
    .result-label {
        font-size: 13px;
        font-weight: 600;
        color: #1A1A2E;
        margin-bottom: 2px;
        font-family: sans-serif;
    }
    /* Caja de advertencia clínica */
    .clinical-warning {
        background: #fffbf0;
        border: 1px solid #f0d080;
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 12px;
        color: #7a6000;
        margin-top: 16px;
        font-family: sans-serif;
    }
    /* Ocultar menú y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""

# ── Utilidades ────────────────────────────────────────────────────────────────
LOGO_PATH = Path(__file__).parent / "assets" / "logo_transparent.png"


def logo_b64() -> str:
    if LOGO_PATH.exists():
        return base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return ""


def show_header():
    b64 = logo_b64()
    if b64:
        st.markdown(
            f'<div class="lumbar-header">'
            f'<img src="data:image/png;base64,{b64}" style="height:38px;object-fit:contain;" />'
            f'</div>',
            unsafe_allow_html=True,
        )


def init_session():
    defaults = {
        "screen": "inicio",
        "mode": "medico",
        "section": 0,
        "answers": {},
        "patient_name": "",
        "patient_age": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ── Pantalla: Inicio ──────────────────────────────────────────────────────────
def show_inicio():
    st.markdown("### Evaluación Diferencial · Dolor Lumbar")
    st.markdown(
        "<p style='color:#888;font-size:13px;margin-bottom:20px;'>"
        "Responda las preguntas para orientar el diagnóstico diferencial "
        "entre dolor facetario y canal lumbar estrecho.</p>",
        unsafe_allow_html=True,
    )

    patient_name = st.text_input("Nombre del paciente (opcional)", placeholder="Ej. Juan García")
    patient_age = st.text_input("Edad (opcional)", placeholder="Ej. 64")

    st.markdown("---")
    st.markdown("**¿Quién responde este cuestionario?**")

    col_m, col_p = st.columns(2)
    with col_m:
        if st.button("🩺 Soy médico\nVista clínica completa", type="primary"):
            st.session_state.mode = "medico"
            st.session_state.patient_name = patient_name
            st.session_state.patient_age = patient_age
            st.session_state.section = 0
            st.session_state.answers = {}
            st.session_state.screen = "preguntas"
            st.rerun()
    with col_p:
        if st.button("🙋 Soy paciente\nCuestionario guiado", type="secondary"):
            st.session_state.mode = "paciente"
            st.session_state.patient_name = patient_name
            st.session_state.patient_age = patient_age
            st.session_state.section = 0
            st.session_state.answers = {}
            st.session_state.screen = "preguntas"
            st.rerun()


# ── Pantalla: Preguntas ───────────────────────────────────────────────────────
def show_preguntas():
    mode = st.session_state.mode
    section_idx = st.session_state.section
    total_sections = len(SECTIONS)

    # Barra de progreso
    progress = (section_idx + 1) / total_sections
    st.progress(progress)
    st.markdown(
        f'<p class="section-label">Sección {section_idx + 1} de {total_sections}: '
        f'<b>{SECTIONS[section_idx]}</b></p>',
        unsafe_allow_html=True,
    )

    # Preguntas de esta sección
    section_questions = [q for q in QUESTIONS if q["section"] == section_idx]

    for q in section_questions:
        text = q["medical"] if mode == "medico" else q["patient"]
        opt_key = "text_medical" if mode == "medico" else "text_patient"
        options = [opt[opt_key] for opt in q["options"]]
        current_idx = st.session_state.answers.get(q["id"])

        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"**{text}**")

        for i, opt_text in enumerate(options):
            btn_type = "primary" if current_idx == i else "secondary"
            if st.button(opt_text, key=f"opt_{q['id']}_{i}", type=btn_type, use_container_width=True):
                st.session_state.answers[q["id"]] = i
                st.rerun()

        if mode == "medico":
            weight_label = {"3": "Alto", "2": "Moderado", "1": "Bajo"}.get(str(q["weight"]), "—")
            st.markdown(
                f'<div class="clinical-note">🩺 {q["clinical_note"]} &nbsp;·&nbsp; Peso: <b>{weight_label}</b></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Navegación
    col_back, col_next = st.columns(2)
    with col_back:
        if section_idx > 0:
            if st.button("← Anterior", use_container_width=True):
                st.session_state.section -= 1
                st.rerun()
        else:
            if st.button("← Inicio", use_container_width=True):
                st.session_state.screen = "inicio"
                st.rerun()

    with col_next:
        if section_idx < total_sections - 1:
            if st.button("Siguiente →", type="primary", use_container_width=True):
                st.session_state.section += 1
                st.rerun()
        else:
            if st.button("Ver resultado →", type="primary", use_container_width=True):
                st.session_state.screen = "resultado"
                st.rerun()


# ── Pantalla: Resultado ───────────────────────────────────────────────────────
def show_resultado():
    answers = st.session_state.answers
    mode = st.session_state.mode

    score = calculate_score(answers)
    interpretation = interpret(score)
    findings = get_key_findings(answers)

    st.markdown("### Resultado de la Evaluación")

    # Barras de porcentaje
    st.markdown(
        f'<p class="result-label">FACETAS &nbsp; {score["pct_facetas"]}%</p>',
        unsafe_allow_html=True,
    )
    st.progress(score["pct_facetas"] / 100)

    st.markdown(
        f'<p class="result-label">CANAL ESTRECHO &nbsp; {score["pct_canal"]}%</p>',
        unsafe_allow_html=True,
    )
    st.progress(score["pct_canal"] / 100)

    st.markdown("---")

    # Interpretación
    color = interpretation["color"]
    st.markdown(
        f'<h4 style="color:{color};">Patrón compatible con: {interpretation["diagnosis"]}</h4>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**Confianza:** {interpretation['confidence']}")

    # Hallazgos clave
    if findings:
        st.markdown("**Hallazgos de alto peso clínico:**")
        for f in findings:
            st.markdown(f"- {f}")
    else:
        st.markdown("_No se registraron hallazgos de alto peso._")

    # Advertencia
    st.markdown(
        '<div class="clinical-warning">'
        "⚠️ <b>Herramienta de apoyo clínico.</b> No reemplaza la historia clínica completa, "
        "el examen físico ni el juicio del médico tratante. "
        "Estándar de oro para facetas: bloqueos de ramas mediales. "
        "Para canal estrecho: RMN correlacionada con la clínica."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Descarga PDF
    pdf_bytes = generate_pdf(
        patient_name=st.session_state.patient_name,
        patient_age=st.session_state.patient_age,
        answers=answers,
        score=score,
        interpretation=interpretation,
        key_findings=findings,
        mode=mode,
    )
    st.download_button(
        label="⬇ Descargar PDF para historia clínica",
        data=pdf_bytes,
        file_name="LumbarEval.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary",
    )

    if mode == "paciente":
        st.info(
            "Sus respuestas han sido evaluadas. "
            "Comparta este reporte con su médico para una orientación diagnóstica completa."
        )

    st.markdown(" ")
    if st.button("← Nueva evaluación", use_container_width=True):
        st.session_state.screen = "inicio"
        st.session_state.answers = {}
        st.session_state.section = 0
        st.session_state.patient_name = ""
        st.session_state.patient_age = ""
        st.rerun()


# ── Punto de entrada ──────────────────────────────────────────────────────────
def main():
    st.markdown(CSS, unsafe_allow_html=True)
    init_session()
    show_header()

    screen = st.session_state.screen
    if screen == "inicio":
        show_inicio()
    elif screen == "preguntas":
        show_preguntas()
    elif screen == "resultado":
        show_resultado()


if __name__ == "__main__":
    main()
