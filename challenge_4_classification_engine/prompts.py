"""
Construcción de prompts para el LLM.

Aísla la "ingeniería de prompt" del resto de la lógica: el prompt se arma a
partir de la taxonomía definida en `models.py`, de modo que si cambian las
etiquetas no hay que tocar el texto del prompt a mano.
"""

from __future__ import annotations

from .models import Category, RiskLevel, SensitivityLevel

SYSTEM_PROMPT = """\
Sos un motor de clasificación de datos para un equipo de ciberseguridad.
Analizás textos cortos y los clasificás por sensibilidad, categoría y riesgo.

Reglas:
- Respondé SIEMPRE y SOLO con un objeto JSON válido, sin texto adicional ni markdown.
- Usá EXCLUSIVAMENTE las etiquetas permitidas para cada campo.
- 'rationale' debe ser una justificación breve (una o dos frases), en español.
- No incluyas en 'rationale' datos sensibles textuales (no repitas tarjetas, tokens, etc.).

Formato de salida exacto:
{
  "sensitivity": "<una de: %(sensitivities)s>",
  "category": "<una de: %(categories)s>",
  "risk": "<una de: %(risks)s>",
  "confidence": <número entre 0.0 y 1.0 con tu nivel de confianza>,
  "rationale": "<justificación breve>"
}
""" % {
    "sensitivities": ", ".join(SensitivityLevel.values()),
    "categories": ", ".join(Category.values()),
    "risks": ", ".join(RiskLevel.values()),
}


def build_user_prompt(text: str) -> str:
    """
    Arma el mensaje de usuario con el texto a clasificar.

    Parameters:
        text (str): texto corto a analizar.

    Returns:
        str: prompt listo para enviar como mensaje 'user'.
    """
    return f"Clasificá el siguiente texto:\n\n\"\"\"\n{text}\n\"\"\""
