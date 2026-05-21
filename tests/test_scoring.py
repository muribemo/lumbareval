# tests/test_scoring.py
import pytest
from scoring import calculate_score, interpret, get_key_findings

def test_empty_answers_returns_neutral():
    score = calculate_score({})
    assert score["total"] == 0
    assert score["pct_facetas"] == 50.0
    assert score["pct_canal"] == 50.0

def test_canal_dominant_score():
    # Q6 Sí → CE+3, Q9 Sí → CE+3, Q12 Sí → CE+3, Q13 Sí → CE+3
    answers = {"q6": 0, "q9": 0, "q12": 0, "q13": 0}
    score = calculate_score(answers)
    assert score["canal"] == 12
    assert score["facetas"] == 0
    assert score["pct_canal"] == 100.0

def test_facetas_dominant_score():
    # Q5 Sí → F+3, Q3 No → F+2, Q8 Sí → F+2
    answers = {"q5": 0, "q3": 1, "q8": 0}
    score = calculate_score(answers)
    assert score["facetas"] == 7
    assert score["canal"] == 0
    assert score["pct_facetas"] == 100.0

def test_mixed_score_sums_to_100():
    answers = {"q1": 0, "q5": 0, "q9": 0}
    score = calculate_score(answers)
    assert abs(score["pct_facetas"] + score["pct_canal"] - 100.0) < 0.1

def test_partial_answer_uses_only_answered():
    answers = {"q1": 0}  # CE+2
    score = calculate_score(answers)
    assert score["canal"] == 2
    assert score["facetas"] == 0

def test_interpret_canal_alta():
    score = {"pct_canal": 76.0, "pct_facetas": 24.0}
    result = interpret(score)
    assert result["diagnosis"] == "Canal Lumbar Estrecho"
    assert result["confidence"] == "Alta"

def test_interpret_canal_moderada():
    score = {"pct_canal": 67.0, "pct_facetas": 33.0}
    result = interpret(score)
    assert result["diagnosis"] == "Canal Lumbar Estrecho"
    assert result["confidence"] == "Moderada"

def test_interpret_facetas_alta():
    score = {"pct_canal": 18.0, "pct_facetas": 82.0}
    result = interpret(score)
    assert result["diagnosis"] == "Dolor Facetario"
    assert result["confidence"] == "Alta"

def test_interpret_mixto():
    score = {"pct_canal": 55.0, "pct_facetas": 45.0}
    result = interpret(score)
    assert result["diagnosis"] == "Patrón Mixto"

def test_key_findings_stoop():
    answers = {"q9": 0}  # Stoop positivo (primera opción)
    findings = get_key_findings(answers)
    assert any("Stoop" in f for f in findings)

def test_key_findings_kemp():
    answers = {"q5": 0}
    findings = get_key_findings(answers)
    assert any("Kemp" in f for f in findings)

def test_no_findings_when_negative():
    answers = {"q9": 2, "q5": 2}  # Todas negativas
    findings = get_key_findings(answers)
    assert len(findings) == 0
