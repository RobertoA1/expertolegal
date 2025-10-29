"""
Módulo de ejecución de pruebas para el Sistema de Cumplimiento Legal
Permite ejecutar tests de pytest desde la interfaz de Streamlit
"""

import streamlit as st
import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime


def ejecutar_pytest(test_file: str = None, verbose: bool = True):
    """
    Ejecuta pytest y captura los resultados
    
    Args:
        test_file: Archivo específico de test a ejecutar (None para todos)
        verbose: Si se debe mostrar salida detallada
    
    Returns:
        Tupla de (exit_code, stdout, stderr)
    """
    cmd = [sys.executable, "-m", "pytest"]
    
    if test_file:
        cmd.append(test_file)
    else:
        cmd.append("tests/")
    
    if verbose:
        cmd.append("-v")
    
    # Añadir opciones para mejor formato
    cmd.extend([
        "--tb=short",  # Traceback corto
        "-s",  # Mostrar prints
        "--color=yes"  # Color en output
    ])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def parsear_resultados_pytest(output: str):
    """
    Parsea la salida de pytest para extraer información de tests
    
    Returns:
        Dict con información de los tests
    """
    lineas = output.split('\n')
    resultados = {
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'total': 0,
        'tests': []
    }
    
    for linea in lineas:
        if 'passed' in linea.lower():
            # Buscar patrón como "3 passed in 0.50s"
            partes = linea.split()
            for i, parte in enumerate(partes):
                if 'passed' in parte.lower() and i > 0:
                    try:
                        resultados['passed'] = int(partes[i-1])
                    except:
                        pass
        
        if 'failed' in linea.lower():
            partes = linea.split()
            for i, parte in enumerate(partes):
                if 'failed' in parte.lower() and i > 0:
                    try:
                        resultados['failed'] = int(partes[i-1])
                    except:
                        pass
        
        # Detectar tests individuales (líneas que empiezan con "tests/")
        if linea.strip().startswith('tests/'):
            resultados['tests'].append(linea.strip())
    
    resultados['total'] = resultados['passed'] + resultados['failed']
    
    return resultados


def mostrar_estado_test(nombre: str, estado: str, descripcion: str = ""):
    """
    Muestra el estado de un test con iconos y colores
    
    Args:
        nombre: Nombre del test
        estado: 'passed', 'failed', 'running', 'pending'
        descripcion: Descripción adicional del test
    """
    iconos = {
        'passed': '✅',
        'failed': '❌',
        'running': '⏳',
        'pending': '⏸️'
    }
    
    colores = {
        'passed': 'success',
        'failed': 'error',
        'running': 'info',
        'pending': 'warning'
    }
    
    icono = iconos.get(estado, '❓')
    color = colores.get(estado, 'info')
    
    if color == 'success':
        st.success(f"{icono} **{nombre}**\n\n{descripcion}")
    elif color == 'error':
        st.error(f"{icono} **{nombre}**\n\n{descripcion}")
    elif color == 'info':
        st.info(f"{icono} **{nombre}**\n\n{descripcion}")
    else:
        st.warning(f"{icono} **{nombre}**\n\n{descripcion}")


