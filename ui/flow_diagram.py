# Lógica del diagrama de flujo
import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout
import time

def crear_nodos_flujo(tipo_documento: str, es_imagen: bool, paso_actual: int = 0):
    """
    Crea los nodos del diagrama de flujo según el tipo de documento
    
    Args:
        tipo_documento: Tipo de documento seleccionado
        es_imagen: Si el archivo es una imagen (requiere OCR)
        paso_actual: Paso actual en ejecución (0-indexed)
    
    Returns:
        Tupla de (nodos, edges, layout)
    """
    nodos = []
    edges = []
    node_id = 0
    
    # Paso 1: OCR (solo si es imagen)
    if es_imagen:
        color = obtener_color_nodo(0, paso_actual)
        nodos.append(StreamlitFlowNode(
            id=str(node_id),
            pos=(0, 0),
            data={'label': '📄 Conversión OCR'},
            node_type='default',
            source_position='right',
            target_position='left',
            style={'background': color, 'border': f'2px solid {color}'}
        ))
        node_id += 1
    
    # Paso 2: Detección de tipo (solo si es "Desconozco")
    offset_deteccion = 1 if es_imagen else 0
    if tipo_documento == "Desconozco":
        color = obtener_color_nodo(offset_deteccion, paso_actual)
        nodos.append(StreamlitFlowNode(
            id=str(node_id),
            pos=(0, 0),
            data={'label': '🔍 Detección de Tipo'},
            node_type='default',
            source_position='right',
            target_position='left',
            style={'background': color, 'border': f'2px solid {color}'}
        ))
        if node_id > 0:
            edges.append(StreamlitFlowEdge(
                id=f"edge_{node_id-1}_{node_id}",
                source=str(node_id - 1),
                target=str(node_id),
                animated=True
            ))
        node_id += 1
    
    # Paso 3: Conversión a Formato Experta
    offset_conversion = offset_deteccion + (1 if tipo_documento == "Desconozco" else 0)
    color = obtener_color_nodo(offset_conversion, paso_actual)
    nodos.append(StreamlitFlowNode(
        id=str(node_id),
        pos=(0, 0),
        data={'label': '🔄 Conversión Experta'},
        node_type='default',
        source_position='right',
        target_position='left',
        style={'background': color, 'border': f'2px solid {color}'}
    ))
    if node_id > 0:
        edges.append(StreamlitFlowEdge(
            id=f"edge_{node_id-1}_{node_id}",
            source=str(node_id - 1),
            target=str(node_id),
            animated=True
        ))
    node_id += 1
    
    # Paso 4: Evaluación de Reglas (puede ser múltiple)
    offset_reglas = offset_conversion + 1
    reglas_ids = []
    
    # Simulación de 3 reglas para el tipo de documento
    for i in range(3):
        color = obtener_color_nodo(offset_reglas, paso_actual)
        regla_id = str(node_id)
        reglas_ids.append(regla_id)
        
        nodos.append(StreamlitFlowNode(
            id=regla_id,
            pos=(0, 0),
            data={'label': f'⚖️ Regla {i+1}'},
            node_type='default',
            source_position='right',
            target_position='left',
            style={'background': color, 'border': f'2px solid {color}'}
        ))
        
        # Conectar desde el nodo anterior
        edges.append(StreamlitFlowEdge(
            id=f"edge_{node_id-1}_{regla_id}",
            source=str(node_id - 1),
            target=regla_id,
            animated=True
        ))
        node_id += 1
    
    # Paso 5: Respuesta
    offset_respuesta = offset_reglas + 1
    color = obtener_color_nodo(offset_respuesta, paso_actual)
    respuesta_id = str(node_id)
    nodos.append(StreamlitFlowNode(
        id=respuesta_id,
        pos=(0, 0),
        data={'label': '✅ Respuesta'},
        node_type='output',
        target_position='left',
        style={'background': color, 'border': f'2px solid {color}'}
    ))
    
    # Conectar todas las reglas a la respuesta
    for i, regla_id in enumerate(reglas_ids):
        edges.append(StreamlitFlowEdge(
            id=f"edge_{regla_id}_{respuesta_id}",
            source=regla_id,
            target=respuesta_id,
            animated=True
        ))
    
    return nodos, edges


