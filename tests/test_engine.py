import pytest

from engine.runner import run_engine, _obtener_hechos  # type: ignore
from engine.selector import select_engines
from engine.registry import get_engine_by_id

@pytest.fixture
def patch_hechos(monkeypatch):
    def _patch(hechos):
        monkeypatch.setattr("engine.runner._obtener_hechos", lambda texto, tipo: hechos)
    return _patch

def test_engine_inferencia_correcta_ambiental(patch_hechos):
    hechos = {
        "tiene_estudio_impacto_ambiental": False,
        "tiene_monitoreo_ambiental": True,
        "cumple_LMP_ECA": True,
        "tiene_registro_residuos_solidos": True,
        "tiene_autorizacion_vertimientos": True,
        "tiene_plan_manejo_ambiental": True,
        "tiene_sistema_gestion_ambiental": True,
        "tiene_plan_contigencia": True,
    }
    patch_hechos(hechos)

    resultados = run_engine("ambiental", "texto de prueba ambiental")

    assert resultados.get("cumple_ambiental") is False

    aspectos_incumplidos = resultados.get("aspectos_incumplidos")
    assert len(aspectos_incumplidos) == 1
    assert aspectos_incumplidos[0].get("severidad") in ("crítica", "critica")

def test_engine_caso_borde_hechos_vacios(patch_hechos):
    patch_hechos({})
    resultados = run_engine("ambiental", "")

    assert isinstance(resultados, dict)
    assert "aspectos_cumplidos" in resultados
    assert "aspectos_incumplidos" in resultados
    assert isinstance(resultados.get("aspectos_incumplidos"), list)


def test_engine_explicacion_ambiental(patch_hechos):
    hechos = {"tiene_estudio_impacto_ambiental": False}
    patch_hechos(hechos)

    resultados = run_engine("ambiental", "texto")

    explicacion = resultados.get("explicacion", "")
    assert isinstance(explicacion, str)
    assert "Falta Estudio de Impacto Ambiental" in explicacion
