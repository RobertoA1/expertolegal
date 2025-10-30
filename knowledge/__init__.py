"""
Paquete de reglas de conocimiento para el Sistema de Cumplimiento legal.
Contiene las reglas de Experta organizadas por tipo de documento/normativa.
"""

from .ProteccionDatosPersonales.Ley29733 import ProteccionDatosPersonalesKB
from .PrevencionLavadoActivos.Ley27693 import PrevencionLavadoActivosKB
from .SeguridadSaludTrabajo.Ley29783 import SeguridadSaludTrabajoKB
from .ResponsabilidadAdministrativa.Ley30424 import ResponsabilidadAdministrativaKB
from .ProteccionConsumidor.Ley29571 import ProteccionConsumidorKB
from .NormasLaborales.DS003_97_TR import NormasLaboralesKB
from .NormativaSocietaria.Ley26887 import NormativaSocietariaKB
from .NormativaTributaria.DS133_2013_EF import NormativaTributariaKB
from .NormativaAmbiental import NormativaAmbientalKB

# Mapeo de tipos de documento a su base de conocimiento

KNOWLEDGE_BASES = {
    "Protección de Datos Personales": ProteccionDatosPersonalesKB,
    "Prevención de Lavado de Activos": PrevencionLavadoActivosKB,
    "Seguridad y Salud en el Trabajo": SeguridadSaludTrabajoKB,
    "Ley de Responsabilidad Administrativa de Personas Jurídicas": ResponsabilidadAdministrativaKB,
    "Protección al Consumidor": ProteccionConsumidorKB,
    "Normas Laborales": NormasLaboralesKB,
    "Normativa Societaria": NormativaSocietariaKB,
    "Normativa Tributaria": NormativaTributariaKB,
    "Normativa Ambiental": NormativaAmbientalKB
}

def obtner_knowledge_base(tipo_documento):
    """
    Obtiene la base de conocimiento segun el tipo de documento.

    Args: tipo_documento: Tipo de documento a evaluar

    Returns: Clase de KnowledgeBase correspondiente a None si no existe
    """
    return KNOWLEDGE_BASES.get(tipo_documento)

__all__ = [
    'ProteccionDatosPersonalesKB',
    'PrevencionLavadoActivosKB',
    'SeguridadSaludTrabajoKB',
    'ResponsabilidadAdministrativaKB',
    'ProteccionConsumidorKB',
    'NormasLaboralesKB',
    'NormativaSocietariaKB',
    'NormativaTributariaKB',
    'NormativaAmbientalKB',
    'KNOWLEDGE_BASES',
    'obtener_knowledge_base'
]