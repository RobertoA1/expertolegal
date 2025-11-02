import importlib
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class EngineEntry:
    id: str
    display_name: str
    module: str
    engine_class: str
    document_class: str
    result_class: str
    keywords: List[str]

_REGISTRY: Dict[str, EngineEntry] = {
    "proteccion_datos": EngineEntry(
        id="proteccion_datos",
        display_name="Protección de Datos Personales",
        module="knowledge.ProteccionDatosPersonales.Ley29733",
        engine_class="ProteccionDatosPersonalesKB",
        document_class="DocumentoProteccionDatos",
        result_class="ResultadoEvaluacion",
        keywords=[
            "datos personales","privacidad","consentimiento","ARCO","banco de datos","RNPDP","Ley 29733"
        ],
    ),
    "lavado_activos": EngineEntry(
        id="lavado_activos",
        display_name="Prevención de Lavado de Activos",
        module="knowledge.PrevencionLavadoActivos.Ley27693",
        engine_class="PrevencionLavadoActivosKB",
        document_class="DocumentoLavadoActivos",
        result_class="ResultadoEvaluacion",
        keywords=[
            "lavado de activos","PLA","UIF","sospechosas","KYC","27693"
        ],
    ),
    "sst": EngineEntry(
        id="sst",
        display_name="Seguridad y Salud en el Trabajo",
        module="knowledge.SeguridadSaludTrabajo.Ley29783",
        engine_class="SeguridadSaludTrabajoKB",
        document_class="DocumentoSST",
        result_class="ResultadoEvaluacion",
        keywords=[
            "seguridad y salud","SST","IPER","comite","EPP","29783"
        ],
    ),
    "ra_30424": EngineEntry(
        id="ra_30424",
        display_name="Ley de Responsabilidad Administrativa de Personas Jurídicas",
        module="knowledge.ResponsabilidadAdministrativa.Ley30424",
        engine_class="ResponsabilidadAdministrativaKB",
        document_class="DocumentoModeloPrevencion",
        result_class="ResultadoEvaluacion30424",
        keywords=[
            "modelo de prevención","soborno","cohecho","30424","responsabilidad administrativa"
        ],
    ),
    "consumidor": EngineEntry(
        id="consumidor",
        display_name="Protección al Consumidor",
        module="knowledge.ProteccionConsumidor.Ley29571",
        engine_class="ProteccionConsumidorKB",
        document_class="DocumentoConsumidor",
        result_class="ResultadoEvaluacion29571",
        keywords=[
            "consumidor","libro de reclamaciones","publicidad","idoneidad","29571"
        ],
    ),
    "laboral": EngineEntry(
        id="laboral",
        display_name="Normas Laborales",
        module="knowledge.NormasLaborales.DS003_97_TR",
        engine_class="NormasLaboralesKB",
        document_class="DocumentoNormaLaboral",
        result_class="ResultadoEvaluacionLaboral",
        keywords=[
            "planilla","boletas","contratos","reglamento interno","asistencia","003-97-TR"
        ],
    ),
    "societaria": EngineEntry(
        id="societaria",
        display_name="Normativa Societaria",
        module="knowledge.NormativaSocietaria.Ley26887",
        engine_class="NormativaSocietariaKB",
        document_class="DocumentoSocietario",
        result_class="ResultadoEvaluacionSocietaria",
        keywords=[
            "estatuto","acciones","junta","matricula","directorio","26887"
        ],
    ),
    "tributaria": EngineEntry(
        id="tributaria",
        display_name="Normativa Tributaria",
        module="knowledge.NormativaTributaria.DS133_2013_EF",
        engine_class="NormativaTributariaKB",
        document_class="DocumentoTributario",
        result_class="ResultadoEvaluacionTributaria",
        keywords=[
            "SUNAT","comprobantes","libros contables","declaración jurada","133-2013-EF"
        ],
    ),
    "ambiental": EngineEntry(
        id="ambiental",
        display_name="Normativa Ambiental",
        module="knowledge.NormativaAmbiental.Ley28611",
        engine_class="NormativaAmbientalKB",
        document_class="AspectoAmbiental",
        result_class="ResultadoEvaluacionAmbiental",
        keywords=[
            "impacto ambiental","EIA","OEFA","LMP","ECA","residuos","vertimientos","28611"
        ],
    ),
}

def get_registry() -> Dict[str, EngineEntry]:
    return _REGISTRY


def get_engine_by_id(engine_id: str) -> Optional[EngineEntry]:
    return _REGISTRY.get(engine_id)


def get_engine_by_name(display_name: str) -> Optional[EngineEntry]:
    for e in _REGISTRY.values():
        if e.display_name == display_name:
            return e
    return None


def import_classes(entry: EngineEntry):
    mod = importlib.import_module(entry.module)
    engine_cls = getattr(mod, entry.engine_class)
    document_cls = getattr(mod, entry.document_class)
    result_cls = getattr(mod, entry.result_class)
    return engine_cls, document_cls, result_cls
