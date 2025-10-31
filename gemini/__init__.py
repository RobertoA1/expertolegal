"""
Módulo de integración con Google Gemini para análisis de documentos legales.
"""

from .gemini_service import consultarTipoDocumento, convertirAFormatoExperta

__all__ = ['consultarTipoDocumento', 'convertirAFormatoExperta']