"""
Reglas de Experta para Ley N° 29783 - Ley de Seguridad y Salud en el Trabajo
Reglamento: D.S. 005-2012-TR y modificatorias
(Versión corregida para compatibilidad con el sistema)
"""

from experta import *

class DocumentoSST(Fact):
    """Documento a evaluar según Ley 29783"""
    tiene_reglamento_interno = Field(bool, default=False)
    tiene_politica_sst = Field(bool, default=False)
    tiene_comite_sst = Field(bool, default=False)
    tiene_supervisor_sst = Field(bool, default=False)
    tiene_matriz_iper = Field(bool, default=False)
    tiene_plan_anual = Field(bool, default=False)
    tiene_registros_obligatorios = Field(bool, default=False)
    tiene_registro_accidentes = Field(bool, default=False)
    tiene_capacitaciones = Field(bool, default=False)
    tiene_examenes_medicos = Field(bool, default=False)
    tiene_epp = Field(bool, default=False)
    tiene_procedimientos_trabajo_seguro = Field(bool, default=False)
    menciona_responsabilidades = Field(bool, default=False)
    numero_trabajadores = Field(int, default=0)

class ResultadoEvaluacion(Fact):
    """Almacena resultados de la evaluación"""
    cumple = Field(bool, default=True)
    # 🔧 CORREGIDO: Eliminar default con listas mutables
    aspectos_cumplidos = Field(list, mandatory=False)
    aspectos_incumplidos = Field(list, mandatory=False)
    recomendaciones = Field(list, mandatory=False)
    explicacion = Field(str, default="")

