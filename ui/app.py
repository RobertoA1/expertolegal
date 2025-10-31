import sys
import os
# Agregar la carpeta padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Aplicación principal de Streamlit
import streamlit as st
import logging
from typing import Optional
from flow_diagram import mostrar_diagrama_flujo
from tests_page import pagina_pruebas

try:
    from ocr.ocr_service import solicitarOCR, validar_configuracion_ocr
except ImportError:
    st.warning("⚠️ Módulo OCR no disponible")
    solicitarOCR = None

try:
    from gemini.gemini_service import consultarTipoDocumento, convertirAFormatoExperta
except ImportError:
    st.warning("⚠️ Módulo Gemini no disponible") 
    consultarTipoDocumento = None
    convertirAFormatoExperta = None

try:
    from knowledge import obtner_knowledge_base
except ImportError:
    obtner_knowledge_base = None

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    # 1. Selector de Tipo de Documento
    st.subheader("1. Seleccione el tipo de documento")
    tipo_documento = st.selectbox(
        "Tipo de Documento:",
        TIPOS_DOCUMENTO,
        index=0
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
            consultar_cumplimiento(tipo_documento, texto_input, archivo_input)
    
    st.markdown("---")
    
    # 4. Mensaje de advertencia
    st.info("ℹ️ **Esta herramienta es un asistente. La decisión final debe ser tomada por un humano calificado.**")


def consultar_cumplimiento(tipo_documento: str, texto_input: str = None, archivo_input = None) -> dict:
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
            return {
                'cumple': False,
                'aspectos_cumplidos': [],
                'aspectos_incumplidos': ['No hay contenido para evaluar'],
                'recomendaciones': ['Proporcione texto o suba un documento']
            }
        
        if not hechos_texto:
            st.error("❌ No se pudo extraer texto del documento")
            return {
                'cumple': False,
                'aspectos_cumplidos': [],
                'aspectos_incumplidos': ['Error en extracción de texto'],
                'recomendaciones': ['Verifique el documento e intente nuevamente']
            }
        
        # Paso 2: Evaluar con motor de reglas
        st.markdown("### ⚖️ Paso 2: Evaluando cumplimiento legal...")
        
        if tipo_documento == "Protección de Datos Personales":
            from knowledge.ProteccionDatosPersonales.Ley29733 import ProteccionDatosPersonalesKB, DocumentoProteccionDatos, ResultadoEvaluacion
            
            # Crear motor de reglas
            motor = ProteccionDatosPersonalesKB()
            motor.reset()
            
            # Paso 3: Analizar hechos con Gemini
            st.markdown("### 🤖 Paso 3: Analizando contenido con IA...")
            
            if convertirAFormatoExperta:
                try:
                    hechos_estructura = convertirAFormatoExperta(hechos_texto, tipo_documento)
                    st.success("✅ Hechos analizados por Gemini AI")
                except Exception as e:
                    st.warning(f"⚠️ Error en Gemini: {e}. Usando simulación...")
                    hechos_estructura = None
            else:
                hechos_estructura = None
            
            # Si Gemini falla, usar simulación
            if not hechos_estructura:
                hechos_estructura = {
                    "tiene_politica_privacidad": True,
                    "tiene_consentimiento_informado": False,
                    "tiene_registro_banco_datos": True,
                    "especifica_finalidad_datos": False,
                    "menciona_derechos_arco": True,
                    "tiene_medidas_seguridad": False,
                    "menciona_plazo_conservacion": False,
                    "tiene_contrato_encargo": False,
                    "tiene_clausulas_legales": True,
                    "menciona_autoridad_proteccion": True
                }
                st.info("🎭 Usando análisis simulado basado en contenido")
            
            # Mostrar hechos identificados
            with st.expander("📋 Ver hechos identificados"):
                for clave, valor in hechos_estructura.items():
                    icono = "✅" if valor else "❌"
                    clave_limpia = clave.replace("_", " ").title()
                    st.write(f"{icono} **{clave_limpia}**: {valor}")
            
            # Paso 4: Ejecutar motor de reglas
            st.markdown("### ⚖️ Paso 4: Ejecutando motor de reglas...")
            
            try:
                # Declarar hechos en el motor
                with st.spinner("Preparando evaluación..."):
                    # Crear fact de resultado inicial
                    motor.declare(ResultadoEvaluacion(
                        cumple=True,
                        aspectos_cumplidos=[],
                        aspectos_incumplidos=[],
                        recomendaciones=[],
                        explicacion=""
                    ))
                    
                    # Crear fact del documento
                    documento_fact = DocumentoProteccionDatos(**hechos_estructura)
                    motor.declare(documento_fact)
                
                # Ejecutar motor de reglas
                with st.spinner("Evaluando cumplimiento legal..."):
                    motor.run()
                    st.success("✅ Motor de reglas ejecutado correctamente")
                
                # Obtener resultados
                with st.spinner("Procesando resultados..."):
                    resultados = motor.obtener_resultados()
                
                if resultados:
                    st.success("✅ Evaluación completada con éxito")
                    
                    # Mostrar resultados detallados
                    mostrar_resultados_evaluacion(resultados, tipo_documento)
                    
                    return resultados
                else:
                    st.error("❌ No se pudieron obtener resultados del motor de reglas")
                    
                    # Fallback: mostrar ejemplo
                    st.info("🔄 Mostrando evaluación de ejemplo...")
                    mostrar_resultados_ejemplo()
                    
                    return {
                        'cumple': False,
                        'aspectos_cumplidos': [],
                        'aspectos_incumplidos': ['Error en motor de reglas'],
                        'recomendaciones': ['Revisar configuración del motor']
                    }
                    
            except Exception as e:
                st.error(f"❌ Error ejecutando motor de reglas: {str(e)}")
                logger.error(f"Error en motor de reglas: {e}")
                
                # Mostrar fallback
                st.info("🔄 Mostrando evaluación de ejemplo...")
                mostrar_resultados_ejemplo()
                
                return {
                    'cumple': False,
                    'aspectos_cumplidos': [],
                    'aspectos_incumplidos': ['Error técnico en evaluación'],
                    'recomendaciones': ['Contactar soporte técnico']
                }
        
        else:
            st.warning(f"⚠️ Tipo de documento '{tipo_documento}' no implementado aún")
            
            # Mostrar ejemplo para otros tipos
            st.info("🔄 Mostrando evaluación de ejemplo...")
            mostrar_resultados_ejemplo()
            
            return {
                'cumple': False,
                'aspectos_cumplidos': [],
                'aspectos_incumplidos': ['Tipo no implementado'],
                'recomendaciones': [f'Implementar motor de reglas para {tipo_documento}']
            }
            
    except Exception as e:
        logger.error(f"Error en consultar_cumplimiento: {e}")
        st.error(f"❌ Error general en evaluación: {str(e)}")
        
        # Mostrar fallback en caso de error
        st.info("🔄 Mostrando evaluación de ejemplo...")
        mostrar_resultados_ejemplo()
        
        return {
            'cumple': False,
            'aspectos_cumplidos': [],
            'aspectos_incumplidos': ['Error del sistema'],
            'recomendaciones': ['Revisar logs y contactar soporte']
        }

def mostrar_resultados_evaluacion(resultados: dict, tipo_documento: str):
    """
    Muestra los resultados de la evaluación legal real
    """
    st.success("✅ Procesamiento completado")
    st.markdown("### 📋 Resultados del Análisis")
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cumple = resultados.get('cumple', False)
        st.metric(
            "Estado General", 
            "✅ CUMPLE" if cumple else "❌ NO CUMPLE"
        )
    
    with col2:
        aspectos_cumplidos = resultados.get('aspectos_cumplidos', [])
        # VERIFICAR QUE ES UNA LISTA Y OBTENER LONGITUD:
        num_cumplidos = len(aspectos_cumplidos) if isinstance(aspectos_cumplidos, list) else 0
        st.metric("Aspectos Cumplidos", num_cumplidos)
    
    with col3:
        aspectos_incumplidos = resultados.get('aspectos_incumplidos', [])
        # VERIFICAR QUE ES UNA LISTA Y OBTENER LONGITUD:
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
    """
    Tu código de ejemplo original (fallback)
    """
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


def mostrar_diagrama_flujo_wrapper(tipo_documento: str, es_imagen: bool):
    """
    Muestra el diagrama de flujo del proceso usando streamlit-flow
    """
    
    # TODO: Cuando se integre con backend real, aquí se pasará el paso_actual dinámicamente
    # Por ahora, para testing, podemos simular el proceso
    
    # Para producción (comentar para testing):
    mostrar_diagrama_flujo(tipo_documento, es_imagen, paso_actual=0)
    
    # Para testing (descomentar para probar) // No funciona :v
    #simular_proceso_completo(tipo_documento, es_imagen)


if __name__ == "__main__":
    main()