def pagina_pruebas():
    """
    Página principal de ejecución de pruebas
    """
    st.title("🧪 Ejecución de Pruebas")
    st.markdown("---")
    
    st.markdown("""
    Esta página permite ejecutar las pruebas automáticas del sistema experto.
    Las pruebas validan que las reglas de Experta funcionen correctamente.
    """)
    
    # Información sobre los tests requeridos
    with st.expander("ℹ️ Información sobre las Pruebas Requeridas"):
        st.markdown("""
        ### Tests Implementados
        
        1. **Test de Inferencia Correcta**: Verifica que las reglas se disparen correctamente con datos válidos
        2. **Test de Caso Borde**: Prueba situaciones límite o casos especiales
        3. **Test de Explicación**: Valida que el sistema pueda explicar por qué tomó una decisión
        
        ### ¿Cómo funcionan?
        
        Los tests utilizan `pytest` para validar automáticamente el comportamiento del motor de reglas.
        Cada test alimenta el sistema con datos predefinidos y verifica que la respuesta sea la esperada.
        """)
    
    st.markdown("---")
    
    # Estado de los tests
    st.subheader("📋 Estado de las Pruebas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tests Pasados", 
                 st.session_state.get('tests_passed', 0),
                 delta=None)
    
    with col2:
        st.metric("Tests Fallidos", 
                 st.session_state.get('tests_failed', 0),
                 delta=None)
    
    with col3:
        st.metric("Total Tests", 
                 st.session_state.get('tests_total', 0),
                 delta=None)
    
    st.markdown("---")
    
    # Opciones de ejecución
    st.subheader("⚙️ Opciones de Ejecución")
    
    col1, col2 = st.columns(2)
    
    with col1:
        modo_ejecucion = st.radio(
            "Modo de ejecución:",
            ["Todos los tests", "Test individual"],
            horizontal=True
        )
    
    with col2:
        verbose = st.checkbox("Mostrar salida detallada", value=True)
    
    # Selector de test individual si corresponde
    test_seleccionado = None
    if modo_ejecucion == "Test individual":
        test_seleccionado = st.selectbox(
            "Seleccione el test a ejecutar:",
            [
                "test_inferencia_correcta",
                "test_caso_borde",
                "test_explicacion"
            ]
        )
    
    st.markdown("---")
    
    # Botones de acción
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        ejecutar = st.button("▶️ Ejecutar Pruebas", type="primary", use_container_width=True)
    
    with col2:
        limpiar = st.button("🗑️ Limpiar Resultados", use_container_width=True)
    
    if limpiar:
        st.session_state.pop('test_output', None)
        st.session_state.pop('tests_passed', None)
        st.session_state.pop('tests_failed', None)
        st.session_state.pop('tests_total', None)
        st.rerun()
    
    # Ejecutar tests
    if ejecutar:
        st.markdown("---")
        st.subheader("🔄 Ejecutando Pruebas...")
        
        # Determinar qué test ejecutar
        test_file = None
        if modo_ejecucion == "Test individual" and test_seleccionado:
            test_file = f"tests/test_{test_seleccionado}.py"
        
        with st.spinner("Ejecutando pytest..."):
            exit_code, stdout, stderr = ejecutar_pytest(test_file, verbose)
        
        # Guardar output en session state
        st.session_state['test_output'] = stdout
        st.session_state['test_stderr'] = stderr
        st.session_state['test_exit_code'] = exit_code
        
        # Parsear resultados
        resultados = parsear_resultados_pytest(stdout)
        st.session_state['tests_passed'] = resultados['passed']
        st.session_state['tests_failed'] = resultados['failed']
        st.session_state['tests_total'] = resultados['total']
        
        st.rerun()
    
    # Mostrar resultados si existen
    if 'test_output' in st.session_state:
        st.markdown("---")
        st.subheader("📊 Resultados de las Pruebas")
        
        exit_code = st.session_state.get('test_exit_code', -1)
        
        if exit_code == 0:
            st.success("✅ ¡Todas las pruebas pasaron exitosamente!")
        else:
            st.error("❌ Algunas pruebas fallaron. Revisa los detalles abajo.")
        
        # Detalles de tests individuales
        st.markdown("### 📝 Detalle de Tests")
        
        # Estos son placeholders - se actualizarán con resultados reales
        tests_info = [
            {
                'nombre': 'Test de Inferencia Correcta',
                'descripcion': 'Verifica que las reglas se disparen correctamente',
                'archivo': 'test_inferencia_correcta.py'
            },
            {
                'nombre': 'Test de Caso Borde',
                'descripcion': 'Prueba situaciones límite del sistema',
                'archivo': 'test_caso_borde.py'
            },
            {
                'nombre': 'Test de Explicación',
                'descripcion': 'Valida que el sistema explique sus decisiones',
                'archivo': 'test_explicacion.py'
            }
        ]
        
        for test_info in tests_info:
            # Determinar estado basado en la salida
            estado = 'passed' if exit_code == 0 else 'pending'
            output = st.session_state.get('test_output', '')
            
            if test_info['archivo'] in output:
                if 'PASSED' in output or 'passed' in output:
                    estado = 'passed'
                elif 'FAILED' in output or 'failed' in output:
                    estado = 'failed'
            
            mostrar_estado_test(
                test_info['nombre'],
                estado,
                test_info['descripcion']
            )
        
        # Output completo en expander
        with st.expander("🔍 Ver Output Completo de pytest"):
            st.code(st.session_state.get('test_output', ''), language='bash')
            
            if st.session_state.get('test_stderr'):
                st.markdown("**Errores:**")
                st.code(st.session_state.get('test_stderr', ''), language='bash')
    
    st.markdown("---")
    
    # Información adicional
    st.info("💡 **Nota**: Los tests deben estar implementados en la carpeta `tests/` del proyecto.")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Pruebas - Sistema Legal",
        page_icon="🧪",
        layout="wide"
    )
    pagina_pruebas()