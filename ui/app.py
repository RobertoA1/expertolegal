import sys
import os
# Agregar la carpeta padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Aplicación principal de Streamlit
import streamlit as st
import logging
from typing import Optional
from ui.flow_diagram import mostrar_diagrama_flujo
from ui.tests_page import pagina_pruebas
from engine.selector import select_engines
from engine.runner import run_engine
from engine.registry import get_engine_by_id, get_engine_by_name

try:
    from ocr.ocr_service import solicitarOCR
except ImportError:
    st.warning("⚠️ Módulo OCR no disponible")
    solicitarOCR = None

try:
    from gemini.gemini_service import convertirAFormatoExperta
except ImportError:
    st.warning("⚠️ Módulo Gemini no disponible") 
    convertirAFormatoExperta = None

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Compatibilidad Python 3.10+: asegurar collections.Mapping
import collections
import collections.abc as _collections_abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = _collections_abc.Mapping

# Configurar OCR si está disponible
try:
    from ocr.ocr_service import configurar_tesseract
    configurar_tesseract(r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    logger.info("✅ OCR configurado correctamente")
except ImportError:
    logger.warning("⚠️ OCR no disponible")
except Exception as e:
    logger.warning(f"⚠️ Error configurando OCR: {e}")

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Cumplimiento Legal",
    page_icon="⚖️",
    layout="wide"
)

# Tipos de documentos según el PDF
TIPOS_DOCUMENTO = [
    "Protección de Datos Personales",
    "Prevención de Lavado de Activos",
    "Seguridad y Salud en el Trabajo",
    "Ley de Responsabilidad Administrativa de Personas Jurídicas",
    "Protección al Consumidor",
    "Normas Laborales",
    "Normativa Societaria",
    "Normativa Tributaria",
    "Normativa Ambiental",
    "Desconozco"
]

def main():
    # Menú lateral para navegar entre páginas
    with st.sidebar:
        st.title("⚖️ Navegación")
        page = st.radio(
            "Selecciona una página:",
            ["🏠 Página Principal", "🧪 Pruebas"],
            label_visibility="collapsed"
        )
    
    # Renderizar la página seleccionada
    if page == "🏠 Página Principal":
        render_main_page()
    elif page == "🧪 Pruebas":
        pagina_pruebas()


def render_main_page():
    """Página principal del sistema"""
    st.title("⚖️ Sistema de Cumplimiento Legal")
    st.markdown("---")
    
    # 1. Selector de Tipo de Documento y modo
    st.subheader("1. Seleccione el tipo de documento")
    tipo_documento = st.selectbox(
        "Tipo de Documento:",
        TIPOS_DOCUMENTO,
        index=0
    )
    modo_seleccion = st.radio(
        "Modo de selección del motor:",
        ["Automático", "Manual"],
        horizontal=True,
        help="En modo Manual se usará el tipo de documento elegido. En Automático, el sistema elegirá el motor."
    )
    
    st.markdown("---")
    
    # 2. Campo de texto o subida de documentos
    st.subheader("2. Ingrese el contenido a evaluar")
    
    opcion_entrada = st.radio(
        "¿Cómo desea ingresar el contenido?",
        ["Escribir texto", "Subir documento"],
        horizontal=True
    )
    
    texto_input = None
    archivo_input = None
    
    if opcion_entrada == "Escribir texto":
        texto_input = st.text_area(
            "Escriba el contenido del documento:",
            height=200,
            placeholder="Ingrese aquí el texto a evaluar..."
        )
    else:
        archivo_input = st.file_uploader(
            "Suba su documento (PDF, PNG, JPG):",
            type=["pdf", "png", "jpg", "jpeg"]
        )
    
    st.markdown("---")
    
    # 3. Botón de consulta
    if st.button("🔍 Consultar Cumplimiento Legal", type="primary", use_container_width=True):
        if (opcion_entrada == "Escribir texto" and not texto_input) or \
           (opcion_entrada == "Subir documento" and not archivo_input):
            st.error("⚠️ Por favor, ingrese texto o suba un documento antes de consultar.")
        else:
            consultar_cumplimiento(tipo_documento, texto_input, archivo_input, modo_seleccion)
    
    st.markdown("---")
    
    # 4. Mensaje de advertencia
    st.info("ℹ️ **Esta herramienta es un asistente. La decisión final debe ser tomada por un humano calificado.**")


