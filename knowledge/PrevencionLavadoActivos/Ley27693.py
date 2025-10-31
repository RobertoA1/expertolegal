"""
Reglas de Experta para Ley N° 27693 - Ley de Prevención de Lavado de Activos
(Versión corregida - compatible con Ley 29733)
"""

from experta import *
import logging

logger = logging.getLogger(__name__)

class DocumentoLavadoActivos(Fact):
    """Documento a evaluar según Ley 27693"""
    tiene_manual_prevencion = Field(bool, default=False)
    tiene_politicas_prevencion = Field(bool, default=False)
    tiene_identificacion_clientes = Field(bool, default=False)
    tiene_registro_operaciones = Field(bool, default=False)
    tiene_reporte_operaciones_sospechosas = Field(bool, default=False)
    tiene_oficial_cumplimiento = Field(bool, default=False)
    tiene_capacitaciones = Field(bool, default=False)
    tiene_evaluacion_riesgos = Field(bool, default=False)
    tiene_debida_diligencia = Field(bool, default=False)
    menciona_uif_peru = Field(bool, default=False)

class ResultadoEvaluacion(Fact):
    """Almacena resultados de la evaluación"""
    cumple = Field(bool, default=True)
    # 🔧 CORREGIDO: Eliminar default con listas mutables
    aspectos_cumplidos = Field(list, mandatory=False)
    aspectos_incumplidos = Field(list, mandatory=False)
    recomendaciones = Field(list, mandatory=False)
    explicacion = Field(str, default="")

