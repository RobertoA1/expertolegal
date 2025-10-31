"""
Reglas de experta para Normativa Ambiental (Ley General del Ambiente - Ley N° 28611) 🌿
Enfoque: Instrumentos de Gestión Ambiental (IGA/IEGA), Licencias y Cumplimiento de ECA/LMP.
"""

from experta import *

class AspectoAmbiental(Fact):
    # Hechos sobre la situacion ambiental de la empresa
    
    # 1. Evaluación de Impacto Ambiental (Ley 27446 / Ley 28611)
    tiene_estudio_impacto_ambiental = Field(bool, default=False) 
    
    # 2. Fiscalización y Monitoreo
    tiene_monitoreo_ambiental = Field(bool, default=False) 
    
    # 3. Cumplimiento de Estándares
    cumple_LMP_ECA = Field(bool, default=False) 
    
    # 4. Gestión de Residuos
    tiene_registro_residuos_solidos = Field(bool, default=False) 
    
    # 5. Autorizaciones Específicas
    tiene_autorizacion_vertimientos = Field(bool, default=False)
    
    # 6. Planes de Gestión
    tiene_plan_manejo_ambiental = Field(bool, default=False)
    
    # 7. Sistema de Gestión
    tiene_sistema_gestion_ambiental = Field(bool, default=False)
    
    # 8. Plan de Contingencias
    tiene_plan_contigencia = Field(bool, default=False)