def consultar_cumplimiento(tipo_documento: str, texto_input: str = None, archivo_input = None, modo_seleccion: str = "Automático") -> dict:
    """
    Consulta el cumplimiento legal usando el motor de reglas Experta
    """
    try:
        # Paso 1: Extraer texto del documento
        st.markdown("### 📄 Paso 1: Extrayendo texto del documento...")
        
        hechos_texto = None
        
        if archivo_input is not None:
            # Procesar archivo subido
            if solicitarOCR:
                hechos_texto = solicitarOCR(archivo_input)
            else:
                st.warning("⚠️ OCR no disponible, usando simulación")
                hechos_texto = "Simulación: Política de privacidad con datos personales..."
        elif texto_input:
            # Usar texto ingresado directamente
            hechos_texto = texto_input
            st.success(f"✅ Texto ingresado: {len(hechos_texto)} caracteres")
        else:
            st.error("❌ No se proporcionó texto ni archivo")
            return crear_resultado_error("No hay contenido para evaluar")
        
        if not hechos_texto:
            st.error("❌ No se pudo extraer texto del documento")
            return crear_resultado_error("Error en extracción de texto")
        
        # Paso 2: Evaluar con motor de reglas
        st.markdown("### ⚖️ Paso 2: Evaluando cumplimiento legal...")
        
        # Modo Manual: usar el tipo seleccionado por el usuario
        if modo_seleccion == "Manual" and tipo_documento != "Desconozco":
            entry_manual = get_engine_by_name(tipo_documento)
            if entry_manual:
                st.info(f"🧭 Motor seleccionado (Manual): {entry_manual.display_name}")
                resultados = run_engine(entry_manual.id, hechos_texto)
                if resultados:
                    mostrar_resultados_evaluacion(resultados, entry_manual.display_name)
                    return resultados
                st.info("🔄 Mostrando evaluación de ejemplo...")
                mostrar_resultados_ejemplo()
                return crear_resultado_error("No se obtuvieron resultados del motor (Manual)")
            else:
                st.warning("⚠️ Tipo de documento no reconocido. Usando selección automática.")
        
        # Selección Automática del motor (fuera de la UI)
        candidatos = select_engines(hechos_texto, top_k=1)
        if not candidatos:
            st.info("🔄 Mostrando evaluación de ejemplo...")
            mostrar_resultados_ejemplo()
            return crear_resultado_error("No se pudo seleccionar un motor")
        engine_id, score = candidatos[0]
        entry = get_engine_by_id(engine_id)
        if entry:
            st.info(f"🧭 Motor seleccionado: {entry.display_name}")
        resultados = run_engine(engine_id, hechos_texto)
        if resultados:
            mostrar_resultados_evaluacion(resultados, entry.display_name if entry else "")
            return resultados
        st.info("🔄 Mostrando evaluación de ejemplo...")
        mostrar_resultados_ejemplo()
        return crear_resultado_error("No se obtuvieron resultados del motor")
            
    except Exception as e:
        logger.error(f"Error en consultar_cumplimiento: {e}")
        st.error(f"❌ Error general en evaluación: {str(e)}")
        st.info("🔄 Mostrando evaluación de ejemplo...")
        mostrar_resultados_ejemplo()
        return crear_resultado_error("Error del sistema")


