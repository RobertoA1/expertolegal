"""
Reglas de Experta para Ley N° 29783 - Ley de Seguridad y Salud en el Trabajo
Reglamento: D.S. 005-2012-TR y modificatorias
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
    
    # Contexto adicional
    numero_trabajadores = Field(int, default=0)  # Para determinar si necesita Comité o Supervisor

class ResultadoEvaluacion(Fact):
    """Almacena resultados de la evaluación"""
    cumple = Field(bool, default=True)
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class SeguridadSaludTrabajoKB(KnowledgeEngine):
    """Motor de inferencia para Ley 29783"""
    
    def __init__(self):
        super().__init__()
        self.aspectos_evaluados = []
        self.explicaciones = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluación"""
        yield ResultadoEvaluacion()
    
    @Rule(
        DocumentoSST(tiene_reglamento_interno=False, numero_trabajadores=MATCH.n),
        TEST(lambda n: n >= 20),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_reglamento_interno(self):
        """Verifica Reglamento Interno de SST (20+ trabajadores)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Reglamento Interno de SST",
            descripcion="No se identificó Reglamento Interno de Seguridad y Salud en el Trabajo",
            base_legal="Art. 42, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Los empleadores con 20 o más trabajadores deben elaborar "
            "su Reglamento Interno de Seguridad y Salud en el Trabajo (Art. 42, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: El documento contiene Reglamento Interno de Seguridad y Salud en el Trabajo"
        )
    
    @Rule(
        DocumentoSST(tiene_politica_sst=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_politica_sst(self):
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
            "de seguridad y salud en el trabajo, que debe ser específica y apropiada al tamaño y naturaleza "
            "de sus actividades (Art. 22, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: El documento incluye Política de Seguridad y Salud en el Trabajo"
        )
    
    @Rule(
        DocumentoSST(tiene_comite_sst=False, numero_trabajadores=MATCH.n),
        TEST(lambda n: n >= 20),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_comite_sst(self):
        """Verifica Comité de SST (20+ trabajadores)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Comité de Seguridad y Salud en el Trabajo",
            descripcion="No se identificó evidencia del Comité de SST",
            base_legal="Art. 29, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Los empleadores con 20 o más trabajadores deben constituir "
            "un Comité de Seguridad y Salud en el Trabajo, de naturaleza bipartita y paritaria "
            "(Art. 29, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento evidencia la existencia del Comité de SST"
        )
    
    @Rule(
        DocumentoSST(tiene_supervisor_sst=False, numero_trabajadores=MATCH.n),
        TEST(lambda n: 0 < n < 20),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_supervisor_sst(self):
        """Verifica Supervisor de SST (menos de 20 trabajadores)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Supervisor de Seguridad y Salud en el Trabajo",
            descripcion="No se identificó Supervisor de SST",
            base_legal="Art. 30, Ley 29783",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Los empleadores con menos de 20 trabajadores deben capacitar y "
            "nombrar, de entre sus trabajadores, un Supervisor de Seguridad y Salud en el Trabajo "
            "(Art. 30, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento evidencia la designación del Supervisor de SST"
        )
    
    @Rule(
        DocumentoSST(tiene_matriz_iper=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_matriz_iper(self):
        """Verifica Matriz de Identificación de Peligros y Evaluación de Riesgos"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Matriz IPER (Identificación de Peligros y Evaluación de Riesgos)",
            descripcion="No se identificó Matriz IPER",
            base_legal="Art. 57 y 77, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: El empleador debe realizar una evaluación inicial de riesgos "
            "y actualizar la identificación de peligros y evaluación de riesgos (IPER) anualmente como mínimo "
            "(Art. 57 y 77, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye Matriz de Identificación de Peligros y Evaluación de Riesgos"
        )
    
    @Rule(
        DocumentoSST(tiene_plan_anual=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_plan_anual(self):
        """Verifica Plan Anual de SST"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Plan Anual de Seguridad y Salud en el Trabajo",
            descripcion="No se identificó Plan Anual de SST",
            base_legal="Art. 32, D.S. 005-2012-TR",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: El empleador debe elaborar un Plan Anual de Seguridad y Salud en el Trabajo "
            "que contenga los objetivos, metas, actividades y recursos para su implementación "
            "(Art. 32, D.S. 005-2012-TR)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye Plan Anual de Seguridad y Salud en el Trabajo"
        )
    
    @Rule(
        DocumentoSST(tiene_registros_obligatorios=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_registros_obligatorios(self):
        """Verifica Registros Obligatorios del Sistema de Gestión"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registros Obligatorios del Sistema de Gestión de SST",
            descripcion="No se identificaron los registros obligatorios del sistema de gestión",
            base_legal="Art. 33, D.S. 005-2012-TR",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: El empleador debe contar con registros obligatorios del Sistema de Gestión "
            "de SST, que incluyen: registro de accidentes, enfermedades ocupacionales, exámenes médicos, "
            "monitoreos, inspecciones, estadísticas, equipos de emergencia, inducción y capacitación "
            "(Art. 33, D.S. 005-2012-TR)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento evidencia los registros obligatorios del sistema de gestión"
        )
    
    @Rule(
        DocumentoSST(tiene_registro_accidentes=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_registro_accidentes(self):
        """Verifica Registro específico de Accidentes e Incidentes"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registro de Accidentes e Incidentes de Trabajo",
            descripcion="No se identificó Registro de Accidentes e Incidentes",
            base_legal="Art. 88, D.S. 005-2012-TR",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe llevarse un registro de accidentes de trabajo, incidentes peligrosos "
            "y enfermedades ocupacionales (Art. 88, D.S. 005-2012-TR)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye Registro de Accidentes e Incidentes de Trabajo"
        )
    
    @Rule(
        DocumentoSST(tiene_capacitaciones=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_capacitaciones(self):
        """Verifica Programa de Capacitación en SST"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Capacitaciones en Seguridad y Salud en el Trabajo",
            descripcion="No se identificó evidencia de capacitaciones en SST",
            base_legal="Art. 27 y 35, Ley 29783",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: El empleador debe realizar al menos 4 capacitaciones al año en materia "
            "de seguridad y salud en el trabajo. La capacitación debe estar centrada en el puesto de trabajo "
            "específico (Art. 27 y 35, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento evidencia capacitaciones en Seguridad y Salud en el Trabajo"
        )
    
    @Rule(
        DocumentoSST(tiene_examenes_medicos=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_examenes_medicos(self):
        """Verifica Exámenes Médicos Ocupacionales"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Exámenes Médicos Ocupacionales",
            descripcion="No se identificó evidencia de exámenes médicos ocupacionales",
            base_legal="Art. 49, Ley 29783",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: El empleador debe realizar exámenes médicos antes, durante y al término "
            "de la relación laboral a los trabajadores. Los exámenes son con cargo al empleador "
            "(Art. 49, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento evidencia la realización de exámenes médicos ocupacionales"
        )
    
    @Rule(
        DocumentoSST(tiene_epp=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_epp(self):
        """Verifica Equipos de Protección Personal"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Equipos de Protección Personal (EPP)",
            descripcion="No se identificó provisión de EPP",
            base_legal="Art. 60, Ley 29783",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: El empleador debe proporcionar de forma gratuita a sus trabajadores "
            "equipos de protección personal adecuados según el tipo de trabajo y riesgos específicos "
            "(Art. 60, Ley 29783)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: Documento evidencia la provisión de Equipos de Protección Personal"
        )
    
    # Reglas complementarias
    
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
        
        self.explicaciones.append(
            "BUENA PRÁCTICA: El documento incluye Procedimientos Escritos de Trabajo Seguro (PETS)"
        )
    
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
        
        self.explicaciones.append(
            "BUENA PRÁCTICA: El documento especifica las responsabilidades en materia de SST"
        )
    
    # ------ REGLA DE SÍNTESIS --------
    
    @Rule(
        ResultadoEvaluacion(cumple=MATCH.cumple),
        salience=-100
    )
    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluación"""
        cumplimientos = []
        incumplimientos = []
        recomendaciones = []
        
        for fact in self.facts.values():
            if isinstance(fact, Fact):
                if fact.get('tipo') == 'cumplimiento':
                    cumplimientos.append(fact.get('aspecto'))
                elif fact.get('tipo') == 'incumplimiento':
                    incumplimientos.append({
                        'aspecto': fact.get('aspecto'),
                        'descripcion': fact.get('descripcion'),
                        'base_legal': fact.get('base_legal'),
                        'severidad': fact.get('severidad')
                    })
                    
                    # Generar recomendaciones
                    aspecto = fact.get('aspecto', '')
                    if 'Reglamento Interno' in aspecto:
                        recomendaciones.append(
                            "Elaborar e implementar el Reglamento Interno de Seguridad y Salud en el Trabajo"
                        )
                    elif 'Política' in aspecto:
                        recomendaciones.append(
                            "Establecer por escrito la Política de Seguridad y Salud en el Trabajo"
                        )
                    elif 'Comité' in aspecto:
                        recomendaciones.append(
                            "Constituir el Comité de Seguridad y Salud en el Trabajo (paritario y bipartito)"
                        )
                    elif 'Supervisor' in aspecto:
                        recomendaciones.append(
                            "Designar y capacitar a un Supervisor de Seguridad y Salud en el Trabajo"
                        )
                    elif 'IPER' in aspecto or 'Matriz' in aspecto:
                        recomendaciones.append(
                            "Elaborar la Matriz de Identificación de Peligros y Evaluación de Riesgos (IPER)"
                        )
                    elif 'Plan Anual' in aspecto:
                        recomendaciones.append(
                            "Desarrollar el Plan Anual de Seguridad y Salud en el Trabajo"
                        )
                    elif 'Registros' in aspecto:
                        recomendaciones.append(
                            "Implementar los registros obligatorios del sistema de gestión de SST"
                        )
                    elif 'Accidentes' in aspecto:
                        recomendaciones.append(
                            "Llevar el Registro de Accidentes de Trabajo, Incidentes y Enfermedades Ocupacionales"
                        )
                    elif 'Capacitaciones' in aspecto:
                        recomendaciones.append(
                            "Implementar programa de capacitación en SST (mínimo 4 capacitaciones anuales)"
                        )
                    elif 'Exámenes' in aspecto:
                        recomendaciones.append(
                            "Realizar exámenes médicos ocupacionales (pre-ocupacional, periódico y de retiro)"
                        )
                    elif 'EPP' in aspecto:
                        recomendaciones.append(
                            "Proporcionar Equipos de Protección Personal adecuados de forma gratuita"
                        )
        
        # Modificar el resultado final
        explicacion_final = "\n".join(self.explicaciones)
        
        self.modify(
            self.facts[1],
            cumple=cumple,
            aspectos_cumplidos=cumplimientos,
            aspectos_incumplidos=incumplimientos,
            recomendaciones=recomendaciones,
            explicacion=explicacion_final
        )
    
    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacion):
                return {
                    'cumple': fact.get('cumple'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)
    
    def resetear(self):
        """Limpia resultados para nueva evaluación"""
        self.explicaciones = []
        self.aspectos_evaluados = []
        self.reset()