class SeguridadSaludTrabajoKB(KnowledgeEngine):
    """Motor de inferencia para Ley 29783"""
    
    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    # 🔧 ELIMINADO: No usar @DefFacts, se declara desde la aplicación
    
    # ============= REGLAS DE INCUMPLIMIENTO CORREGIDAS =============
    
    @Rule(
        DocumentoSST(tiene_reglamento_interno=False, numero_trabajadores=MATCH.n),
        TEST(lambda n: n >= 20),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_reglamento_interno(self, resultado, n):
        """Verifica Reglamento Interno de SST (20+ trabajadores)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Reglamento Interno de SST",
            descripcion="No se identificó Reglamento Interno de Seguridad y Salud en el Trabajo",
            base_legal="Art. 42, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            f"INCUMPLIMIENTO CRÍTICO: Con {n} trabajadores, debe elaborar Reglamento Interno de SST (Art. 42, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_reglamento_interno=True),
        ResultadoEvaluacion()
    )
    def cumple_reglamento_interno(self):
        """Confirma Reglamento Interno de SST"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Reglamento Interno de SST",
            descripcion="Se identificó Reglamento Interno de SST"
        ))
        self.explicaciones.append("CUMPLE: Documento contiene Reglamento Interno de SST")
    
    @Rule(
        DocumentoSST(tiene_politica_sst=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_politica_sst(self, resultado):
        """Verifica Política de SST"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Política de Seguridad y Salud en el Trabajo",
            descripcion="No se identificó la Política de SST",
            base_legal="Art. 22, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: El empleador debe establecer por escrito la política en materia "
            "de seguridad y salud en el trabajo (Art. 22, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_politica_sst=True),
        ResultadoEvaluacion()
    )
    def cumple_politica_sst(self):
        """Confirma Política de SST"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Política de Seguridad y Salud en el Trabajo",
            descripcion="Se identificó Política de SST"
        ))
        self.explicaciones.append("CUMPLE: Documento incluye Política de SST")
    
    @Rule(
        DocumentoSST(tiene_comite_sst=False, numero_trabajadores=MATCH.n),
        TEST(lambda n: n >= 20),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_comite_sst(self, resultado, n):
        """Verifica Comité de SST (20+ trabajadores)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Comité de Seguridad y Salud en el Trabajo",
            descripcion="No se identificó evidencia del Comité de SST",
            base_legal="Art. 29, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            f"INCUMPLIMIENTO CRÍTICO: Con {n} trabajadores, debe constituir Comité de SST (Art. 29, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_comite_sst=True),
        ResultadoEvaluacion()
    )
    def cumple_comite_sst(self):
        """Confirma Comité de SST"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Comité de Seguridad y Salud en el Trabajo",
            descripcion="Se identificó Comité de SST"
        ))
        self.explicaciones.append("CUMPLE: Documento evidencia Comité de SST")
    
    @Rule(
        DocumentoSST(tiene_supervisor_sst=False, numero_trabajadores=MATCH.n),
        TEST(lambda n: 0 < n < 20),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_supervisor_sst(self, resultado, n):
        """Verifica Supervisor de SST (menos de 20 trabajadores)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Supervisor de Seguridad y Salud en el Trabajo",
            descripcion="No se identificó Supervisor de SST",
            base_legal="Art. 30, Ley 29783",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            f"INCUMPLIMIENTO: Con {n} trabajadores, debe designar Supervisor de SST (Art. 30, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_supervisor_sst=True),
        ResultadoEvaluacion()
    )
    def cumple_supervisor_sst(self):
        """Confirma Supervisor de SST"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Supervisor de Seguridad y Salud en el Trabajo",
            descripcion="Se identificó Supervisor de SST"
        ))
        self.explicaciones.append("CUMPLE: Documento evidencia Supervisor de SST")
    
    @Rule(
        DocumentoSST(tiene_matriz_iper=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_matriz_iper(self, resultado):
        """Verifica Matriz de Identificación de Peligros y Evaluación de Riesgos"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Matriz IPER (Identificación de Peligros y Evaluación de Riesgos)",
            descripcion="No se identificó Matriz IPER",
            base_legal="Art. 57 y 77, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Debe realizar evaluación de riesgos y Matriz IPER anualmente (Art. 57 y 77, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_matriz_iper=True),
        ResultadoEvaluacion()
    )
    def cumple_matriz_iper(self):
        """Confirma Matriz IPER"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Matriz IPER (Identificación de Peligros y Evaluación de Riesgos)",
            descripcion="Se identificó Matriz IPER"
        ))
        self.explicaciones.append("CUMPLE: Documento incluye Matriz IPER")
    
    @Rule(
        DocumentoSST(tiene_plan_anual=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_plan_anual(self, resultado):
        """Verifica Plan Anual de SST"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Plan Anual de Seguridad y Salud en el Trabajo",
            descripcion="No se identificó Plan Anual de SST",
            base_legal="Art. 32, D.S. 005-2012-TR",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe elaborar Plan Anual de SST con objetivos, metas y recursos (Art. 32, D.S. 005-2012-TR)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_plan_anual=True),
        ResultadoEvaluacion()
    )
    def cumple_plan_anual(self):
        """Confirma Plan Anual de SST"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Plan Anual de Seguridad y Salud en el Trabajo",
            descripcion="Se identificó Plan Anual de SST"
        ))
        self.explicaciones.append("CUMPLE: Documento incluye Plan Anual de SST")
    
    @Rule(
        DocumentoSST(tiene_registros_obligatorios=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_registros_obligatorios(self, resultado):
        """Verifica Registros Obligatorios del Sistema de Gestión"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registros Obligatorios del Sistema de Gestión de SST",
            descripcion="No se identificaron los registros obligatorios del sistema de gestión",
            base_legal="Art. 33, D.S. 005-2012-TR",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe contar con registros obligatorios del Sistema de Gestión de SST (Art. 33, D.S. 005-2012-TR)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_registros_obligatorios=True),
        ResultadoEvaluacion()
    )
    def cumple_registros_obligatorios(self):
        """Confirma Registros Obligatorios"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Registros Obligatorios del Sistema de Gestión de SST",
            descripcion="Se identificaron registros obligatorios"
        ))
        self.explicaciones.append("CUMPLE: Documento evidencia registros obligatorios")
    
    @Rule(
        DocumentoSST(tiene_registro_accidentes=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_registro_accidentes(self, resultado):
        """Verifica Registro específico de Accidentes e Incidentes"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registro de Accidentes e Incidentes de Trabajo",
            descripcion="No se identificó Registro de Accidentes e Incidentes",
            base_legal="Art. 88, D.S. 005-2012-TR",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe llevar registro de accidentes e incidentes (Art. 88, D.S. 005-2012-TR)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_registro_accidentes=True),
        ResultadoEvaluacion()
    )
    def cumple_registro_accidentes(self):
        """Confirma Registro de Accidentes"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Registro de Accidentes e Incidentes de Trabajo",
            descripcion="Se identificó Registro de Accidentes e Incidentes"
        ))
        self.explicaciones.append("CUMPLE: Documento incluye Registro de Accidentes")
    
    @Rule(
        DocumentoSST(tiene_capacitaciones=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_capacitaciones(self, resultado):
        """Verifica Programa de Capacitación en SST"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Capacitaciones en Seguridad y Salud en el Trabajo",
            descripcion="No se identificó evidencia de capacitaciones en SST",
            base_legal="Art. 27 y 35, Ley 29783",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe realizar al menos 4 capacitaciones anuales en SST (Art. 27 y 35, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_capacitaciones=True),
        ResultadoEvaluacion()
    )
    def cumple_capacitaciones(self):
        """Confirma Capacitaciones en SST"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Capacitaciones en Seguridad y Salud en el Trabajo",
            descripcion="Se identificó programa de capacitación"
        ))
        self.explicaciones.append("CUMPLE: Documento evidencia capacitaciones en SST")
    
    @Rule(
        DocumentoSST(tiene_examenes_medicos=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_examenes_medicos(self, resultado):
        """Verifica Exámenes Médicos Ocupacionales"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Exámenes Médicos Ocupacionales",
            descripcion="No se identificó evidencia de exámenes médicos ocupacionales",
            base_legal="Art. 49, Ley 29783",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe realizar exámenes médicos ocupacionales (Art. 49, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_examenes_medicos=True),
        ResultadoEvaluacion()
    )
    def cumple_examenes_medicos(self):
        """Confirma Exámenes Médicos"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Exámenes Médicos Ocupacionales",
            descripcion="Se identificó programa de exámenes médicos"
        ))
        self.explicaciones.append("CUMPLE: Documento evidencia exámenes médicos")
    
    @Rule(
        DocumentoSST(tiene_epp=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_epp(self, resultado):
        """Verifica Equipos de Protección Personal"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Equipos de Protección Personal (EPP)",
            descripcion="No se identificó provisión de EPP",
            base_legal="Art. 60, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Debe proporcionar EPP de forma gratuita (Art. 60, Ley 29783)"
        )
        
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoSST(tiene_epp=True),
        ResultadoEvaluacion()
    )
    def cumple_epp(self):
        """Confirma provisión de EPP"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Equipos de Protección Personal (EPP)",
            descripcion="Se identificó provisión de EPP"
        ))
        self.explicaciones.append("CUMPLE: Documento evidencia provisión de EPP")
    
    # ============= REGLAS COMPLEMENTARIAS =============
    
    @Rule(
        DocumentoSST(tiene_procedimientos_trabajo_seguro=True),
        ResultadoEvaluacion()
    )
    def tiene_procedimientos(self):
        """Valora positivamente los procedimientos de trabajo seguro"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Procedimientos de Trabajo Seguro",
            descripcion="Se identificaron procedimientos escritos de trabajo seguro (PETS)"
        ))
        self.explicaciones.append("BUENA PRÁCTICA: Incluye Procedimientos Escritos de Trabajo Seguro")
    
    @Rule(
        DocumentoSST(menciona_responsabilidades=True),
        ResultadoEvaluacion()
    )
    def menciona_responsabilidades(self):
        """Valora mención de responsabilidades"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Responsabilidades en SST",
            descripcion="Se identifican responsabilidades de empleador y trabajadores"
        ))
        self.explicaciones.append("BUENA PRÁCTICA: Especifica responsabilidades en SST")
    
    # ============= REGLA DE SÍNTESIS CORREGIDA =============
    
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
        
        # 🔧 CORRECCIÓN: Iterar de forma segura
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
                    
                    # Generar recomendaciones
                    aspecto = fact.get('aspecto', '')
                    if 'Reglamento Interno' in aspecto:
                        recomendaciones.append("Elaborar e implementar el Reglamento Interno de SST")
                    elif 'Política' in aspecto:
                        recomendaciones.append("Establecer por escrito la Política de SST")
                    elif 'Comité' in aspecto:
                        recomendaciones.append("Constituir el Comité de SST (paritario y bipartito)")
                    elif 'Supervisor' in aspecto:
                        recomendaciones.append("Designar y capacitar a un Supervisor de SST")
                    elif 'IPER' in aspecto or 'Matriz' in aspecto:
                        recomendaciones.append("Elaborar la Matriz IPER")
                    elif 'Plan Anual' in aspecto:
                        recomendaciones.append("Desarrollar el Plan Anual de SST")
                    elif 'Registros' in aspecto:
                        recomendaciones.append("Implementar registros obligatorios del sistema de gestión")
                    elif 'Accidentes' in aspecto:
                        recomendaciones.append("Llevar Registro de Accidentes e Incidentes")
                    elif 'Capacitaciones' in aspecto:
                        recomendaciones.append("Implementar programa de capacitación en SST (mínimo 4 anuales)")
                    elif 'Exámenes' in aspecto:
                        recomendaciones.append("Realizar exámenes médicos ocupacionales")
                    elif 'EPP' in aspecto:
                        recomendaciones.append("Proporcionar EPP adecuados de forma gratuita")
        
        explicacion_final = "\n".join(self.explicaciones)
        
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
    
    # ============= MÉTODOS DE UTILIDAD =============
    
    def obtener_resultados(self):
        """Retorna el resultado de la evaluación - VERSIÓN ROBUSTA"""
        try:
            for fact_id, fact in list(self.facts.items()):
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacion':
                    return {
                        'cumple': fact.get('cumple', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Fallback si no encuentra resultados
            return {
                'cumple': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
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
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)