def obtener_hechos_gemini(texto: str, tipo_documento: str):
    """Obtiene hechos usando Gemini AI"""
    if convertirAFormatoExperta:
        try:
            hechos = convertirAFormatoExperta(texto, tipo_documento)
            if hechos:
                st.success("✅ Hechos analizados por Gemini AI")
                st.write("DEBUG - Hechos de Gemini:", hechos)  # ← AÑADIR ESTO
                return hechos
            else:
                st.warning("⚠️ Gemini devolvió None. Usando simulación...")
                return None
        except Exception as e:
            st.warning(f"⚠️ Error en Gemini: {e}. Usando simulación...")
            return None
    else:
        st.info("ℹ️ Gemini no está disponible. Usando simulación...")
        return None


def mostrar_hechos_identificados(hechos_estructura: dict):
    """Muestra los hechos identificados en un expander"""
    with st.expander("📋 Ver hechos identificados"):
        for clave, valor in hechos_estructura.items():
            icono = "✅" if valor else "❌"
            clave_limpia = clave.replace("_", " ").title()
            st.write(f"{icono} **{clave_limpia}**: {valor}")


def ejecutar_motor_reglas(motor, hechos_estructura: dict, DocumentoClase, ResultadoClase):
    """Ejecuta el motor de reglas de Experta"""
    st.markdown("### ⚖️ Paso 4: Ejecutando motor de reglas...")
    
    try:
        with st.spinner("Preparando evaluación..."):
            # DEBUG: Mostrar hechos que se enviarán al motor
            with st.expander("🔍 DEBUG - Hechos enviados al motor"):
                st.json(hechos_estructura)
            
            # Crear fact de resultado inicial
            motor.declare(ResultadoClase())
            
            # Crear fact del documento
            documento_fact = DocumentoClase(**hechos_estructura)
            motor.declare(documento_fact)
        
        with st.spinner("Evaluando cumplimiento legal..."):
            motor.run()
            st.success("✅ Motor de reglas ejecutado correctamente")
        
        with st.spinner("Procesando resultados..."):
            resultados = motor.obtener_resultados()
        
        if resultados:
            st.success("✅ Evaluación completada con éxito")
            mostrar_resultados_evaluacion(resultados, "")
            return resultados
        else:
            st.error("❌ No se pudieron obtener resultados del motor de reglas")
            st.info("🔄 Mostrando evaluación de ejemplo...")
            mostrar_resultados_ejemplo()
            return crear_resultado_error("Error en motor de reglas")
            
    except Exception as e:
        st.error(f"❌ Error ejecutando motor de reglas: {str(e)}")
        logger.error(f"Error en motor de reglas: {e}")
        
        # DEBUG MEJORADO: Mostrar más detalles del error
        with st.expander("🐛 Ver detalles técnicos del error"):
            st.code(f"Tipo de error: {type(e).__name__}")
            st.code(f"Mensaje: {str(e)}")
            import traceback
            st.code(f"Traceback: {traceback.format_exc()}")
        
        st.info("🔄 Mostrando evaluación de ejemplo...")
        mostrar_resultados_ejemplo()
        return crear_resultado_error("Error técnico en evaluación")


