"""
Reglas de Experta para Ley N° 27693 - Ley de Prevención de Lavado de Activos
y modificatorias (Ley N° 30424, D.Leg. 1249, etc.)
"""

from experta import *

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
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class PrevencionLavadoActivosKB(KnowledgeEngine):
    """Motor de inferencia para Ley 27693"""
    
    def __init__(self):
        super().__init__()
        self.aspectos_evaluados = []
        self.explicaciones = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluación"""
        yield ResultadoEvaluacion()
    
    @Rule(
        DocumentoLavadoActivos(tiene_manual_prevencion=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_manual_prevencion(self):
        """Verifica que exista Manual de Prevención de LA/FT"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Manual de Prevención LA/FT",
            descripcion="No se identificó un Manual de Prevención de Lavado de Activos y Financiamiento del Terrorismo",
            base_legal="Art. 3, Ley 27693",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Los sujetos obligados deben contar con un Manual de "
            "Prevención de Lavado de Activos y Financiamiento del Terrorismo (Art. 3, Ley 27693)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
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
        
        self.explicaciones.append(
            "CUMPLE: El documento contiene Manual de Prevención de Lavado de Activos según Ley 27693"
        )
    
    @Rule(
        DocumentoLavadoActivos(tiene_politicas_prevencion=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_politicas_prevencion(self):
        """Verifica existencia de políticas de prevención"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Políticas de Prevención",
            descripcion="No se identificaron políticas y procedimientos de prevención de LA/FT",
            base_legal="Art. 3, Ley 27693",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Deben existir políticas y procedimientos específicos "
            "para la prevención del lavado de activos (Art. 3, Ley 27693)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_politicas_prevencion=True),
        ResultadoEvaluacion()
    )
    def cumple_politicas_prevencion(self):
        """Confirma políticas de prevención"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Políticas de Prevención",
            descripcion="Se identificaron políticas de prevención de LA/FT"
        ))
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye políticas de prevención según Ley 27693"
        )
    
    @Rule(
        DocumentoLavadoActivos(tiene_identificacion_clientes=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_identificacion_clientes(self):
        """Verifica procedimientos de identificación de clientes (KYC)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Identificación de Clientes (KYC)",
            descripcion="No se identificaron procedimientos de identificación y conocimiento del cliente",
            base_legal="Art. 3 inc. a), Ley 27693",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Debe establecerse un sistema de conocimiento del cliente "
            "(KYC - Know Your Customer) para identificar y verificar la identidad de los clientes "
            "(Art. 3 inc. a), Ley 27693)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_identificacion_clientes=True),
        ResultadoEvaluacion()
    )
    def cumple_identificacion_clientes(self):
        """Confirma procedimientos KYC"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Identificación de Clientes (KYC)",
            descripcion="Se identificaron procedimientos de conocimiento del cliente"
        ))
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye procedimientos de identificación de clientes (KYC)"
        )
    
    @Rule(
        DocumentoLavadoActivos(tiene_registro_operaciones=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_registro_operaciones(self):
        """Verifica registro de operaciones"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registro de Operaciones",
            descripcion="No se identificó sistema de registro de operaciones",
            base_legal="Art. 3 inc. b), Ley 27693",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe mantenerse un registro de las operaciones que superen "
            "los montos establecidos por la normativa (Art. 3 inc. b), Ley 27693)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_registro_operaciones=True),
        ResultadoEvaluacion()
    )
    def cumple_registro_operaciones(self):
        """Confirma registro de operaciones"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Registro de Operaciones",
            descripcion="Se identificó sistema de registro de operaciones"
        ))
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye sistema de registro de operaciones"
        )
    
    @Rule(
        DocumentoLavadoActivos(tiene_reporte_operaciones_sospechosas=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_reporte_operaciones_sospechosas(self):
        """Verifica procedimiento de reporte de operaciones sospechosas"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Reporte de Operaciones Sospechosas (ROS)",
            descripcion="No se identificó procedimiento para reportar operaciones sospechosas",
            base_legal="Art. 3 inc. c), Ley 27693",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Debe establecerse un procedimiento para detectar y reportar "
            "operaciones sospechosas a la UIF-Perú (Art. 3 inc. c), Ley 27693)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_reporte_operaciones_sospechosas=True),
        ResultadoEvaluacion()
    )
    def cumple_reporte_operaciones_sospechosas(self):
        """Confirma procedimiento de ROS"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Reporte de Operaciones Sospechosas (ROS)",
            descripcion="Se identificó procedimiento de reporte de operaciones sospechosas"
        ))
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye procedimiento para reportar operaciones sospechosas"
        )
    
    @Rule(
        DocumentoLavadoActivos(tiene_oficial_cumplimiento=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_oficial_cumplimiento(self):
        """Verifica designación de Oficial de Cumplimiento"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Oficial de Cumplimiento",
            descripcion="No se identificó la designación de un Oficial de Cumplimiento",
            base_legal="Art. 3 inc. d), Ley 27693",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Debe designarse un Oficial de Cumplimiento responsable "
            "de la implementación del sistema de prevención (Art. 3 inc. d), Ley 27693)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_oficial_cumplimiento=True),
        ResultadoEvaluacion()
    )
    def cumple_oficial_cumplimiento(self):
        """Confirma Oficial de Cumplimiento"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Oficial de Cumplimiento",
            descripcion="Se identificó designación de Oficial de Cumplimiento"
        ))
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye designación de Oficial de Cumplimiento"
        )
    
    @Rule(
        DocumentoLavadoActivos(tiene_capacitaciones=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_capacitaciones(self):
        """Verifica programa de capacitación"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Capacitación del Personal",
            descripcion="No se identificó programa de capacitación en prevención de LA/FT",
            base_legal="Art. 3 inc. e), Ley 27693",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe implementarse un programa de capacitación permanente "
            "para el personal en materia de prevención de LA/FT (Art. 3 inc. e), Ley 27693)"
        )
        
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_capacitaciones=True),
        ResultadoEvaluacion()
    )
    def cumple_capacitaciones(self):
        """Confirma programa de capacitación"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Capacitación del Personal",
            descripcion="Se identificó programa de capacitación"
        ))
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye programa de capacitación en prevención de LA/FT"
        )
    
    @Rule(
        DocumentoLavadoActivos(tiene_evaluacion_riesgos=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_evaluacion_riesgos(self):
        """Verifica evaluación de riesgos de LA/FT"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Evaluación de Riesgos LA/FT",
            descripcion="No se identificó evaluación de riesgos de lavado de activos",
            base_legal="Enfoque Basado en Riesgos - GAFI",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe realizarse una evaluación de riesgos de LA/FT según "
            "el enfoque basado en riesgos (Risk-Based Approach) recomendado por GAFI"
        )
        
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoLavadoActivos(tiene_evaluacion_riesgos=True),
        ResultadoEvaluacion()
    )
    def cumple_evaluacion_riesgos(self):
        """Confirma evaluación de riesgos"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Evaluación de Riesgos LA/FT",
            descripcion="Se identificó evaluación de riesgos"
        ))
        
        self.explicaciones.append(
            "CUMPLE: Documento incluye evaluación de riesgos de LA/FT"
        )
    
    # Reglas complementarias
    
    @Rule(
        DocumentoLavadoActivos(tiene_debida_diligencia=True),
        ResultadoEvaluacion()
    )
    def tiene_debida_diligencia(self):
        """Valora positivamente la debida diligencia reforzada"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Debida Diligencia",
            descripcion="Se identificaron procedimientos de debida diligencia del cliente"
        ))
        
        self.explicaciones.append(
            "BUENA PRÁCTICA: Se identifican procedimientos de debida diligencia del cliente"
        )
    
    @Rule(
        DocumentoLavadoActivos(menciona_uif_peru=True),
        ResultadoEvaluacion()
    )
    def menciona_uif(self):
        """Valora mención de la UIF-Perú"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Mención UIF-Perú",
            descripcion="Se menciona a la Unidad de Inteligencia Financiera del Perú"
        ))
        
        self.explicaciones.append(
            "BUENA PRÁCTICA: El documento menciona a la UIF-Perú como entidad receptora de reportes"
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
                    if 'Manual' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Elaborar e implementar un Manual de Prevención de LA/FT conforme a la Ley 27693"
                        )
                    elif 'Políticas' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Desarrollar políticas y procedimientos específicos de prevención de lavado de activos"
                        )
                    elif 'KYC' in fact.get('aspecto', '') or 'Identificación' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Implementar procedimientos de debida diligencia y conocimiento del cliente (KYC)"
                        )
                    elif 'Registro' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Establecer un sistema de registro de operaciones que superen los montos establecidos"
                        )
                    elif 'Reporte' in fact.get('aspecto', '') or 'ROS' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Implementar procedimiento para detectar y reportar operaciones sospechosas a la UIF-Perú"
                        )
                    elif 'Oficial' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Designar un Oficial de Cumplimiento responsable del sistema de prevención"
                        )
                    elif 'Capacitación' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Implementar programa de capacitación permanente en prevención de LA/FT"
                        )
                    elif 'Riesgos' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Realizar evaluación de riesgos de LA/FT según enfoque basado en riesgos"
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