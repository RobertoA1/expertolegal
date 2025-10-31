"""
Servicio de integración con Google Gemini para análisis de documentos legales
Actualizado al SDK oficial 'google-genai'
"""

import streamlit as st
import json
import logging
from typing import Optional, Dict, Any
from google import genai
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tipos de documentos disponibles
TIPOS_DOCUMENTO = [
    "Protección de Datos Personales",
    "Prevención de Lavado de Activos", 
    "Seguridad y Salud en el Trabajo",
    "Ley de Responsabilidad Administrativa de Personas Jurídicas",
    "Protección al Consumidor",
    "Normas Laborales",
    "Normativa Societaria", 
    "Normativa Tributaria",
    "Normativa Ambiental"
]

def configurar_gemini(api_key: Optional[str] = None) -> Optional[genai.Client]:
    """
    Configura el cliente de Google Gemini
    """
    try:
        if api_key is None:
            # 🔐 HARDCODEA TU API KEY AQUÍ:
            api_key = "AIzaSyC0qkUMjdwURQoDPF4J0z131BgwiogV_pc"

        if not api_key:
            st.error("❌ No se encontró la API Key de Gemini.")
            return None

        client = genai.Client(api_key=api_key)
        logger.info("✅ Gemini configurado correctamente")
        return client

    except Exception as e:
        logger.error(f"Error al configurar Gemini: {e}")
        st.error(f"❌ Error al configurar Gemini: {str(e)}")
        return None


def consultarTipoDocumento(texto_documento: str) -> Optional[str]:
    """
    Utiliza Gemini para identificar el tipo de documento legal
    """
    try:
        client = configurar_gemini()
        if client is None:
            return None

        prompt = f"""
        Analiza el siguiente texto de documento legal peruano e identifica de qué tipo de normativa se trata.

        Tipos disponibles:
        1. Protección de Datos Personales
        2. Prevención de Lavado de Activos
        3. Seguridad y Salud en el Trabajo
        4. Ley de Responsabilidad Administrativa de Personas Jurídicas
        5. Protección al Consumidor
        6. Normas Laborales
        7. Normativa Societaria
        8. Normativa Tributaria
        9. Normativa Ambiental

        IMPORTANTE: 
        - Responde ÚNICAMENTE con el nombre exacto de una de estas categorías.
        - Si no puedes identificar claramente el tipo, responde "No identificado".
        - Basa tu análisis en palabras clave, referencias legales y contexto del documento.

        Texto a analizar:
        {texto_documento[:3000]}...

        Tipo de documento:
        """

        st.info("🤖 Analizando tipo de documento con Gemini...")
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[prompt]
        )

        if not response.text:
            st.warning("⚠️ Gemini no pudo generar una respuesta")
            return None

        tipo_identificado = response.text.strip()

        if tipo_identificado in TIPOS_DOCUMENTO:
            st.success(f"✅ Tipo de documento identificado: **{tipo_identificado}**")
            return tipo_identificado
        else:
            st.warning(f"⚠️ Tipo no reconocido: {tipo_identificado}")
            return None

    except Exception as e:
        logger.error(f"Error en consultarTipoDocumento: {e}")
        st.error(f"❌ Error al consultar tipo de documento: {str(e)}")
        return None


def convertirAFormatoExperta(texto_documento: str, tipo_documento: str) -> Optional[Dict[str, Any]]:
    """
    Convierte el documento a formato compatible con Experta (hechos)
    """
    try:
        client = configurar_gemini()
        if client is None:
            return None

        prompt_especifico = obtener_prompt_conversion(tipo_documento, texto_documento)

        if not prompt_especifico:
            st.error(f"❌ No hay prompt definido para: {tipo_documento}")
            return None

        st.info("🔄 Convirtiendo documento a formato Experta...")
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[prompt_especifico]
        )

        if not response.text:
            st.warning("⚠️ Gemini no pudo generar la conversión")
            return None

        try:
            # 🔧 LIMPIEZA MEJORADA: Eliminar bloques de markdown
            respuesta_limpia = response.text.strip()
            
            # Eliminar ```json al inicio y ``` al final
            if respuesta_limpia.startswith("```json"):
                respuesta_limpia = respuesta_limpia[7:]  # Quitar ```json
            elif respuesta_limpia.startswith("```"):
                respuesta_limpia = respuesta_limpia[3:]  # Quitar ```
            
            if respuesta_limpia.endswith("```"):
                respuesta_limpia = respuesta_limpia[:-3]  # Quitar ``` del final
            
            # Limpiar espacios adicionales
            respuesta_limpia = respuesta_limpia.strip()
            
            # 🔧 Intentar parsear JSON
            hechos_extraidos = json.loads(respuesta_limpia)

            if isinstance(hechos_extraidos, dict):
                st.success("✅ Documento convertido a formato Experta")
                with st.expander("👁️ Ver hechos extraídos"):
                    st.json(hechos_extraidos)
                return hechos_extraidos
            else:
                st.error("❌ La respuesta de Gemini no tiene el formato JSON esperado")
                return None

        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {e}")
            st.error("❌ La respuesta de Gemini no es un JSON válido")
            
            # Mostrar más información de depuración
            with st.expander("🐛 Ver detalles del error"):
                st.text(f"Error: {str(e)}")
                st.text("Respuesta original de Gemini:")
                st.code(response.text, language="text")
                st.text("Respuesta limpiada:")
                st.code(respuesta_limpia, language="text")
            
            return None

    except Exception as e:
        logger.error(f"Error en convertirAFormatoExperta: {e}")
        st.error(f"❌ Error al convertir documento: {str(e)}")
        return None


