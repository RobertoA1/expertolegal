from __future__ import annotations
from typing import Dict, Any
from .registry import get_engine_by_id, import_classes

class EngineNotFound(Exception):
    pass


def _obtener_hechos(texto: str, tipo_documento: str):
    try:
        from gemini.gemini_service import convertirAFormatoExperta  # type: ignore
    except Exception:
        convertirAFormatoExperta = None  # type: ignore
    if convertirAFormatoExperta:
        try:
            hechos = convertirAFormatoExperta(texto, tipo_documento)
            return hechos or {}
        except Exception:
            return {}
    return {}


def _extraer_resultados_generico(motor, result_cls):
    try:
        # Buscar instancia del resultado en los hechos del motor
        for fact in list(motor.facts.values()):
            if getattr(fact, "__class__", None) is result_cls:
                # Intentar acceder como dict-like
                get = getattr(fact, "get", None)
                if callable(get):
                    return {
                        k: get(k, None) for k in [
                            "cumple", "cumple_ambiental", "cumple_consumidor",
                            "aspectos_cumplidos", "aspectos_incumplidos",
                            "recomendaciones", "explicacion"
                        ] if get(k, None) is not None
                    }
        return {}
    except Exception:
        return {}


def run_engine(engine_id: str, texto: str) -> Dict[str, Any]:
    entry = get_engine_by_id(engine_id)
    if not entry:
        raise EngineNotFound(engine_id)

    engine_cls, document_cls, result_cls = import_classes(entry)
    motor = engine_cls()
    motor.reset()

    hechos_estructura = _obtener_hechos(texto, entry.display_name)

    # Declarar resultado inicial y documento
    try:
        motor.declare(result_cls())
    except Exception:
        pass
    try:
        documento_fact = document_cls(**hechos_estructura)
    except Exception:
        documento_fact = document_cls()
    motor.declare(documento_fact)

    motor.run()

    # Intentar método específico si existe
    if hasattr(motor, "obtener_resultados"):
        try:
            return motor.obtener_resultados()
        except Exception:
            pass

    # Fallback genérico
    resultados = _extraer_resultados_generico(motor, result_cls)
    if resultados:
        return resultados
    return {
        "cumple": False,
        "aspectos_cumplidos": [],
        "aspectos_incumplidos": ["No se pudo extraer resultados"],
        "recomendaciones": []
    }
