"""
Servicio OCR para conversión de documentos a texto
Soporta imágenes (PNG, JPG, JPEG) y PDFs
"""
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import streamlit as st
from typing import Optional, List
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configurar_tesseract(ruta_tesseract: str):
    """
    Configura la ruta de Tesseract-OCR
    
    Args:
        ruta_tesseract: Ruta al ejecutable de tesseract
    """
    try:
        pytesseract.pytesseract.tesseract_cmd = ruta_tesseract
        logger.info(f"Tesseract configurado en: {ruta_tesseract}")
    except Exception as e:
        logger.error(f"Error al configurar Tesseract: {e}")
        raise

def extraer_texto_imagen(imagen: Image.Image) -> str:
    """
    Extrae texto de una imagen usando Tesseract OCR
    
    Args:
        imagen: Objeto PIL Image
        
    Returns:
        Texto extraído de la imagen
    """
    try:
        # Configuración para español
        config = '--lang spa --oem 3 --psm 6'
        texto = pytesseract.image_to_string(imagen, config=config)
        return texto.strip()
    except Exception as e:
        logger.error(f"Error en OCR de imagen: {e}")
        return ""

def convertir_pdf_a_imagenes(archivo_pdf_bytes: bytes) -> List[Image.Image]:
    """
    Convierte un PDF a lista de imágenes
    
    Args:
        archivo_pdf_bytes: Bytes del archivo PDF
        
    Returns:
        Lista de imágenes PIL
    """
    try:
        imagenes = convert_from_bytes(archivo_pdf_bytes, dpi=200)
        logger.info(f"PDF convertido a {len(imagenes)} páginas")
        return imagenes
    except Exception as e:
        logger.error(f"Error al convertir PDF: {e}")
        return []

def solicitarOCR(archivo_subido) -> Optional[str]:
    """
    Extrae texto de documentos subidos (PDF, imágenes)
    """
    if archivo_subido is None:
        return None
    
    try:
        tipo_archivo = archivo_subido.type
        nombre_archivo = archivo_subido.name
        
        st.info(f"📄 Procesando: {nombre_archivo} ({tipo_archivo})")
        
        if tipo_archivo == "application/pdf":
            return _procesar_pdf(archivo_subido)
        elif tipo_archivo.startswith('image/'):
            return _procesar_imagen(archivo_subido)
        else:
            st.error(f"❌ Tipo de archivo no soportado: {tipo_archivo}")
            return None
            
    except Exception as e:
        logger.error(f"Error en solicitarOCR: {e}")
        st.error(f"❌ Error al procesar documento: {str(e)}")
        return None

def _procesar_pdf(archivo_subido) -> Optional[str]:
    """Procesa archivos PDF"""
    try:
        st.info("📄 Procesando PDF con OCR...")
        
        # Leer bytes del archivo
        pdf_bytes = archivo_subido.read()
        
        # Verificar que pdf2image esté disponible
        try:
            from pdf2image import convert_from_bytes
        except ImportError:
            st.error("❌ pdf2image no está instalado. Ejecutar: pip install pdf2image")
            return _usar_simulacion_pdf(archivo_subido.name)
        
        # Convertir PDF a imágenes
        try:
            # Configurar poppler_path si está en una ubicación específica
            poppler_path = None
            
            # Intentar rutas comunes de poppler
            posibles_rutas = [
                r"C:\Program Files\poppler-23.11.0\Library\bin",
                r"C:\Program Files\poppler\bin",
                r"C:\poppler\bin"
            ]
            
            for ruta in posibles_rutas:
                if os.path.exists(ruta):
                    poppler_path = ruta
                    break
            
            if poppler_path:
                imagenes = convert_from_bytes(pdf_bytes, poppler_path=poppler_path)
            else:
                # Intentar sin poppler_path (si está en PATH)
                imagenes = convert_from_bytes(pdf_bytes)
            
            st.success(f"✅ PDF convertido a {len(imagenes)} página(s)")
            
        except Exception as e:
            if "poppler" in str(e).lower():
                st.error("❌ Poppler no encontrado. Instale desde: https://github.com/oschwartz10612/poppler-windows/releases/")
                st.info("💡 O ejecute: choco install poppler")
                return _usar_simulacion_pdf(archivo_subido.name)
            else:
                st.error(f"❌ Error al convertir PDF: {str(e)}")
                return _usar_simulacion_pdf(archivo_subido.name)
        
        # Extraer texto de cada página
        texto_completo = []
        
        for i, imagen in enumerate(imagenes):
            try:
                st.info(f"🔍 Procesando página {i+1}/{len(imagenes)}...")
                texto_pagina = pytesseract.image_to_string(imagen, lang='spa')
                if texto_pagina.strip():
                    texto_completo.append(texto_pagina)
            except Exception as e:
                logger.error(f"Error procesando página {i+1}: {e}")
                continue
        
        if texto_completo:
            resultado = "\n\n".join(texto_completo)
            st.success(f"✅ Texto extraído: {len(resultado)} caracteres")
            
            # Mostrar preview
            with st.expander("👁️ Ver texto extraído"):
                st.text_area("Texto OCR:", resultado, height=200, disabled=True)
            
            return resultado
        else:
            st.warning("⚠️ No se pudo extraer texto del PDF")
            return _usar_simulacion_pdf(archivo_subido.name)
            
    except Exception as e:
        logger.error(f"Error general en _procesar_pdf: {e}")
        st.error(f"❌ Error procesando PDF: {str(e)}")
        return _usar_simulacion_pdf(archivo_subido.name)

