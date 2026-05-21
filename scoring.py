# scoring.py
from questions import QUESTIONS


def calculate_score(answers: dict) -> dict:
    """
    answers: {question_id: option_index}
    Retorna: {facetas, canal, total, pct_facetas, pct_canal}
    """
    score_f = 0
    score_ce = 0

    for question in QUESTIONS:
        qid = question["id"]
        if qid not in answers:
            continue
        option = question["options"][answers[qid]]
        score_f += option["facetas"]
        score_ce += option["canal"]

    total = score_f + score_ce
    if total == 0:
        return {"facetas": 0, "canal": 0, "total": 0, "pct_facetas": 50.0, "pct_canal": 50.0}

    return {
        "facetas": score_f,
        "canal": score_ce,
        "total": total,
        "pct_facetas": round((score_f / total) * 100, 1),
        "pct_canal": round((score_ce / total) * 100, 1),
    }


def interpret(score: dict) -> dict:
    """Retorna {diagnosis, confidence, color}"""
    pct_ce = score["pct_canal"]
    pct_f = score["pct_facetas"]

    if pct_ce >= 65:
        return {
            "diagnosis": "Canal Lumbar Estrecho",
            "confidence": "Alta" if pct_ce >= 75 else "Moderada",
            "color": "#1A3A6E",
        }
    if pct_f >= 65:
        return {
            "diagnosis": "Dolor Facetario",
            "confidence": "Alta" if pct_f >= 75 else "Moderada",
            "color": "#1A1A2E",
        }
    return {
        "diagnosis": "Patrón Mixto",
        "confidence": "Baja — ambas entidades posibles",
        "color": "#666666",
    }


def get_key_findings(answers: dict) -> list[str]:
    """Retorna lista de hallazgos de alto peso clínico (primera opción = positivo)."""
    KEY = {
        "q5":  ("Kemp positivo",           "Facetas"),
        "q6":  ("Claudicación neurógena",   "Canal Estrecho"),
        "q9":  ("Stoop sign positivo",      "Canal Estrecho"),
        "q10": ("Bicycle test positivo",    "Canal Estrecho"),
        "q12": ("Debilidad con la marcha",  "Canal Estrecho"),
        "q13": ("Romberg / Inestabilidad",  "Canal Estrecho"),
    }
    findings = []
    for qid, (label, diagnosis) in KEY.items():
        if answers.get(qid) == 0:
            findings.append(f"✓ {label} · {diagnosis}")
    return findings
