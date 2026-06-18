"""
Modelos de dominio del motor de clasificación.

Define la taxonomía (enums) y el resultado de una clasificación. Mantener la
taxonomía en un único lugar permite reutilizarla tanto al construir el prompt
como al validar la respuesta del LLM (una sola fuente de verdad).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum


class _LabelEnum(str, Enum):
    """
    Enum base cuyos miembros se comportan como strings.

    Aporta utilidades comunes a todas las taxonomías: listar las etiquetas
    válidas y parsear un valor recibido del LLM de forma tolerante.
    """

    @classmethod
    def values(cls) -> list[str]:
        """Devuelve las etiquetas válidas como lista de strings."""
        return [member.value for member in cls]

    @classmethod
    def parse(cls, value: str) -> "_LabelEnum":
        """
        Convierte un string (posible salida del LLM) en un miembro del enum.

        El match es case-insensitive y tolera espacios. Lanza ValueError si la
        etiqueta no pertenece a la taxonomía, para no aceptar valores inventados.
        """
        normalized = (value or "").strip().upper()
        for member in cls:
            if member.value.upper() == normalized:
                return member
        raise ValueError(
            f"'{value}' no es un valor válido para {cls.__name__}. "
            f"Valores permitidos: {cls.values()}"
        )


class SensitivityLevel(_LabelEnum):
    """Nivel de sensibilidad del dato, de menor a mayor."""

    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class Category(_LabelEnum):
    """Categoría del dato según su naturaleza."""

    PII = "PII"                  # Datos personales identificables
    PCI = "PCI"                  # Datos de tarjetas / pagos
    PHI = "PHI"                  # Datos de salud
    CREDENTIALS = "CREDENTIALS"  # Secretos, tokens, contraseñas
    FINANCIAL = "FINANCIAL"      # Información financiera de la empresa
    INTELLECTUAL_PROPERTY = "INTELLECTUAL_PROPERTY"
    GENERAL = "GENERAL"          # Sin contenido sensible


class RiskLevel(_LabelEnum):
    """Riesgo asociado a la exposición del dato."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class ClassificationResult:
    """
    Resultado estructurado de clasificar un texto.

    Attributes:
        text: el texto original analizado.
        sensitivity: nivel de sensibilidad asignado.
        category: categoría asignada.
        risk: nivel de riesgo asignado.
        rationale: breve justificación generada por el modelo.
    """

    text: str
    sensitivity: SensitivityLevel
    category: Category
    risk: RiskLevel
    rationale: str

    def to_dict(self) -> dict:
        """Serializa el resultado a un dict con valores string (apto para JSON)."""
        data = asdict(self)
        data["sensitivity"] = self.sensitivity.value
        data["category"] = self.category.value
        data["risk"] = self.risk.value
        return data