def mostrar_resultados_evaluacion(resultados: dict, tipo_documento: str):
    """Muestra los resultados de la evaluación legal real"""
    st.success("✅ Procesamiento completado")
    st.markdown("### 📋 Resultados del Análisis")
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    # Detectar qué clave de cumplimiento usar
    clave_cumple = None
    for key in resultados.keys():
        if key.startswith('cumple'):
            clave_cumple = key
            break
    
    with col1:
        cumple = resultados.get(clave_cumple, False) if clave_cumple else False
        st.metric(
            "Estado General", 
            "✅ CUMPLE" if cumple else "❌ NO CUMPLE"
        )
    
    with col2:
        aspectos_cumplidos = resultados.get('aspectos_cumplidos', [])
        num_cumplidos = len(aspectos_cumplidos) if isinstance(aspectos_cumplidos, list) else 0
        st.metric("Aspectos Cumplidos", num_cumplidos)
    
    with col3:
        aspectos_incumplidos = resultados.get('aspectos_incumplidos', [])
        num_incumplidos = len(aspectos_incumplidos) if isinstance(aspectos_incumplidos, list) else 0
        st.metric("Aspectos Incumplidos", num_incumplidos)
    
    # Detalles de cumplimiento
    st.markdown("#### 📊 Detalle por Aspectos:")
    
    # Aspectos cumplidos
    if resultados.get('aspectos_cumplidos'):
        st.markdown("**✅ Aspectos que SÍ cumple:**")
        for aspecto in resultados['aspectos_cumplidos']:
            st.success(f"✅ {aspecto}")
    
    # Aspectos incumplidos
    if resultados.get('aspectos_incumplidos'):
        st.markdown("**❌ Aspectos que NO cumple:**")
        for aspecto in resultados['aspectos_incumplidos']:
            if isinstance(aspecto, dict):
                severidad_icon = "🔴" if aspecto.get('severidad') == 'crítica' else "🟡"
                st.error(f"{severidad_icon} **{aspecto.get('aspecto', 'N/A')}**: {aspecto.get('descripcion', 'Sin descripción')}")
            else:
                st.error(f"❌ {aspecto}")
    
    # Recomendaciones
    if resultados.get('recomendaciones'):
        st.markdown("#### 💡 Recomendaciones:")
        for recomendacion in resultados['recomendaciones']:
            st.info(f"💡 {recomendacion}")


def mostrar_resultados_ejemplo():
    """Fallback con resultados de ejemplo"""
    st.success("✅ Procesamiento completado")
    st.markdown("### 📋 Resultados del Análisis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cumplimiento General", "85%", "+5%")
    with col2:
        st.metric("Reglas Evaluadas", "3", "")
    
    st.markdown("#### Detalle de Cumplimiento:")
    st.success("✅ **Regla 1**: Cumple con los requisitos de consentimiento informado")
    st.warning("⚠️ **Regla 2**: Falta incluir cláusula de tratamiento de datos")
    st.success("✅ **Regla 3**: Cumple con registro de banco de datos")
    st.info("💡 **Recomendación**: Agregar cláusula específica sobre tratamiento y conservación de datos personales.")


def crear_resultado_error(mensaje: str) -> dict:
    """Crea un resultado de error estándar"""
    return {
        'cumple': False,
        'aspectos_cumplidos': [],
        'aspectos_incumplidos': [mensaje],
        'recomendaciones': ['Revisar el documento e intentar nuevamente']
    }


def mostrar_diagrama_flujo_wrapper(tipo_documento: str, es_imagen: bool):
    """Muestra el diagrama de flujo del proceso usando streamlit-flow"""
    # Para producción:
    mostrar_diagrama_flujo(tipo_documento, es_imagen, paso_actual=0)

def corregir_hechos_lavado_activos(hechos: dict) -> dict:
    """Corrige los nombres de campos devueltos por Gemini para Lavado de Activos"""
    if not hechos:
        return hechos
    
    mapeo_correcciones = {
        "tiene_politica_pla": "tiene_manual_prevencion",
        "menciona_uff": "menciona_uif_peru",
        "menciona_operaciones_sospechosas": "tiene_reporte_operaciones_sospechosas", 
        "tiene_capacitacion_empleados": "tiene_capacitaciones",
        "menciona_sanciones": "tiene_evaluacion_riesgos"
    }
    
    hechos_corregidos = {}
    
    for clave, valor in hechos.items():
        if clave in mapeo_correcciones:
            hechos_corregidos[mapeo_correcciones[clave]] = valor
        else:
            hechos_corregidos[clave] = valor
    
    # Asegurar campos faltantes
    campos_requeridos = [
        "tiene_manual_prevencion", "tiene_politicas_prevencion",
        "tiene_identificacion_clientes", "tiene_registro_operaciones", 
        "tiene_reporte_operaciones_sospechosas", "tiene_oficial_cumplimiento",
        "tiene_capacitaciones", "tiene_evaluacion_riesgos",
        "tiene_debida_diligencia", "menciona_uif_peru"
    ]
    
    for campo in campos_requeridos:
        if campo not in hechos_corregidos:
            hechos_corregidos[campo] = False
    
    return hechos_corregidos

