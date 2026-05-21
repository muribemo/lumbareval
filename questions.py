# questions.py
SECTIONS = [
    "Localización del dolor",
    "Factores agravantes",
    "Factores aliviantes",
    "Síntomas neurológicos",
]

QUESTIONS = [
    # ── Sección 0: Localización ──────────────────────────────────────────
    {
        "id": "q1",
        "section": 0,
        "medical": "¿El dolor irradia por debajo de la rodilla?",
        "patient": "¿El dolor le baja hasta la pantorrilla, el pie o los dedos?",
        "options": [
            {"text_medical": "Sí", "text_patient": "Sí, claramente", "facetas": 0, "canal": 2},
            {"text_medical": "A veces", "text_patient": "A veces / no sé", "facetas": 0, "canal": 0},
            {"text_medical": "No", "text_patient": "No, se queda arriba de la rodilla", "facetas": 1, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Irradiación distal a la rodilla sugiere compresión radicular · Canal Estrecho",
    },
    {
        "id": "q2",
        "section": 0,
        "medical": "¿El dolor es bilateral (ambas piernas)?",
        "patient": "¿Le duele en las dos piernas a la vez?",
        "options": [
            {"text_medical": "Sí", "text_patient": "Sí, en las dos", "facetas": 0, "canal": 2},
            {"text_medical": "Varía (a veces una, a veces ambas)", "text_patient": "A veces en una, a veces en las dos", "facetas": 0, "canal": 0},
            {"text_medical": "No, unilateral", "text_patient": "No, solo en una pierna", "facetas": 1, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Bilateralidad sugiere canal central estrecho — menos frecuente en dolor facetario puro",
    },
    {
        "id": "q3",
        "section": 0,
        "medical": "¿El dolor sigue un patrón dermatomal claro?",
        "patient": "¿El dolor sigue una línea definida desde la espalda por la pierna?",
        "options": [
            {"text_medical": "Sí, patrón dermatomal definido", "text_patient": "Sí, sigue una línea clara", "facetas": 0, "canal": 1},
            {"text_medical": "No, difuso / pseudo-radicular", "text_patient": "No, es difuso y sin dirección clara", "facetas": 2, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Dolor pseudo-radicular sin patrón dermatomal claro — característico de referral facetario",
    },
    {
        "id": "q4",
        "section": 0,
        "medical": "¿Siente hormigueo o adormecimiento en piernas o pies?",
        "patient": "¿Siente hormigueo, adormecimiento o 'corrientazos' en las piernas o los pies?",
        "options": [
            {"text_medical": "Sí, frecuente", "text_patient": "Sí, seguido", "facetas": 0, "canal": 2},
            {"text_medical": "Ocasionalmente", "text_patient": "A veces", "facetas": 0, "canal": 1},
            {"text_medical": "No", "text_patient": "No", "facetas": 0, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Parestesias en extremidades inferiores sugieren compromiso radicular · Canal Estrecho",
    },
    # ── Sección 1: Factores agravantes ───────────────────────────────────
    {
        "id": "q5",
        "section": 1,
        "medical": "¿Empeora con extensión lumbar + rotación ipsilateral? (Maniobra de Kemp)",
        "patient": "¿Empeora el dolor al inclinarse hacia atrás y girar el tronco hacia el lado que duele?",
        "options": [
            {"text_medical": "Sí, reproduce el dolor claramente", "text_patient": "Sí, claramente", "facetas": 3, "canal": 0},
            {"text_medical": "Parcialmente", "text_patient": "Un poco", "facetas": 1, "canal": 0},
            {"text_medical": "No", "text_patient": "No cambia", "facetas": 0, "canal": 0},
        ],
        "weight": 3,
        "clinical_note": "Kemp positivo — extensión + rotación ipsilateral reproduce el dolor · ALTO PESO · Facetas (86.7% concordancia)",
    },
    {
        "id": "q6",
        "section": 1,
        "medical": "¿Empeora al caminar una distancia reproducible y lo obliga a parar? (Claudicación neurógena)",
        "patient": "¿Cuando camina, siempre llega a un punto donde el dolor lo obliga a parar?",
        "options": [
            {"text_medical": "Sí, distancia reproducible", "text_patient": "Sí, siempre me paro antes de cierta distancia", "facetas": 0, "canal": 3},
            {"text_medical": "A veces", "text_patient": "A veces", "facetas": 0, "canal": 1},
            {"text_medical": "No", "text_patient": "No, puedo caminar sin que el dolor me detenga", "facetas": 1, "canal": 0},
        ],
        "weight": 3,
        "clinical_note": "Claudicación neurógena — hallazgo cardinal del Canal Estrecho · ALTO PESO",
    },
    {
        "id": "q7",
        "section": 1,
        "medical": "¿Empeora al estar de pie quieto, sin caminar?",
        "patient": "¿Le duele estar parado quieto aunque no esté caminando?",
        "options": [
            {"text_medical": "Sí, claramente", "text_patient": "Sí, mucho", "facetas": 0, "canal": 2},
            {"text_medical": "Un poco", "text_patient": "Un poco", "facetas": 0, "canal": 1},
            {"text_medical": "No", "text_patient": "No", "facetas": 0, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Bipedestación estática agrava el canal estrecho por extensión lumbar mantenida",
    },
    {
        "id": "q8",
        "section": 1,
        "medical": "¿Empeora por las mañanas o tras períodos de inactividad? (Rigidez matutina)",
        "patient": "¿Es peor el dolor al despertar o después de estar sentado mucho tiempo sin moverse?",
        "options": [
            {"text_medical": "Sí, rigidez matutina clara", "text_patient": "Sí, en las mañanas o al levantarme de la silla", "facetas": 2, "canal": 0},
            {"text_medical": "Algo", "text_patient": "Un poco", "facetas": 1, "canal": 0},
            {"text_medical": "No", "text_patient": "No, me da igual", "facetas": 0, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Rigidez matutina — patrón inflamatorio-mecánico característico de artropatía facetaria",
    },
    # ── Sección 2: Factores aliviantes ───────────────────────────────────
    {
        "id": "q9",
        "section": 2,
        "medical": "¿Mejora al inclinarse hacia adelante / empujar carrito? (Stoop sign)",
        "patient": "¿Mejora el dolor al caminar inclinado hacia adelante, como empujando un carrito del supermercado?",
        "options": [
            {"text_medical": "Sí, claramente", "text_patient": "Sí, mucho", "facetas": 0, "canal": 3},
            {"text_medical": "A veces / un poco", "text_patient": "A veces / un poco", "facetas": 0, "canal": 1},
            {"text_medical": "No", "text_patient": "No me cambia nada", "facetas": 0, "canal": 0},
        ],
        "weight": 3,
        "clinical_note": "Stoop sign positivo — ALTA especificidad para Canal Estrecho · ALTO PESO",
    },
    {
        "id": "q10",
        "section": 2,
        "medical": "¿Puede montar bicicleta con menos dolor que al caminar? (Bicycle test)",
        "patient": "¿Puede montar bicicleta con menos dolor del que siente al caminar la misma distancia?",
        "options": [
            {"text_medical": "Sí, bicicleta bien tolerada", "text_patient": "Sí, en bicicleta estoy mejor", "facetas": 0, "canal": 2},
            {"text_medical": "No monto bicicleta", "text_patient": "No monto bicicleta", "facetas": 0, "canal": 0},
            {"text_medical": "No, igual de doloroso", "text_patient": "No, me duele igual", "facetas": 0, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Bicycle test — flexión de cadera tolera bicicleta · Diferencia canal estrecho de claudicación vascular",
    },
    {
        "id": "q11",
        "section": 2,
        "medical": "¿Mejora notablemente al sentarse?",
        "patient": "¿El dolor mejora rápidamente cuando se sienta?",
        "options": [
            {"text_medical": "Sí, alivio claro al sentarse", "text_patient": "Sí, al sentarme mejoro bastante", "facetas": 0, "canal": 2},
            {"text_medical": "Un poco", "text_patient": "Un poco", "facetas": 0, "canal": 1},
            {"text_medical": "No", "text_patient": "No cambia", "facetas": 1, "canal": 0},
        ],
        "weight": 2,
        "clinical_note": "Alivio al sentarse — flexión lumbar aumenta diámetro del canal · Canal Estrecho",
    },
    # ── Sección 3: Síntomas neurológicos ─────────────────────────────────
    {
        "id": "q12",
        "section": 3,
        "medical": "¿Debilidad en piernas que aparece o empeora con la marcha?",
        "patient": "¿Siente que las piernas 'se aflojan' o se debilitan cuando lleva un rato caminando?",
        "options": [
            {"text_medical": "Sí, debilidad con la marcha", "text_patient": "Sí, claramente", "facetas": 0, "canal": 3},
            {"text_medical": "Leve sensación", "text_patient": "A veces, un poco", "facetas": 0, "canal": 1},
            {"text_medical": "No", "text_patient": "No", "facetas": 0, "canal": 0},
        ],
        "weight": 3,
        "clinical_note": "Déficit motor que aparece/empeora con marcha — claudicación neurógena motora · ALTO PESO · Canal Estrecho",
    },
    {
        "id": "q13",
        "section": 3,
        "medical": "¿Inestabilidad o dificultad para mantener equilibrio al caminar? (Romberg modificado)",
        "patient": "¿Ha sentido que pierde el equilibrio al caminar, especialmente en superficies irregulares o con poca luz?",
        "options": [
            {"text_medical": "Sí, inestabilidad clara", "text_patient": "Sí, me ha pasado", "facetas": 0, "canal": 3},
            {"text_medical": "Ocasionalmente", "text_patient": "Alguna vez", "facetas": 0, "canal": 1},
            {"text_medical": "No", "text_patient": "No", "facetas": 0, "canal": 0},
        ],
        "weight": 3,
        "clinical_note": "Romberg modificado positivo · Especificidad >90% para Canal Estrecho · ALTO PESO",
    },
]