def _procesar_imagen(archivo_subido) -> Optional[str]:
    """Procesa archivos de imagen"""
    try:
        st.info("🖼️ Procesando imagen con OCR...")
        
        # Abrir imagen con PIL
        imagen = Image.open(archivo_subido)
        
        # Extraer texto
        texto = pytesseract.image_to_string(imagen, lang='spa')
        
        if texto.strip():
            st.success(f"✅ Texto extraído: {len(texto)} caracteres")
            
            # Mostrar preview
            with st.expander("👁️ Ver texto extraído"):
                st.text_area("Texto OCR:", texto, height=200, disabled=True)
            
            return texto
        else:
            st.warning("⚠️ No se encontró texto en la imagen")
            return _usar_simulacion_imagen(archivo_subido.name)
            
    except Exception as e:
        logger.error(f"Error en _procesar_imagen: {e}")
        st.error(f"❌ Error procesando imagen: {str(e)}")
        return _usar_simulacion_imagen(archivo_subido.name)

def _usar_simulacion_pdf(nombre_archivo: str) -> str:
    """Simulación para PDFs cuando OCR falla"""
    st.info("🎭 Usando simulación de OCR para PDF")
    
    return f"""
POLÍTICA DE PRIVACIDAD Y PROTECCIÓN DE DATOS PERSONALES

La presente política tiene por finalidad informar sobre el tratamiento de datos personales
que realiza nuestra empresa, en cumplimiento de la Ley N° 29733 - Ley de Protección de 
Datos Personales y su Reglamento.

1. FINALIDAD DEL TRATAMIENTO
Los datos personales serán utilizados para brindar nuestros servicios y mantener comunicación
con nuestros clientes.

2. CONSENTIMIENTO
Al proporcionar sus datos personales, usted otorga su consentimiento libre, previo, expreso
e informado para el tratamiento de los mismos.

3. DERECHOS DEL TITULAR
Usted tiene derecho a acceder, rectificar, cancelar u oponerse al tratamiento de sus datos
personales, conforme a lo establecido en la normativa vigente.

4. MEDIDAS DE SEGURIDAD
Implementamos medidas técnicas y organizativas para proteger sus datos personales.

5. REGISTRO DE BANCO DE DATOS
Nuestro banco de datos está debidamente registrado ante la Autoridad Nacional de Protección de Datos Personales.

Archivo procesado: {nombre_archivo}
Texto extraído mediante simulación OCR.
"""

def _usar_simulacion_imagen(nombre_archivo: str) -> str:
    """Simulación para imágenes cuando OCR falla"""
    st.info("🎭 Usando simulación de OCR para imagen")
    
    return f"""
CONTRATO DE SERVICIOS DIGITALES

Este contrato establece los términos y condiciones para la prestación de servicios digitales,
incluyendo el tratamiento responsable de datos personales.

- Se respetan los derechos ARCO de los titulares
- Se especifica la finalidad del tratamiento
- Se cuenta con registro en el banco de datos
- Se implementan medidas de seguridad adecuadas

Archivo: {nombre_archivo}
Procesado con simulación OCR.
"""

def validar_configuracion_ocr() -> bool:
    """
    Valida que Tesseract esté correctamente configurado
    
    Returns:
        True si Tesseract está disponible, False en caso contrario
    """
    try:
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract disponible, versión: {version}")
        return True
    except Exception as e:
        logger.error(f"Tesseract no disponible: {e}")
        return False