def corregir_hechos_sst(hechos: dict) -> dict:
    """Corrige los nombres de campos devueltos por Gemini para SST"""
    if not hechos:
        return hechos
    
    mapeo_correcciones = {
        "tíene_reglamento_interno": "tiene_reglamento_interno",
        "tíene_politica_sst": "tiene_politica_sst",
        "tíene_comite_sst": "tiene_comite_sst", 
        "tíene_supervisor_sst": "tiene_supervisor_sst",
        "tíene_matriz_iper": "tiene_matriz_iper",
        "tíene_plan_anual": "tiene_plan_anual",
        "tíene_registros_obligatorios": "tiene_registros_obligatorios",
        "tíene_registro_accidentes": "tiene_registro_accidentes",
        "tíene_capacitaciones": "tiene_capacitaciones",
        "tíene_examenes_medicos": "tiene_examenes_medicos",
        "tíene_epp": "tiene_epp",
        "tíene_procedimientos_trabajo_seguro": "tiene_procedimientos_trabajo_seguro",
        "menciona_responsabilidades": "menciona_responsabilidades"
    }
    
    hechos_corregidos = {}
    
    for clave, valor in hechos.items():
        if clave in mapeo_correcciones:
            hechos_corregidos[mapeo_correcciones[clave]] = valor
        else:
            hechos_corregidos[clave] = valor
    
    # Asegurar campos faltantes
    campos_requeridos = [
        "tiene_reglamento_interno", "tiene_politica_sst", "tiene_comite_sst",
        "tiene_supervisor_sst", "tiene_matriz_iper", "tiene_plan_anual",
        "tiene_registros_obligatorios", "tiene_registro_accidentes", 
        "tiene_capacitaciones", "tiene_examenes_medicos", "tiene_epp",
        "tiene_procedimientos_trabajo_seguro", "menciona_responsabilidades",
        "numero_trabajadores"
    ]
    
    for campo in campos_requeridos:
        if campo not in hechos_corregidos:
            if campo == "numero_trabajadores":
                hechos_corregidos[campo] = 0
            else:
                hechos_corregidos[campo] = False
    
    return hechos_corregidos

def corregir_hechos_consumidor(hechos: dict) -> dict:
    """Corrige los nombres de campos devueltos por Gemini para Protección al Consumidor"""
    if not hechos:
        return hechos
    
    mapeo_correcciones = {
        "garantiza_idoneidad_producto": "garantiza_idoneidad",
        "menciona_medidas_seguridad": "menciona_riesgos_seguridad",
        "publicidad_veraz": "es_publicidad_clara_veraz",
        "clausulas_claras": "tiene_clausulas_transparentes",
        "libro_reclamaciones": "tiene_libro_reclamaciones_fisico_virtual",
        "plazo_respuesta_30_dias": "cumple_plazo_respuesta_reclamos",
        "pago_anticipado_sin_penalidad": "ofrece_posibilidad_pago_anticipado"
    }
    
    hechos_corregidos = {}
    
    for clave, valor in hechos.items():
        if clave in mapeo_correcciones:
            hechos_corregidos[mapeo_correcciones[clave]] = valor
        else:
            hechos_corregidos[clave] = valor
    
    # Asegurar campos faltantes
    campos_requeridos = [
        "garantiza_idoneidad", "menciona_riesgos_seguridad", 
        "es_publicidad_clara_veraz", "tiene_clausulas_transparentes",
        "tiene_libro_reclamaciones_fisico_virtual", "cumple_plazo_respuesta_reclamos",
        "ofrece_posibilidad_pago_anticipado"
    ]
    
    for campo in campos_requeridos:
        if campo not in hechos_corregidos:
            hechos_corregidos[campo] = False
    
    return hechos_corregidos