def obtener_prompt_conversion(tipo_documento: str, texto: str) -> Optional[str]:
    """
    Obtiene el prompt específico para conversión según el tipo de documento
    """
    prompts = {
        "Protección de Datos Personales": f"""
        Analiza este documento de protección de datos personales y extrae información para el motor de reglas Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}

        Estructura JSON requerida:
        {{
            "tiene_politica_privacidad": true/false,
            "tiene_consentimiento_informado": true/false,
            "tiene_registro_banco_datos": true/false,
            "tiene_contrato_encargo": true/false,
            "tiene_clausulas_legales": true/false,
            "menciona_autoridad_proteccion": true/false,
            "especifica_finalidad_datos": true/false,
            "menciona_derechos_arco": true/false,
            "tiene_medidas_seguridad": true/false,
            "menciona_plazo_conservacion": true/false
        }}

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,

        "Prevención de Lavado de Activos": f"""
        Analiza este documento de prevención de lavado de activos y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}

        Estructura JSON requerida:
        {{
            "tiene_politica_pla": true/false,
            "menciona_uif": true/false,
            "tiene_oficial_cumplimiento": true/false,
            "menciona_operaciones_sospechosas": true/false,
            "tiene_capacitacion_empleados": true/false,
            "menciona_sanciones": true/false
        }}

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
        
        # 🆕 Agregar más tipos de documento aquí siguiendo el mismo patrón
        "Seguridad y Salud en el Trabajo": f"""
        Analiza este documento de seguridad y salud en el trabajo y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON

        Estructura JSON requerida:
        {{
            "tiene_reglamento_interno_sst": true/false,
            "tiene_politica_sst": true/false,
            "menciona_registro_accidentes": true/false,
            "menciona_comite_sst": true/false,
            "tiene_matriz_riesgos": true/false,
            "menciona_capacitaciones_sst": true/false,
            "menciona_ley_29783": true/false
        }}

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
    }

    return prompts.get(tipo_documento)


def validar_configuracion_gemini() -> bool:
    """
    Verifica si Gemini está disponible
    """
    try:
        client = configurar_gemini()
        if client is None:
            return False

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=["Responde solo 'OK'"]
        )

        if response.text and 'OK' in response.text:
            logger.info("✅ Gemini disponible y funcionando")
            return True
        else:
            logger.warning("⚠️ Gemini responde pero de forma inesperada")
            return False

    except Exception as e:
        logger.error(f"❌ Gemini no disponible: {e}")
        return False


def configurar_api_key_ui():
    """
    Interfaz Streamlit para configurar la API Key de Gemini
    """
    st.subheader("🔑 Configuración de Gemini")

    if validar_configuracion_gemini():
        st.success("✅ Gemini está configurado y funcionando")
        return True

    st.warning("⚠️ Gemini no está configurado")

    api_key = st.text_input(
        "Ingresa tu API Key de Gemini:",
        type="password",
        help="Puedes obtener una API Key gratuita en https://makersuite.google.com/app/apikey"
    )

    if st.button("💾 Guardar y Validar"):
        client = configurar_gemini(api_key)
        if client:
            st.success("✅ API Key configurada correctamente")
            return True
        else:
            st.error("❌ API Key inválida o problema de conexión")

    return False