def obtener_color_nodo(indice_nodo: int, paso_actual: int) -> str:
    """
    Determina el color del nodo según su estado
    
    - Verde oscuro (#10b981): nodo en ejecución actual
    - Verde claro (#d1fae5): nodo completado
    - Gris claro (#e5e7eb): nodo pendiente
    """
    if indice_nodo < paso_actual:
        return '#d1fae5'  # Verde claro - completado
    elif indice_nodo == paso_actual:
        return '#10b981'  # Verde oscuro - en ejecución
    else:
        return '#e5e7eb'  # Gris - pendiente


def mostrar_diagrama_flujo(tipo_documento: str, es_imagen: bool, paso_actual: int = 0):
    """
    Renderiza el diagrama de flujo usando streamlit-flow
    
    Args:
        tipo_documento: Tipo de documento seleccionado
        es_imagen: Si el archivo es una imagen
        paso_actual: Paso actual en ejecución (default: 0)
    """
    st.markdown("### 🔄 Diagrama de Flujo del Proceso")
    
    nodos, edges = crear_nodos_flujo(tipo_documento, es_imagen, paso_actual)
    
    # Crear el estado del flujo
    state = StreamlitFlowState(nodos, edges)
    
    # Renderizar el flujo
    streamlit_flow(
        'legal_flow',
        state,
        layout=TreeLayout(direction='right'),
        fit_view=True,
        height=400,
        enable_node_menu=False,
        enable_edge_menu=False,
        enable_pane_menu=False,
        get_node_on_click=False,
        get_edge_on_click=False,
        allow_new_edges=False,
        animate_new_edges=True,
    )


def simular_proceso_completo(tipo_documento: str, es_imagen: bool):
    """
    Simula el proceso completo paso a paso para testing
    Útil para verificar visualmente el cambio de colores
    """
    st.markdown("### 🧪 Simulación de Proceso (Testing)")
    
    # Calcular número total de pasos
    num_pasos = 3  # Base: Conversión Experta, Reglas, Respuesta
    if es_imagen:
        num_pasos += 1
    if tipo_documento == "Desconozco":
        num_pasos += 1
    
    # Control de simulación
    if 'paso_simulacion' not in st.session_state:
        st.session_state.paso_simulacion = 0
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⏮️ Reiniciar", use_container_width=True):
            st.session_state.paso_simulacion = 0
            st.rerun()
    
    with col2:
        if st.button("▶️ Siguiente Paso", use_container_width=True):
            if st.session_state.paso_simulacion < num_pasos:
                st.session_state.paso_simulacion += 1
                st.rerun()
    
    with col3:
        if st.button("⏭️ Completar Todo", use_container_width=True):
            st.session_state.paso_simulacion = num_pasos
            st.rerun()
    
    # Mostrar paso actual
    st.info(f"📍 Paso actual: {st.session_state.paso_simulacion} de {num_pasos}")
    
    # Renderizar diagrama con el paso actual
    mostrar_diagrama_flujo(tipo_documento, es_imagen, st.session_state.paso_simulacion)
    
    # Mensaje de estado
    if st.session_state.paso_simulacion >= num_pasos:
        st.success("✅ Proceso completado")
    elif st.session_state.paso_simulacion > 0:
        st.warning(f"⏳ En progreso... ({st.session_state.paso_simulacion}/{num_pasos} completados)")


# Para testing independiente del módulo
if __name__ == "__main__":
    st.set_page_config(page_title="Test - Diagrama de Flujo", layout="wide")
    st.title("🧪 Testing: Diagrama de Flujo")
    
    # Controles de testing
    col1, col2 = st.columns(2)
    
    with col1:
        tipo_test = st.selectbox(
            "Tipo de Documento",
            ["Protección de Datos Personales", "Desconozco"]
        )
    
    with col2:
        es_imagen_test = st.checkbox("¿Es imagen? (requiere OCR)")
    
    st.markdown("---")
    
    simular_proceso_completo(tipo_test, es_imagen_test)