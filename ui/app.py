# Aplicación principal de Streamlit
import streamlit as st
from typing import Optional
from flow_diagram import mostrar_diagrama_flujo
from tests_page import pagina_pruebas

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


def consultar_cumplimiento(tipo_documento: str, texto: Optional[str], archivo):
    """
    Procesa la consulta de cumplimiento legal
    """
    st.markdown("### 📊 Procesamiento en curso...")
    
    # Aquí se conectará con el backend
    # Por ahora, placeholder para desarrollo
    
    with st.spinner("Procesando..."):
        import time
        # Simulación temporal de procesamiento
        time.sleep(1)  # Simula tiempo de procesamiento
        
        # TODO: Integrar con los métodos del backend
        # - Si es archivo de imagen: llamar a ocr.solicitarOCR()
        # - Si tipo_documento == "Desconozco": llamar a gemini.consultarTipoDocumento()
        # - Llamar a gemini.convertirAFormatoExperta()
        # - Ejecutar motor de reglas Experta
        
        pass
        
    st.success("✅ Procesamiento completado")
    
    # Mostrar resultados de ejemplo (placeholder)
    st.markdown("### 📋 Resultados del Análisis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cumplimiento General", "85%", "+5%")
    with col2:
        st.metric("Reglas Evaluadas", "3", "")
    
    st.markdown("#### Detalle de Cumplimiento:")
    
    # Ejemplo de resultados
    st.success("✅ **Regla 1**: Cumple con los requisitos de consentimiento informado")
    st.warning("⚠️ **Regla 2**: Falta incluir cláusula de tratamiento de datos")
    st.success("✅ **Regla 3**: Cumple con registro de banco de datos")
    
    st.info("💡 **Recomendación**: Agregar cláusula específica sobre tratamiento y conservación de datos personales.")
        
    # Mostrar diagrama de flujo
    mostrar_diagrama_flujo_wrapper(tipo_documento, archivo is not None and str(archivo.type).startswith('image'))


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