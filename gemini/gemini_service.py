"""
Servicio de integración con Google Gemini para análisis de documentos legales
Actualizado al SDK oficial 'google-genai'
"""

import streamlit as st
import json
import logging
from typing import Optional, Dict, Any
from google import genai

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
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "tiene_manual_prevencion": true/false,
            "tiene_politicas_prevencion": true/false,
            "tiene_identificacion_clientes": true/false,
            "tiene_registro_operaciones": true/false,
            "tiene_reporte_operaciones_sospechosas": true/false,
            "tiene_oficial_cumplimiento": true/false,
            "tiene_capacitaciones": true/false,
            "tiene_evaluacion_riesgos": true/false,
            "tiene_debida_diligencia": true/false,
            "menciona_uif_peru": true/false
        }}

        DEFINICIONES:
        - "tiene_manual_prevencion": Si existe un Manual de Prevención de LA/FT
        - "tiene_politicas_prevencion": Si hay políticas y procedimientos específicos
        - "tiene_identificacion_clientes": Si hay procedimientos KYC (conocimiento del cliente)
        - "tiene_registro_operaciones": Si se registran operaciones según montos
        - "tiene_reporte_operaciones_sospechosas": Si hay procedimiento para reportar a UIF
        - "tiene_oficial_cumplimiento": Si hay persona designada como responsable
        - "tiene_capacitaciones": Si hay programa de capacitación del personal
        - "tiene_evaluacion_riesgos": Si se realiza evaluación de riesgos LA/FT
        - "tiene_debida_diligencia": Si hay procedimientos de debida diligencia
        - "menciona_uif_peru": Si se menciona a la Unidad de Inteligencia Financiera

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,        
        "Seguridad y Salud en el Trabajo": f"""
        Analiza este documento de seguridad y salud en el trabajo y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "tiene_reglamento_interno": true/false,
            "tiene_politica_sst": true/false,
            "tiene_comite_sst": true/false,
            "tiene_supervisor_sst": true/false,
            "tiene_matriz_iper": true/false,
            "tiene_plan_anual": true/false,
            "tiene_registros_obligatorios": true/false,
            "tiene_registro_accidentes": true/false,
            "tiene_capacitaciones": true/false,
            "tiene_examenes_medicos": true/false,
            "tiene_epp": true/false,
            "tiene_procedimientos_trabajo_seguro": true/false,
            "menciona_responsabilidades": true/false,
            "numero_trabajadores": número_entero
        }}

        DEFINICIONES:
        - "tiene_reglamento_interno": Si existe Reglamento Interno de SST (obligatorio con 20+ trabajadores)
        - "tiene_politica_sst": Si hay Política de SST establecida por la alta dirección
        - "tiene_comite_sst": Si existe Comité de SST (obligatorio con 20+ trabajadores)
        - "tiene_supervisor_sst": Si hay Supervisor de SST designado (obligatorio con menos de 20 trabajadores)
        - "tiene_matriz_iper": Si existe Matriz de Identificación de Peligros y Evaluación de Riesgos
        - "tiene_plan_anual": Si hay Plan Anual de SST con objetivos y metas
        - "tiene_registros_obligatorios": Si se mantienen registros del sistema de gestión de SST
        - "tiene_registro_accidentes": Si existe registro específico de accidentes e incidentes
        - "tiene_capacitaciones": Si se realizan capacitaciones en SST (mínimo 4 anuales)
        - "tiene_examenes_medicos": Si se realizan exámenes médicos ocupacionales
        - "tiene_epp": Si se proveen Equipos de Protección Personal
        - "tiene_procedimientos_trabajo_seguro": Si existen procedimientos escritos de trabajo seguro (PETS)
        - "menciona_responsabilidades": Si se definen responsabilidades del empleador y trabajadores
        - "numero_trabajadores": Número aproximado de trabajadores (para determinar obligaciones legales)

        PALABRAS CLAVE A BUSCAR:
        - Reglamento Interno, Política de SST, Comité de SST, Supervisor de SST
        - Matriz IPER, Identificación de Peligros, Evaluación de Riesgos
        - Plan Anual, registros, accidentes, incidentes, enfermedades ocupacionales
        - Capacitación, entrenamiento, formación en SST
        - Exámenes médicos, ocupacionales, pre-ocupacional, periódico
        - EPP, Equipos de Protección Personal, casco, guantes, protección
        - Procedimientos, PETS, trabajo seguro, instrucciones de trabajo
        - Responsabilidades, obligaciones, deberes, empleador, trabajadores

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
        "Ley de Responsabilidad Administrativa de Personas Jurídicas": f"""
        Analiza este documento de responsabilidad administrativa y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "compromiso_organo_gobierno": true/false,
            "tiene_encargado_prevencion": true/false,
            "tiene_mapa_riesgos": true/false,
            "tiene_controles_contables_financieros": true/false,
            "tiene_canal_denuncia_proteccion": true/false,
            "tiene_procedimiento_disciplinario_sancion": true/false,
            "tiene_politicas_riesgos_especificos": true/false
        }}

        DEFINICIONES:
        - "compromiso_organo_gobierno": Si existe compromiso visible de la alta dirección
        - "tiene_encargado_prevencion": Si hay un Compliance Officer designado
        - "tiene_mapa_riesgos": Si existe mapa de riesgos de delitos
        - "tiene_controles_contables_financieros": Si hay controles contables robustos
        - "tiene_canal_denuncia_proteccion": Si hay canal de denuncias con protección
        - "tiene_procedimiento_disciplinario_sancion": Si hay régimen sancionador
        - "tiene_politicas_riesgos_especificos": Si hay políticas para riesgos específicos

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
        "Protección al Consumidor": f"""
        Analiza este documento de protección al consumidor y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "garantiza_idoneidad": true/false,
            "menciona_riesgos_seguridad": true/false,
            "es_publicidad_clara_veraz": true/false,
            "tiene_clausulas_transparentes": true/false,
            "tiene_libro_reclamaciones_fisico_virtual": true/false,
            "cumple_plazo_respuesta_reclamos": true/false,
            "ofrece_posibilidad_pago_anticipado": true/false
        }}

        DEFINICIONES:
        - "garantiza_idoneidad": Si el producto/servicio corresponde a lo ofrecido
        - "menciona_riesgos_seguridad": Si se informa sobre riesgos y medidas de seguridad
        - "es_publicidad_clara_veraz": Si la publicidad es clara, veraz y no induce a error
        - "tiene_clausulas_transparentes": Si las cláusulas son claras y no abusivas
        - "tiene_libro_reclamaciones_fisico_virtual": Si existe libro de reclamaciones físico o virtual
        - "cumple_plazo_respuesta_reclamos": Si se responde a reclamos en máximo 30 días
        - "ofrece_posibilidad_pago_anticipado": Si permite pago anticipado sin penalidades

        PALABRAS CLAVE A BUSCAR:
        - Idoneidad, conforme a oferta, corresponde a descripción
        - Riesgos, seguridad, advertencias, medidas de protección
        - Publicidad veraz, información clara, no engañosa
        - Cláusulas claras, transparentes, no abusivas, legible
        - Libro de reclamaciones, reclamos, quejas, libro virtual
        - Plazo de respuesta, 30 días, días calendario
        - Pago anticipado, adelanto de cuotas, sin penalidad

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
        "Normas Laborales": f"""
        Analiza este documento de normas laborales peruanas y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "tiene_contratos_escritos_vigentes": true/false,
            "tiene_periodo_prueba_informado": true/false,
            "tiene_registro_planilla_electronica": true/false,
            "entrega_boletas_pago_oportunas": true/false,
            "tiene_reglamento_interno_trabajo": true/false,
            "registra_control_asistencia": true/false
        }}

        DEFINICIONES:
        - "tiene_contratos_escritos_vigentes": Si existen contratos de trabajo por escrito y vigentes
        - "tiene_periodo_prueba_informado": Si se informa expresamente sobre el periodo de prueba
        - "tiene_registro_planilla_electronica": Si hay registro en Planilla Electrónica (PLAME/T-Registro)
        - "entrega_boletas_pago_oportunas": Si se entregan boletas de pago de forma oportuna y firmadas
        - "tiene_reglamento_interno_trabajo": Si existe Reglamento Interno de Trabajo (obligatorio con 100+ trabajadores)
        - "registra_control_asistencia": Si existe sistema de control de asistencia y registro de horas extra

        PALABRAS CLAVE A BUSCAR:
        - Contrato de trabajo, contrato escrito, modalidad contractual, plazo fijo, plazo indeterminado
        - Periodo de prueba, prueba laboral, evaluación inicial
        - Planilla electrónica, PLAME, T-Registro, registro de trabajadores
        - Boleta de pago, recibo por honorarios, comprobante de pago, firma del trabajador
        - Reglamento Interno de Trabajo, RIT, normas de conducta, régimen disciplinario
        - Control de asistencia, registro de horario, marcación, horas extra, sobretiempo
        - Jornada laboral, horario de trabajo, descansos, vacaciones

        NORMAS DE REFERENCIA:
        - D.S. N° 003-97-TR (Ley de Productividad y Competitividad Laboral)
        - Ley N° 28806 (Ley General de Inspección del Trabajo)
        - D.S. 004-2006-TR (Reglamento de Jornada y Horario)
        - D.S. 039-91-TR (Reglamento de Reglamento Interno de Trabajo)

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
        "Normativa Societaria": f"""
        Analiza este documento societario peruano y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "esta_constituida_escritura_publica": true/false,
            "esta_inscrita_registros_publicos": true/false,
            "tiene_estatuto_actualizado": true/false,
            "capital_suscrito_totalmente": true/false,
            "capital_pagado_minimo": true/false,
            "mantiene_pluralidad_socios": true/false,
            "tiene_libro_actas_junta_general": true/false,
            "tiene_libro_matricula_acciones": true/false,
            "tiene_libro_actas_directorio": true/false
        }}

        DEFINICIONES:
        - "esta_constituida_escritura_publica": Si la sociedad está constituida mediante Escritura Pública
        - "esta_inscrita_registros_publicos": Si está inscrita en SUNARP (Registros Públicos)
        - "tiene_estatuto_actualizado": Si los estatutos sociales están actualizados
        - "capital_suscrito_totalmente": Si el capital social está totalmente suscrito
        - "capital_pagado_minimo": Si se ha pagado el mínimo del 25% de cada acción suscrita
        - "mantiene_pluralidad_socios": Si mantiene mínimo 2 socios (excepto EIRL)
        - "tiene_libro_actas_junta_general": Si existe Libro de Actas de Junta General
        - "tiene_libro_matricula_acciones": Si existe Libro de Matrícula de Acciones (para S.A./S.A.C.)
        - "tiene_libro_actas_directorio": Si existe Libro de Actas de Directorio (si aplica)

        PALABRAS CLAVE A BUSCAR:
        - Escritura Pública, constitución, notario, protocolo notarial
        - SUNARP, Registros Públicos, inscripción, partida registral
        - Estatutos, modificación estatutaria, reforma de estatutos
        - Capital social, suscripción, acciones, aportes, desembolso
        - Socios, accionistas, pluralidad, junta general, asamblea
        - Libro de actas, libro de matrícula, libro de acciones, libro de directorio
        - Junta General, Directorio, Gerente, órganos sociales

        NORMAS DE REFERENCIA:
        - Ley N° 26887 - Ley General de Sociedades
        - Art. 5 - Constitución por Escritura Pública
        - Art. 9 - Inscripción en Registros Públicos
        - Art. 4 - Pluralidad de socios
        - Art. 52 - Capital social y aportes
        - Art. 114 - Libro de Actas de Junta General
        - Art. 245 - Libro de Matrícula de Acciones

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
        "Normativa Tributaria": f"""
        Analiza este documento tributario peruano y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "tiene_libros_obligatorios_vigentes": true/false,
            "libros_cumplen_plazo_maximo_atraso": true/false,
            "emite_comprobantes_pago_por_ventas": true/false,
            "comprobantes_sustentan_costo_gasto": true/false,
            "presenta_declaracion_jurada_mensual": true/false,
            "presenta_declaracion_jurada_anual": true/false,
            "domicilio_fiscal_comunicado_sunat": true/false
        }}

        DEFINICIONES:
        - "tiene_libros_obligatorios_vigentes": Si existen y se llevan los libros contables obligatorios
        - "libros_cumplen_plazo_maximo_atraso": Si los libros están actualizados dentro del plazo máximo permitido
        - "emite_comprobantes_pago_por_ventas": Si se emiten comprobantes de pago por todas las ventas
        - "comprobantes_sustentan_costo_gasto": Si los costos y gastos se sustentan con comprobantes válidos
        - "presenta_declaracion_jurada_mensual": Si se presentan declaraciones juradas mensuales (IGV/Renta)
        - "presenta_declaracion_jurada_anual": Si se presenta declaración jurada anual de renta
        - "domicilio_fiscal_comunicado_sunat": Si el domicilio fiscal está actualizado y comunicado a SUNAT

        PALABRAS CLAVE A BUSCAR:
        - Libros contables, registro de ventas, registro de compras, libro caja, libro bancos
        - Plazo de atraso, actualización, libros al día, registro oportuno
        - Comprobantes de pago, facturas, boletas, tickets, comprobantes electrónicos
        - Sustento, gastos deducibles, costos, documentos sustentatorios
        - Declaración jurada, PDT, IGV, impuesto a la renta, mensual, anual
        - Domicilio fiscal, SUNAT, actualización de datos, notificaciones
        - RUC, Registro Único de Contribuyentes, obligaciones tributarias

        NORMAS DE REFERENCIA:
        - D.S. N° 133-2013-EF - Texto Único Ordenado del Código Tributario
        - Art. 87 - Obligaciones formales de los deudores tributarios
        - Art. 11 - Domicilio fiscal
        - R.S. 234-2006/SUNAT - Plazos máximos de atraso en libros
        - Ley del Impuesto General a las Ventas (IGV)
        - Ley del Impuesto a la Renta

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """,
        "Normativa Ambiental": f"""
        Analiza este documento ambiental peruano y extrae información para Experta.

        INSTRUCCIONES CRÍTICAS:
        1. Responde ÚNICAMENTE con un objeto JSON válido
        2. NO uses bloques de código markdown (```json)
        3. NO agregues texto adicional antes o después del JSON
        4. El JSON debe empezar con {{ y terminar con }}
        5. Usa EXACTAMENTE estos nombres de campos:

        Estructura JSON requerida:
        {{
            "tiene_estudio_impacto_ambiental": true/false,
            "tiene_monitoreo_ambiental": true/false,
            "cumple_LMP_ECA": true/false,
            "tiene_registro_residuos_solidos": true/false,
            "tiene_autorizacion_vertimientos": true/false,
            "tiene_plan_manejo_ambiental": true/false,
            "tiene_sistema_gestion_ambiental": true/false,
            "tiene_plan_contigencia": true/false
        }}

        DEFINICIONES:
        - "tiene_estudio_impacto_ambiental": Si existe Estudio de Impacto Ambiental (EIA) aprobado
        - "tiene_monitoreo_ambiental": Si realiza monitoreo ambiental periódico y reporta a autoridades
        - "cumple_LMP_ECA": Si cumple con Límites Máximos Permisibles y Estándares de Calidad Ambiental
        - "tiene_registro_residuos_solidos": Si cuenta con registro de generador de residuos sólidos
        - "tiene_autorizacion_vertimientos": Si tiene autorización para vertimientos de aguas residuales
        - "tiene_plan_manejo_ambiental": Si tiene Plan de Manejo Ambiental implementado
        - "tiene_sistema_gestion_ambiental": Si tiene sistema de gestión ambiental (ISO 14001 u otro)
        - "tiene_plan_contigencia": Si tiene plan de contingencias ambientales

        PALABRAS CLAVE A BUSCAR:
        - EIA, Estudio de Impacto Ambiental, certificación ambiental, DIA, EIA-sd, EIA-d
        - Monitoreo ambiental, IMA, informe de monitoreo, mediciones, controles ambientales
        - LMP, Límites Máximos Permisibles, ECA, Estándares de Calidad Ambiental, emisiones, efluentes
        - Residuos sólidos, registro de generador, declaración anual de residuos, plan de manejo
        - Vertimientos, autorización ANA, aguas residuales, descargas
        - Plan de manejo ambiental, PMA, medidas de mitigación
        - Sistema de gestión ambiental, ISO 14001, políticas ambientales
        - Plan de contingencias, emergencias ambientales, respuesta a incidentes

        NORMAS DE REFERENCIA:
        - Ley N° 28611 - Ley General del Ambiente
        - Ley N° 27446 - Ley del Sistema Nacional de Evaluación de Impacto Ambiental
        - D.S. N° 019-2009-MINAM - Reglamento de la Ley del SEIA
        - D.S. N° 004-2017-MINAM - Reglamento de la OEFA
        - D.L. 1278 - Ley de Gestión Integral de Residuos Sólidos
        - Ley N° 29338 - Ley de Recursos Hídricos

        Documento a analizar:
        {texto[:4000]}

        Responde SOLO con el JSON:
        """
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