def corregir_hechos_laborales(hechos: dict) -> dict:
    """Corrige los nombres de campos devueltos por Gemini para Normas Laborales"""
    if not hechos:
        return hechos
    
    mapeo_correcciones = {
        "contratos_escritos": "tiene_contratos_escritos_vigentes",
        "periodo_prueba": "tiene_periodo_prueba_informado",
        "planilla_electronica": "tiene_registro_planilla_electronica",
        "boletas_pago": "entrega_boletas_pago_oportunas",
        "reglamento_interno": "tiene_reglamento_interno_trabajo",
        "control_asistencia": "registra_control_asistencia",
        "registro_asistencia": "registra_control_asistencia"
    }
    
    hechos_corregidos = {}
    
    for clave, valor in hechos.items():
        if clave in mapeo_correcciones:
            hechos_corregidos[mapeo_correcciones[clave]] = valor
        else:
            hechos_corregidos[clave] = valor
    
    # Asegurar campos faltantes
    campos_requeridos = [
        "tiene_contratos_escritos_vigentes",
        "tiene_periodo_prueba_informado", 
        "tiene_registro_planilla_electronica",
        "entrega_boletas_pago_oportunas",
        "tiene_reglamento_interno_trabajo",
        "registra_control_asistencia"
    ]
    
    for campo in campos_requeridos:
        if campo not in hechos_corregidos:
            hechos_corregidos[campo] = False
    
    return hechos_corregidos

def corregir_hechos_societarios(hechos: dict) -> dict:
    """Corrige los nombres de campos devueltos por Gemini para Normativa Societaria"""
    if not hechos:
        return hechos
    
    mapeo_correcciones = {
        "escritura_publica": "esta_constituida_escritura_publica",
        "inscrita_sunarp": "esta_inscrita_registros_publicos",
        "inscrita_registros_publicos": "esta_inscrita_registros_publicos",
        "estatutos_actualizados": "tiene_estatuto_actualizado",
        "capital_suscrito": "capital_suscrito_totalmente",
        "capital_pagado": "capital_pagado_minimo",
        "pluralidad": "mantiene_pluralidad_socios",
        "libro_actas": "tiene_libro_actas_junta_general",
        "libro_matricula": "tiene_libro_matricula_acciones",
        "libro_directorio": "tiene_libro_actas_directorio",
        "actas_junta": "tiene_libro_actas_junta_general",
        "matricula_acciones": "tiene_libro_matricula_acciones",
        "actas_directorio": "tiene_libro_actas_directorio"
    }
    
    hechos_corregidos = {}
    
    for clave, valor in hechos.items():
        if clave in mapeo_correcciones:
            hechos_corregidos[mapeo_correcciones[clave]] = valor
        else:
            hechos_corregidos[clave] = valor
    
    # Asegurar campos faltantes
    campos_requeridos = [
        "esta_constituida_escritura_publica",
        "esta_inscrita_registros_publicos",
        "tiene_estatuto_actualizado",
        "capital_suscrito_totalmente",
        "capital_pagado_minimo",
        "mantiene_pluralidad_socios",
        "tiene_libro_actas_junta_general",
        "tiene_libro_matricula_acciones",
        "tiene_libro_actas_directorio"
    ]
    
    for campo in campos_requeridos:
        if campo not in hechos_corregidos:
            hechos_corregidos[campo] = False
    
    return hechos_corregidos