class PrevencionLavadoActivosKB(KnowledgeEngine):
    """Motor de inferencia para Ley 27693"""
    
    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    # ================== REGLAS CORREGIDAS ==================
    
    @Rule(
        DocumentoLavadoActivos(tiene_manual_prevencion=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)  # 🔧 CORREGIDO
    )
    def falta_manual_prevencion(self, resultado):
        """Verifica que exista Manual de Prevención de LA/FT"""
        self.declare(Fact(
            tipo="incumplimiento", 
            aspecto="Manual de Prevención LA/FT",
            descripcion="No se identificó un Manual de Prevención de Lavado de Activos y Financiamiento del Terrorismo",
            base_legal="Art. 3, Ley 27693", 
            severidad="crítica"
        ))
        self.explicaciones.append("INCUMPLIMIENTO CRÍTICO: Los sujetos obligados deben contar con un Manual de Prevención de LA/FT (Art. 3, Ley 27693)")
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_manual_prevencion=True),
        ResultadoEvaluacion()
    )
    def cumple_manual_prevencion(self):
        """Confirma presencia de Manual de Prevención"""
        self.declare(Fact(
            tipo="cumplimiento", 
            aspecto="Manual de Prevención LA/FT", 
            descripcion="Se identificó Manual de Prevención de LA/FT"
        ))
        self.explicaciones.append("CUMPLE: El documento contiene Manual de Prevención según Ley 27693")

    # 🔧 REPETIR LA MISMA CORRECCIÓN PARA TODAS LAS REGLAS DE INCUMPLIMIENTO:
    # Cambiar ResultadoEvaluacion() por ResultadoEvaluacion(cumple=True)
    
    @Rule(
        DocumentoLavadoActivos(tiene_politicas_prevencion=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)  # 🔧 CORREGIDO
    )
    def falta_politicas_prevencion(self, resultado):
        self.declare(Fact(
            tipo="incumplimiento", 
            aspecto="Políticas de Prevención", 
            descripcion="No se identificaron políticas y procedimientos de prevención de LA/FT",
            base_legal="Art. 3, Ley 27693", 
            severidad="crítica"
        ))
        self.explicaciones.append("INCUMPLIMIENTO CRÍTICO: Deben existir políticas y procedimientos específicos para la prevención del LA/FT")
        self.modify(resultado, cumple=False)

    # 🔧 AÑADIR REGLA DE SÍNTESIS PARA EVITAR BUCLE INFINITO
    
    @Rule(
        AS.resultado << ResultadoEvaluacion(cumple=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),
        salience=-100
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluación - VERSIÓN CORREGIDA"""
        
        cumplimientos = []
        incumplimientos = []
        recomendaciones = []
        
        # 🔧 CORRECCIÓN: Iterar de forma segura sobre los facts
        for fact in list(self.facts.values()):
            if isinstance(fact, Fact):
                tipo = fact.get('tipo')
                
                if tipo == 'cumplimiento':
                    cumplimientos.append(fact.get('aspecto', 'Aspecto desconocido'))
                    
                elif tipo == 'incumplimiento':
                    incumplimientos.append({
                        'aspecto': fact.get('aspecto', 'Aspecto desconocido'),
                        'descripcion': fact.get('descripcion', 'Sin descripción'),
                        'base_legal': fact.get('base_legal', 'No especificada'),
                        'severidad': fact.get('severidad', 'media')
                    })
                    
                    # Generar recomendaciones específicas
                    aspecto = fact.get('aspecto', '')
                    if 'Manual' in aspecto:
                        recomendaciones.append("Elaborar e implementar un Manual de Prevención de LA/FT conforme a la Ley 27693")
                    elif 'Políticas' in aspecto:
                        recomendaciones.append("Desarrollar políticas y procedimientos específicos de prevención")
                    elif 'Identificación' in aspecto or 'KYC' in aspecto:
                        recomendaciones.append("Implementar procedimientos de conocimiento del cliente (KYC)")
                    elif 'Registro' in aspecto:
                        recomendaciones.append("Establecer sistema de registro de operaciones")
                    elif 'Reporte' in aspecto or 'ROS' in aspecto:
                        recomendaciones.append("Implementar procedimiento para reportar operaciones sospechosas a la UIF-Perú")
                    elif 'Oficial' in aspecto:
                        recomendaciones.append("Designar un Oficial de Cumplimiento responsable")
                    elif 'Capacitación' in aspecto:
                        recomendaciones.append("Implementar programa de capacitación permanente en prevención de LA/FT")
                    elif 'Riesgos' in aspecto:
                        recomendaciones.append("Realizar evaluación de riesgos de LA/FT")
        
        explicacion_final = "\n".join(self.explicaciones)
        
        # 🔧 CORRECCIÓN: Modificar de forma segura
        self.modify(
            resultado,
            cumple=cumple,
            aspectos_cumplidos=cumplimientos,
            aspectos_incumplidos=incumplimientos,
            recomendaciones=recomendaciones,
            explicacion=explicacion_final
        )
        
        # 🔧 EVITAR BUCLE INFINITO
        self.declare(Fact(sintesis_generada=True))
    
    def obtener_resultados(self):
        """Retorna el resultado de la evaluación - VERSIÓN CORREGIDA"""
        try:
            # 🔧 CORRECCIÓN: Buscar de forma más robusta
            for fact_id, fact in list(self.facts.items()):
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacion':
                    return {
                        'cumple': fact.get('cumple', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Si no encuentra resultados, crear uno básico
            return {
                'cumple': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación completada con resultados básicos'
            }
            
        except Exception as e:
            logger.error(f"Error en obtener_resultados: {e}")
            return {
                'cumple': False,
                'aspectos_cumplidos': [],
                'aspectos_incumplidos': [f'Error técnico: {str(e)}'],
                'recomendaciones': ['Contactar soporte técnico'],
                'explicacion': f'Error en evaluación: {str(e)}'
            }
    
    def _extraer_cumplimientos(self):
        """Extrae cumplimientos de los hechos"""
        cumplimientos = []
        for fact in self.facts.values():
            if hasattr(fact, 'get') and fact.get('tipo') == 'cumplimiento':
                cumplimientos.append(fact.get('aspecto', 'Aspecto desconocido'))
        return cumplimientos
    
    def _extraer_incumplimientos(self):
        """Extrae incumplimientos de los hechos"""
        incumplimientos = []
        for fact in self.facts.values():
            if hasattr(fact, 'get') and fact.get('tipo') == 'incumplimiento':
                incumplimientos.append({
                    'aspecto': fact.get('aspecto', 'Aspecto desconocido'),
                    'descripcion': fact.get('descripcion', 'Sin descripción'),
                    'base_legal': fact.get('base_legal', 'No especificada'),
                    'severidad': fact.get('severidad', 'media')
                })
        return incumplimientos