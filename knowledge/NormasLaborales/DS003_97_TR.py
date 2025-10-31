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
    """Motor de inferencia para D.S. 003-97-TR (Normas Laborales)"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
        self.recomendaciones_generadas = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluacion"""
        yield ResultadoEvaluacionLaboral()
    
    # --- Funciones Auxiliares ---

    def _registrar_incumplimiento(self, aspecto, descripcion, base_legal, severidad, recomendacion_texto):
        """Registra un incumplimiento y modifica el estado general de cumplimiento"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto=aspecto,
            descripcion=descripcion,
            base_legal=base_legal,
            severidad=severidad
        ))
        self.explicaciones.append(f"INCUMPLIMIENTO {severidad.upper()}: Falta {aspecto}. {descripcion} ({base_legal})")
        
        if recomendacion_texto not in self.recomendaciones_generadas:
            self.recomendaciones_generadas.append(recomendacion_texto)

        resultado_fact = self.facts.get(self.facts[1])
        if resultado_fact and resultado_fact.get('cumple_laboral'):
             self.modify(self.facts[1], cumple_laboral = False)

    def _registrar_cumplimiento(self, aspecto, descripcion):
        """Registra un cumplimiento"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto=aspecto,
            descripcion=descripcion
        ))
        self.explicaciones.append(f"CUMPLE: Se identificó {aspecto}.")


    # --- REGLAS DE EVALUACIÓN DE OBLIGACIONES CLAVE ---
    
    # 1. Contratos Escritos y Formalidad (CRÍTICO)
    @Rule(
        DocumentoNormaLaboral(tiene_contratos_escritos_vigentes=False),
        ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_contratos_escritos(self):
        """Verifica la formalización de la relación laboral (especialmente contratos modales)"""
        self._registrar_incumplimiento(
            aspecto="Contratos Escritos y Vigentes",
            descripcion="No se evidencian contratos escritos (o están vencidos/mal formalizados), lo que puede presumir un contrato a plazo indeterminado.",
            base_legal="Art. 72, D.S. 003-97-TR (LPCL)",
            severidad="crítica", 
            recomendacion_texto="Formalizar todos los contratos de trabajo, especialmente los modales, asegurando el cumplimiento de los requisitos legales y su registro."
        )

    @Rule(DocumentoNormaLaboral(tiene_contratos_escritos_vigentes=True), ResultadoEvaluacionLaboral())
    def cumple_contratos_escritos(self):
        self._registrar_cumplimiento("Contratos Escritos y Vigentes", "Se verifica la existencia y vigencia de los contratos de trabajo.")

    # 2. Registro en Planilla y Boletas de Pago (CRÍTICO)
    @Rule(
        DocumentoNormoLaboral(tiene_registro_planilla_electronica=False) |
        DocumentoNormoLaboral(entrega_boletas_pago_oportunas=False),
        ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_registro_y_boletas(self):
        """Verifica el registro en Planilla Electrónica y la entrega de boletas"""
        
        aspecto_desc = ""
        recomendacion = ""
        
        if not self.facts.get(self.facts[0]).get('tiene_registro_planilla_electronica'):
            aspecto_desc += "Falta de registro en la Planilla Electrónica (PLAME/T-Registro). "
            recomendacion = "Regularizar el registro de todos los trabajadores en la Planilla Electrónica."
        
        if not self.facts.get(self.facts[0]).get('entrega_boletas_pago_oportunas'):
            aspecto_desc += "No se evidencia la entrega oportuna de boletas de pago firmadas. "
            if recomendacion:
                recomendacion += " Y asegurar la entrega oportuna de las boletas de pago."
            else:
                recomendacion = "Asegurar la entrega oportuna de las boletas de pago."


        self._registrar_incumplimiento(
            aspecto="Formalidad Documentaria (Planilla y Boletas)",
            descripcion=aspecto_desc,
            base_legal="Ley 28806 / D.S. 003-97-TR",
            severidad="crítica",
            recomendacion_texto=recomendacion
        )

    @Rule(
        DocumentoNormaLaboral(tiene_registro_planilla_electronica=True, entrega_boletas_pago_oportunas=True), 
        ResultadoEvaluacionLaboral()
    )
    def cumple_registro_y_boletas(self):
        self._registrar_cumplimiento("Formalidad Documentaria (Planilla y Boletas)", "Se verifica el registro en Planilla Electrónica y la entrega de boletas de pago.")

    # 3. Control de Asistencia (ALTA)
    @Rule(
        DocumentoNormaLaboral(registra_control_asistencia=False),
        ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_control_asistencia(self):
        """Verifica el registro de control de asistencia, horas extra y jornada"""
        self._registrar_incumplimiento(
            aspecto="Control de Asistencia y Horas Extra",
            descripcion="No existe un sistema de control de asistencia o no se registra el sobretiempo correctamente.",
            base_legal="D.S. 004-2006-TR (Reglamento Jornada y Horario)",
            severidad="alta",
            recomendacion_texto="Implementar o formalizar el registro de control de asistencia y asegurar el pago/compensación de las horas extra."
        )

    @Rule(DocumentoNormaLaboral(registra_control_asistencia=True), ResultadoEvaluacionLaboral())
    def cumple_control_asistencia(self):
        self._registrar_cumplimiento("Control de Asistencia y Horas Extra", "Se registra el control de asistencia y jornada laboral.")

    # 4. Reglamento Interno de Trabajo (MODERADA/ALTA)
    @Rule(
        DocumentoNormaLaboral(tiene_reglamento_interno_trabajo=False), # Se asume aplicable si hay >100 trabajadores
        ResultadoEvaluacionLaboral(cumple_laboral=True)
    )
    def falta_reglamento_interno(self):
        """Verifica la existencia del Reglamento Interno de Trabajo (RIT)"""
        self._registrar_incumplimiento(
            aspecto="Reglamento Interno de Trabajo (RIT)",
            descripcion="Falta el Reglamento Interno de Trabajo, obligatorio si la empresa cuenta con 100 o más trabajadores.",
            base_legal="Art. 17, D.S. 039-91-TR (Reglamento RIT)",
            severidad="moderada", # Sube a 'alta' si el número de trabajadores es > 100
            recomendacion_texto="Elaborar e implementar el Reglamento Interno de Trabajo si cuenta con 100 o más trabajadores, y depositarlo ante la Autoridad Administrativa de Trabajo."
        )

    @Rule(DocumentoNormaLaboral(tiene_reglamento_interno_trabajo=True), ResultadoEvaluacionLaboral())
    def cumple_reglamento_interno(self):
        self._registrar_cumplimiento("Reglamento Interno de Trabajo (RIT)", "Se cuenta con Reglamento Interno de Trabajo.")
        
    # 5. Periodo de Prueba (ADICIONAL)
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


    # ------ REGLA DE SINTESIS --------

    @Rule(
        ResultadoEvaluacionLaboral(cumple_laboral = MATCH.cumple),
        salience = -100
    )
    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluacion para D.S. 003-97-TR"""
        cumplimientos = []
        incumplimientos = []
        
        for fact in self.facts.values():
            if isinstance(fact, Fact):
                if fact.get('tipo') in ['cumplimiento', 'cumplimiento_adicional']:
                    cumplimientos.append(fact.get('aspecto'))
                elif fact.get('tipo') == 'incumplimiento':
                    incumplimientos.append({
                        'aspecto': fact.get('aspecto'),
                        'descripcion': fact.get('descripcion'),
                        'base_legal': fact.get('base_legal'),
                        'severidad': fact.get('severidad')
                    })
                        
        # Modificar el resultado final
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            self.facts[1],
            cumple_laboral = cumple,
            aspectos_cumplidos = cumplimientos,
            aspectos_incumplidos = incumplimientos,
            recomendaciones = self.recomendaciones_generadas,
            explicacion = explicacion_final
        )

    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacionLaboral):
                return {
                    'cumple_laboral': fact.get('cumple_laboral'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)