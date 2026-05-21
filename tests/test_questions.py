# tests/test_questions.py
import pytest
from questions import QUESTIONS, SECTIONS

def test_all_questions_have_required_keys():
    required = {"id", "section", "medical", "patient", "options", "weight", "clinical_note"}
    for q in QUESTIONS:
        assert required.issubset(q.keys()), f"Pregunta {q.get('id')} le faltan campos"

def test_all_options_have_scores():
    for q in QUESTIONS:
        for opt in q["options"]:
            assert "facetas" in opt and "canal" in opt, f"Opción en {q['id']} sin puntaje"
            assert "text_medical" in opt and "text_patient" in opt

def test_question_ids_are_unique():
    ids = [q["id"] for q in QUESTIONS]
    assert len(ids) == len(set(ids)), "Hay IDs duplicados"

def test_sections_are_valid():
    valid_sections = set(range(len(SECTIONS)))
    for q in QUESTIONS:
        assert q["section"] in valid_sections, f"{q['id']} tiene sección inválida"

def test_weights_are_valid():
    for q in QUESTIONS:
        assert q["weight"] in {1, 2, 3}, f"{q['id']} tiene peso fuera de rango (debe ser 1, 2 o 3)"

def test_total_question_count():
    assert len(QUESTIONS) == 13

def test_each_section_has_questions():
    for i in range(len(SECTIONS)):
        section_qs = [q for q in QUESTIONS if q["section"] == i]
        assert len(section_qs) > 0, f"Sección {i} no tiene preguntas"