class ResultadoEvaluacionAmbiental(Fact):
    # Almacena Resultados de la evaluación de Normativa Ambiental
    cumple_ambiental = Field(bool, default=True)
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class NormativaAmbientalKB(KnowledgeEngine):
    """Motor de inferencia para Ley 28611 - Ley General del Ambiente - VERSIÓN CORREGIDA"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    @DefFacts()
    def _inicializar(self):
        yield ResultadoEvaluacionAmbiental()

    # ============= REGLAS DE EVALUACIÓN CORREGIDAS =============
    
    # 1. Estudio de Impacto Ambiental (CRÍTICO)
    @Rule(
        AspectoAmbiental(tiene_estudio_impacto_ambiental=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_estudio_impacto(self, resultado):
        """Verifica la existencia del Estudio de Impacto Ambiental"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Estudio de Impacto Ambiental",
            descripcion="El proyecto no cuenta con EIA aprobado por la autoridad competente.",
            base_legal="Art. 28, Ley 28611 / Ley 27446 (SEIA)",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Estudio de Impacto Ambiental. "
            "El proyecto no cuenta con EIA aprobado por la autoridad competente. "
            "(Art. 28, Ley 28611)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(tiene_estudio_impacto_ambiental=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_estudio_impacto(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Estudio de Impacto Ambiental",
            descripcion="El proyecto cuenta con EIA aprobado y vigente."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Estudio de Impacto Ambiental.")

    # 2. Monitoreo Ambiental (ALTA)
    @Rule(
        AspectoAmbiental(tiene_monitoreo_ambiental=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_monitoreo_ambiental(self, resultado):
        """Verifica la ejecución del monitoreo ambiental"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Monitoreo Ambiental",
            descripcion="No se ejecuta el plan de monitoreo ambiental requerido.",
            base_legal="D.S. 004-2017-MINAM (Reglamento OEFA)",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Monitoreo Ambiental. "
            "No se ejecuta el plan de monitoreo ambiental requerido. "
            "(D.S. 004-2017-MINAM)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(tiene_monitoreo_ambiental=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_monitoreo_ambiental(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Monitoreo Ambiental",
            descripcion="Se ejecuta el programa de monitoreo ambiental."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Monitoreo Ambiental.")

    # 3. Cumplimiento de LMP y ECA (CRÍTICO)
    @Rule(
        AspectoAmbiental(cumple_LMP_ECA=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def incumplimiento_limites(self, resultado):
        """Verifica el cumplimiento de LMP y ECA"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Cumplimiento de LMP y ECA",
            descripcion="Se superan los límites máximos permisibles o estándares de calidad ambiental.",
            base_legal="Art. 34, Ley 28611",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Cumplimiento de LMP y ECA. "
            "Se superan los límites máximos permisibles o estándares de calidad ambiental. "
            "(Art. 34, Ley 28611)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(cumple_LMP_ECA=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_limites(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Cumplimiento de LMP y ECA",
            descripcion="Se cumplen los límites máximos permisibles y estándares de calidad ambiental."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Cumplimiento de LMP y ECA.")

    # 4. Registro de Residuos Sólidos (ALTA)
    @Rule(
        AspectoAmbiental(tiene_registro_residuos_solidos=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_registro_residuos(self, resultado):
        """Verifica el registro de generador de residuos"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registro de Residuos Sólidos",
            descripcion="No se cuenta con registro de generador de residuos sólidos.",
            base_legal="D.L. 1278 (Ley de Gestión Integral de Residuos Sólidos)",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Registro de Residuos Sólidos. "
            "No se cuenta con registro de generador de residuos sólidos. "
            "(D.L. 1278)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(tiene_registro_residuos_solidos=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_registro_residuos(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Registro de Residuos Sólidos",
            descripcion="Se cuenta con registro de generador de residuos sólidos."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Registro de Residuos Sólidos.")

    # 5. Autorización de Vertimientos (ALTA)
    @Rule(
        AspectoAmbiental(tiene_autorizacion_vertimientos=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_autorizacion_vertimientos(self, resultado):
        """Verifica la autorización de vertimientos"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Autorización de Vertimientos",
            descripcion="No se cuenta con autorización para vertimientos de aguas residuales.",
            base_legal="Ley 29338 - Ley de Recursos Hídricos",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Autorización de Vertimientos. "
            "No se cuenta con autorización para vertimientos de aguas residuales. "
            "(Ley 29338)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(tiene_autorizacion_vertimientos=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_autorizacion_vertimientos(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Autorización de Vertimientos",
            descripcion="Se cuenta con autorización para vertimientos."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Autorización de Vertimientos.")

    # 6. Plan de Manejo Ambiental (MODERADA)
    @Rule(
        AspectoAmbiental(tiene_plan_manejo_ambiental=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_plan_manejo(self, resultado):
        """Verifica la existencia del plan de manejo ambiental"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Plan de Manejo Ambiental",
            descripcion="No se cuenta con plan de manejo ambiental implementado.",
            base_legal="D.S. 019-2009-MINAM",
            severidad="moderada"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Plan de Manejo Ambiental. "
            "No se cuenta con plan de manejo ambiental implementado. "
            "(D.S. 019-2009-MINAM)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(tiene_plan_manejo_ambiental=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_plan_manejo(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Plan de Manejo Ambiental",
            descripcion="Se cuenta con plan de manejo ambiental implementado."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Plan de Manejo Ambiental.")

    # 7. Sistema de Gestión Ambiental (MODERADA)
    @Rule(
        AspectoAmbiental(tiene_sistema_gestion_ambiental=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_sistema_gestion(self, resultado):
        """Verifica la existencia de sistema de gestión ambiental"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Sistema de Gestión Ambiental",
            descripcion="No se cuenta con sistema de gestión ambiental implementado.",
            base_legal="ISO 14001 / Políticas internas",
            severidad="moderada"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Sistema de Gestión Ambiental. "
            "No se cuenta con sistema de gestión ambiental implementado. "
            "(ISO 14001)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(tiene_sistema_gestion_ambiental=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_sistema_gestion(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Sistema de Gestión Ambiental",
            descripcion="Se cuenta con sistema de gestión ambiental implementado."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Sistema de Gestión Ambiental.")

    # 8. Plan de Contingencias (MODERADA)
    @Rule(
        AspectoAmbiental(tiene_plan_contigencia=False),
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_plan_contingencia(self, resultado):
        """Verifica la existencia del plan de contingencias"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Plan de Contingencias",
            descripcion="No se cuenta con plan de contingencias ambientales.",
            base_legal="D.S. 081-2007-PCM",
            severidad="moderada"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Plan de Contingencias. "
            "No se cuenta con plan de contingencias ambientales. "
            "(D.S. 081-2007-PCM)"
        )
        
        self.modify(resultado, cumple_ambiental=False)

    @Rule(
        AspectoAmbiental(tiene_plan_contigencia=True),
        ResultadoEvaluacionAmbiental()
    )
    def cumple_plan_contingencia(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Plan de Contingencias",
            descripcion="Se cuenta con plan de contingencias ambientales."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Plan de Contingencias.")

    # ============= REGLA DE SÍNTESIS CORREGIDA =============
    
    @Rule(
        AS.resultado << ResultadoEvaluacionAmbiental(cumple_ambiental=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),
        salience=-1000
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluacion para Ley 28611 - VERSIÓN CORREGIDA"""
        cumplimientos = []
        incumplimientos = []
        recomendaciones = []
        
        # Procesar todos los hechos
        for fact in list(self.facts.values()):
            if isinstance(fact, Fact):
                tipo = fact.get('tipo')
                
                if tipo in ['cumplimiento', 'cumplimiento_adicional']:
                    cumplimientos.append(fact.get('aspecto', 'Aspecto desconocido'))
                    
                elif tipo == 'incumplimiento':
                    incumplimientos.append({
                        'aspecto': fact.get('aspecto', 'Aspecto desconocido'),
                        'descripcion': fact.get('descripcion', 'Sin descripción'),
                        'base_legal': fact.get('base_legal', 'No especificada'),
                        'severidad': fact.get('severidad', 'media')
                    })
        
        # Generar recomendaciones basadas en incumplimientos
        for incumplimiento in incumplimientos:
            aspecto = incumplimiento.get('aspecto', '')
            if 'Estudio de Impacto' in aspecto:
                recomendaciones.append("Tramitar la aprobación del Estudio de Impacto Ambiental correspondiente ante la autoridad competente.")
            elif 'Monitoreo Ambiental' in aspecto:
                recomendaciones.append("Implementar programa de monitoreo ambiental continuo y presentar informes periódicos.")
            elif 'LMP y ECA' in aspecto:
                recomendaciones.append("Implementar medidas correctivas para cumplir con los límites máximos permisibles y estándares de calidad ambiental.")
            elif 'Residuos Sólidos' in aspecto:
                recomendaciones.append("Implementar Plan de Manejo de Residuos Sólidos y realizar declaración anual.")
            elif 'Vertimientos' in aspecto:
                recomendaciones.append("Obtener autorización de vertimientos de la Autoridad Nacional del Agua.")
            elif 'Plan de Manejo' in aspecto:
                recomendaciones.append("Elaborar e implementar plan de manejo ambiental específico.")
            elif 'Sistema de Gestión' in aspecto:
                recomendaciones.append("Implementar sistema de gestión ambiental (ISO 14001 u otro).")
            elif 'Contingencias' in aspecto:
                recomendaciones.append("Elaborar e implementar plan de contingencias ambientales.")
        
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            resultado,
            cumple_ambiental=cumple,
            aspectos_cumplidos=cumplimientos,
            aspectos_incumplidos=incumplimientos,
            recomendaciones=recomendaciones,
            explicacion=explicacion_final
        )
        
        # 🔧 EVITAR BUCLE INFINITO
        self.declare(Fact(sintesis_generada=True))

    # ============= MÉTODOS DE UTILIDAD =============
    
    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        try:
            for fact_id, fact in list(self.facts.items()):
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacionAmbiental':
                    return {
                        'cumple_ambiental': fact.get('cumple_ambiental', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Fallback si no encuentra resultados
            return {
                'cumple_ambiental': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
            return {
                'cumple_ambiental': False,
                'aspectos_cumplidos': [],
                'aspectos_incumplidos': [f'Error técnico: {str(e)}'],
                'recomendaciones': ['Contactar soporte técnico'],
                'explicacion': f'Error en evaluación: {str(e)}'
            }
    
    def _extraer_cumplimientos(self):
        """Extrae cumplimientos de los hechos"""
        cumplimientos = []
        for fact in self.facts.values():
            if hasattr(fact, 'get') and fact.get('tipo') in ['cumplimiento', 'cumplimiento_adicional']:
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
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)