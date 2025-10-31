"""
Reglas de experta para D.S. N° 003-97-TR - Ley de Productividad y Competitividad Laboral (Normas Laborales)
Complementario: Ley N° 28806 - Ley General de Inspección del Trabajo.
Enfoque: Formalidad de la contratación y documentación obligatoria.
"""

from experta import *

class DocumentoNormaLaboral(Fact):
    # Documento a evaluar (ej. Contratos, Reglamento Interno, Boletas, Planillas)
    
    # 1. Formalidad Contractual (Art. 59, 72 LPCL)
    tiene_contratos_escritos_vigentes = Field(bool, default=False)
    tiene_periodo_prueba_informado = Field(bool, default=False) # Si aplica
    
    # 2. Obligaciones Documentarias (Boletas, Planillas)
    tiene_registro_planilla_electronica = Field(bool, default=False) # PLAME / T-Registro
    entrega_boletas_pago_oportunas = Field(bool, default=False)
    
    # 3. Instrumentos de Gestión Laboral
    tiene_reglamento_interno_trabajo = Field(bool, default=False) # Obligatorio si > 100 trabajadores
    
    # 4. Jornada y Horario de Trabajo
    registra_control_asistencia = Field(bool, default=False) # Control de ingreso/salida/sobretiempo

class ResultadoEvaluacionLaboral(Fact):
    # Almacena Resultados de la evaluación de Normas Laborales
    cumple_laboral = Field(bool, default=True) # Cumple con las obligaciones clave de formalidad
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class NormasLaboralesKB(KnowledgeEngine):
    """Motor de inferencia para D.S. 003-97-TR (Normas Laborales) - VERSIÓN CORREGIDA"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    @DefFacts()
    def _inicializar(self):
        yield ResultadoEvaluacionLaboral()

    # ============= REGLAS DE EVALUACIÓN CORREGIDAS =============
    
    # 1. Contratos Escritos y Formalidad (CRÍTICO)
    @Rule(
        DocumentoNormaLaboral(tiene_contratos_escritos_vigentes=False),
        AS.resultado << ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_contratos_escritos(self, resultado):
        """Verifica la formalización de la relación laboral (especialmente contratos modales)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Contratos Escritos y Vigentes",
            descripcion="No se evidencian contratos escritos (o están vencidos/mal formalizados), lo que puede presumir un contrato a plazo indeterminado.",
            base_legal="Art. 72, D.S. 003-97-TR (LPCL)",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Contratos Escritos y Vigentes. "
            "No se evidencian contratos escritos (o están vencidos/mal formalizados), lo que puede presumir un contrato a plazo indeterminado. "
            "(Art. 72, D.S. 003-97-TR)"
        )
        
        self.modify(resultado, cumple_laboral=False)

    @Rule(
        DocumentoNormaLaboral(tiene_contratos_escritos_vigentes=True),
        ResultadoEvaluacionLaboral()
    )
    def cumple_contratos_escritos(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Contratos Escritos y Vigentes",
            descripcion="Se verifica la existencia y vigencia de los contratos de trabajo."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Contratos Escritos y Vigentes.")

    # 2. Registro en Planilla Electrónica (CRÍTICO)
    @Rule(
        DocumentoNormaLaboral(tiene_registro_planilla_electronica=False),
        AS.resultado << ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_registro_planilla(self, resultado):
        """Verifica el registro en Planilla Electrónica"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registro en Planilla Electrónica",
            descripcion="Falta de registro en la Planilla Electrónica (PLAME/T-Registro).",
            base_legal="Ley 28806 / D.S. 003-97-TR",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Registro en Planilla Electrónica. "
            "Falta de registro en la Planilla Electrónica (PLAME/T-Registro). "
            "(Ley 28806 / D.S. 003-97-TR)"
        )
        
        self.modify(resultado, cumple_laboral=False)

    @Rule(
        DocumentoNormaLaboral(tiene_registro_planilla_electronica=True),
        ResultadoEvaluacionLaboral()
    )
    def cumple_registro_planilla(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Registro en Planilla Electrónica",
            descripcion="Se verifica el registro en Planilla Electrónica."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Registro en Planilla Electrónica.")

    # 3. Entrega de Boletas de Pago (CRÍTICO)
    @Rule(
        DocumentoNormaLaboral(entrega_boletas_pago_oportunas=False),
        AS.resultado << ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_boletas_pago(self, resultado):
        """Verifica la entrega oportuna de boletas de pago"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Entrega de Boletas de Pago",
            descripcion="No se evidencia la entrega oportuna de boletas de pago firmadas.",
            base_legal="D.S. 003-97-TR",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Entrega de Boletas de Pago. "
            "No se evidencia la entrega oportuna de boletas de pago firmadas. "
            "(D.S. 003-97-TR)"
        )
        
        self.modify(resultado, cumple_laboral=False)

    @Rule(
        DocumentoNormaLaboral(entrega_boletas_pago_oportunas=True),
        ResultadoEvaluacionLaboral()
    )
    def cumple_boletas_pago(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Entrega de Boletas de Pago",
            descripcion="Se verifica la entrega oportuna de boletas de pago."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Entrega de Boletas de Pago.")

    # 4. Control de Asistencia (ALTA)
    @Rule(
        DocumentoNormaLaboral(registra_control_asistencia=False),
        AS.resultado << ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_control_asistencia(self, resultado):
        """Verifica el registro de control de asistencia, horas extra y jornada"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Control de Asistencia y Horas Extra",
            descripcion="No existe un sistema de control de asistencia o no se registra el sobretiempo correctamente.",
            base_legal="D.S. 004-2006-TR (Reglamento Jornada y Horario)",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Control de Asistencia y Horas Extra. "
            "No existe un sistema de control de asistencia o no se registra el sobretiempo correctamente. "
            "(D.S. 004-2006-TR)"
        )
        
        self.modify(resultado, cumple_laboral=False)

    @Rule(
        DocumentoNormaLaboral(registra_control_asistencia=True),
        ResultadoEvaluacionLaboral()
    )
    def cumple_control_asistencia(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Control de Asistencia y Horas Extra",
            descripcion="Se registra el control de asistencia y jornada laboral."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Control de Asistencia y Horas Extra.")

    # 5. Reglamento Interno de Trabajo (MODERADA/ALTA)
    @Rule(
        DocumentoNormaLaboral(tiene_reglamento_interno_trabajo=False),
        AS.resultado << ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_reglamento_interno(self, resultado):
        """Verifica la existencia del Reglamento Interno de Trabajo (RIT)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Reglamento Interno de Trabajo (RIT)",
            descripcion="Falta el Reglamento Interno de Trabajo, obligatorio si la empresa cuenta con 100 o más trabajadores.",
            base_legal="Art. 17, D.S. 039-91-TR (Reglamento RIT)",
            severidad="moderada"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Reglamento Interno de Trabajo (RIT). "
            "Falta el Reglamento Interno de Trabajo, obligatorio si la empresa cuenta con 100 o más trabajadores. "
            "(Art. 17, D.S. 039-91-TR)"
        )
        
        self.modify(resultado, cumple_laboral=False)

    @Rule(
        DocumentoNormaLaboral(tiene_reglamento_interno_trabajo=True),
        ResultadoEvaluacionLaboral()
    )
    def cumple_reglamento_interno(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Reglamento Interno de Trabajo (RIT)",
            descripcion="Se cuenta con Reglamento Interno de Trabajo."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Reglamento Interno de Trabajo (RIT).")
        
    # 6. Periodo de Prueba (ADICIONAL)
    @Rule(
        DocumentoNormaLaboral(tiene_periodo_prueba_informado=True),
        ResultadoEvaluacionLaboral()
    )
    def cumple_periodo_prueba_informado(self):
        """Valora la correcta información sobre el periodo de prueba"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Periodo de Prueba Informado",
            descripcion="Se consigna expresamente el periodo de prueba en los contratos (Art. 10, LPCL)"
        ))
        self.explicaciones.append("BUENA PRÁCTICA: Se informa correctamente sobre el periodo de prueba.")

    # ============= REGLA DE SÍNTESIS CORREGIDA =============
    
    @Rule(
        AS.resultado << ResultadoEvaluacionLaboral(cumple_laboral=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),
        salience=-1000
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluacion para D.S. 003-97-TR - VERSIÓN CORREGIDA"""
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
            if 'Contratos' in aspecto:
                recomendaciones.append("Formalizar todos los contratos de trabajo, especialmente los modales, asegurando el cumplimiento de los requisitos legales y su registro.")
            elif 'Planilla' in aspecto:
                recomendaciones.append("Regularizar el registro de todos los trabajadores en la Planilla Electrónica (PLAME/T-Registro).")
            elif 'Boletas' in aspecto:
                recomendaciones.append("Asegurar la entrega oportuna de las boletas de pago firmadas a todos los trabajadores.")
            elif 'Control de Asistencia' in aspecto:
                recomendaciones.append("Implementar o formalizar el registro de control de asistencia y asegurar el pago/compensación de las horas extra.")
            elif 'Reglamento Interno' in aspecto:
                recomendaciones.append("Elaborar e implementar el Reglamento Interno de Trabajo si cuenta con 100 o más trabajadores, y depositarlo ante la Autoridad Administrativa de Trabajo.")
        
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            resultado,
            cumple_laboral=cumple,
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
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacionLaboral':
                    return {
                        'cumple_laboral': fact.get('cumple_laboral', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Fallback si no encuentra resultados
            return {
                'cumple_laboral': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
            return {
                'cumple_laboral': False,
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