def corregir_hechos_tributarios(hechos: dict) -> dict:
    """Corrige los nombres de campos devueltos por Gemini para Normativa Tributaria"""
    if not hechos:
        return hechos
    
    mapeo_correcciones = {
        "libros_obligatorios": "tiene_libros_obligatorios_vigentes",
        "libros_actualizados": "libros_cumplen_plazo_maximo_atraso",
        "libros_al_dia": "libros_cumplen_plazo_maximo_atraso",
        "emite_comprobantes": "emite_comprobantes_pago_por_ventas",
        "comprobantes_ventas": "emite_comprobantes_pago_por_ventas",
        "sustento_gastos": "comprobantes_sustentan_costo_gasto",
        "declaracion_mensual": "presenta_declaracion_jurada_mensual",
        "declaracion_anual": "presenta_declaracion_jurada_anual",
        "domicilio_actualizado": "domicilio_fiscal_comunicado_sunat",
        "ruc_actualizado": "domicilio_fiscal_comunicado_sunat"
    }
    
    hechos_corregidos = {}
    
    for clave, valor in hechos.items():
        if clave in mapeo_correcciones:
            hechos_corregidos[mapeo_correcciones[clave]] = valor
        else:
            hechos_corregidos[clave] = valor
    
    # Asegurar campos faltantes
    campos_requeridos = [
        "tiene_libros_obligatorios_vigentes",
        "libros_cumplen_plazo_maximo_atraso",
        "emite_comprobantes_pago_por_ventas",
        "comprobantes_sustentan_costo_gasto",
        "presenta_declaracion_jurada_mensual",
        "presenta_declaracion_jurada_anual",
        "domicilio_fiscal_comunicado_sunat"
    ]
    
    for campo in campos_requeridos:
        if campo not in hechos_corregidos:
            hechos_corregidos[campo] = False
    
    return hechos_corregidos

def corregir_hechos_ambientales(hechos: dict) -> dict:
    """Corrige los nombres de campos devueltos por Gemini para Normativa Ambiental"""
    if not hechos:
        return hechos
    
    mapeo_correcciones = {
        "tiene_estudio_impacto": "tiene_estudio_impacto_ambiental",
        "eia_aprobado": "tiene_estudio_impacto_ambiental",
        "estudio_impacto": "tiene_estudio_impacto_ambiental",
        "monitoreo_activo": "tiene_monitoreo_ambiental",
        "monitoreo_ambiental_activo": "tiene_monitoreo_ambiental",
        "cumple_limites": "cumple_LMP_ECA",
        "cumple_lmp_eca": "cumple_LMP_ECA",
        "registro_residuos": "tiene_registro_residuos_solidos",
        "autorizacion_vertimiento": "tiene_autorizacion_vertimientos",
        "plan_manejo": "tiene_plan_manejo_ambiental",
        "sistema_gestion": "tiene_sistema_gestion_ambiental",
        "plan_contingencia": "tiene_plan_contigencia",
        "tiene_permisos_ambientales": "tiene_autorizacion_vertimientos",  # Mapeo alternativo
        "tiene_responsable_ambiental": "tiene_sistema_gestion_ambiental", # Mapeo alternativo
        "menciona_limites_emisiones": "cumple_LMP_ECA"  # Mapeo alternativo
    }
    
    hechos_corregidos = {}
    
    for clave, valor in hechos.items():
        if clave in mapeo_correcciones:
            hechos_corregidos[mapeo_correcciones[clave]] = valor
        else:
            hechos_corregidos[clave] = valor
    
    # Asegurar campos faltantes
    campos_requeridos = [
        "tiene_estudio_impacto_ambiental",
        "tiene_monitoreo_ambiental",
        "cumple_LMP_ECA",
        "tiene_registro_residuos_solidos",
        "tiene_autorizacion_vertimientos",
        "tiene_plan_manejo_ambiental",
        "tiene_sistema_gestion_ambiental",
        "tiene_plan_contigencia"
    ]
    
    for campo in campos_requeridos:
        if campo not in hechos_corregidos:
            hechos_corregidos[campo] = False
    
    return hechos_corregidos

if __name__ == "__main__":
    main()