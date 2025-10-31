"""
Reglas de experta para Ley N° 30424 - Responsabilidad Administrativa de Personas Jurídicas
Reglamento: D.S. N° 002-2019-JUS y modificatorias
Enfoque: Evaluación de la existencia de un Modelo de Prevención (MP) eficaz.
"""

from experta import *

class DocumentoModeloPrevencion(Fact):
    # Documento a evaluar según Ley 30424
    # Elementos Mínimos del MP para eximente de responsabilidad
    
    # 1. Compromiso y Liderazgo del Órgano de Gobierno (Art. 28.1, Reglamento)
    compromiso_organo_gobierno = Field(bool, default=False)
    
    # 2. Encargado de Prevención (Compliance Officer) (Art. 17.2.a, Ley 30424)
    tiene_encargado_prevencion = Field(bool, default=False)
    
    # 3. Identificación, evaluación y mitigación de riesgos (Art. 17.2.b, Ley 30424)
    tiene_mapa_riesgos = Field(bool, default=False)
    
    # 4. Controles Internos (Contabilidad y Finanzas) (Art. 28.2.1, Reglamento)
    tiene_controles_contables_financieros = Field(bool, default=False)
    
    # 5. Canal de Denuncia (Art. 28.2.2, Reglamento)
    tiene_canal_denuncia_proteccion = Field(bool, default=False)
    
    # 6. Procedimiento Disciplinario (Art. 28.2.2, Reglamento)
    tiene_procedimiento_disciplinario_sancion = Field(bool, default=False)
    
    # 7. Políticas de Riesgos Específicos (Buena Práctica, complementa controles)
    tiene_politicas_riesgos_especificos = Field(bool, default=False) 
    
class ResultadoEvaluacion30424(Fact):
    # Almacena Resultados de la evaluación
    cumple_mp = Field(bool, default=True) # Indica si el MP cumple los mínimos para ser eximente
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class ResponsabilidadAdministrativaKB(KnowledgeEngine):
    """Motor de inferencia para Ley 30424 - Modelo de Prevención"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
        self.recomendaciones_generadas = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluacion"""
        yield ResultadoEvaluacion30424()
    
    # --- Funciones Auxiliares para Reducir Repetición en las Reglas ---

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
        if resultado_fact and resultado_fact.get('cumple_mp'):
             # Un incumplimiento crítico invalida el Modelo de Prevención
             self.modify(self.facts[1], cumple_mp = False)

    def _registrar_cumplimiento(self, aspecto, descripcion):
        """Registra un cumplimiento"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto=aspecto,
            descripcion=descripcion
        ))
        self.explicaciones.append(f"CUMPLE: Se identificó {aspecto}.")


    # --- REGLAS DE EVALUACIÓN DE ELEMENTOS MÍNIMOS DEL MP ---
    
    # 1. Compromiso del Órgano de Gobierno (Art. 28.1, Reglamento)
    @Rule(
        DocumentoModeloPrevencion(compromiso_organo_gobierno=False),
        ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_compromiso_organo_gobierno(self):
        """Verifica el compromiso visible y liderazgo de la Alta Dirección"""
        self._registrar_incumplimiento(
            aspecto="Compromiso del Órgano de Gobierno",
            descripcion="No existe evidencia del compromiso y liderazgo visible de la alta dirección.",
            base_legal="Art. 28.1, D.S. 002-2019-JUS",
            severidad="crítica", 
            recomendacion_texto="Asegurar el compromiso y liderazgo visible del Órgano de Gobierno (ej. Declaración de compromiso, asignación de recursos)."
        )

    @Rule(DocumentoModeloPrevencion(compromiso_organo_gobierno=True), ResultadoEvaluacion30424())
    def cumple_compromiso_organo_gobierno(self):
        self._registrar_cumplimiento("Compromiso del Órgano de Gobierno", "Se evidencia el compromiso y liderazgo visible.")
    
    # 2. Encargado de Prevención (Art. 17.2.a, Ley 30424)
    @Rule(
        DocumentoModeloPrevencion(tiene_encargado_prevencion=False),
        ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_encargado_prevencion(self):
        """Verifica la designación del Encargado de Prevención (Compliance Officer)"""
        self._registrar_incumplimiento(
            aspecto="Encargado de Prevención (Compliance Officer)",
            descripcion="No se designa un Encargado de Prevención o este no cumple con los requisitos de autonomía e independencia.",
            base_legal="Art. 17.2.a, Ley 30424",
            severidad="crítica",
            recomendacion_texto="Designar formalmente un Encargado de Prevención (Oficial de Cumplimiento) con recursos y autonomía definidos."
        )

    @Rule(DocumentoModeloPrevencion(tiene_encargado_prevencion=True), ResultadoEvaluacion30424())
    def cumple_encargado_prevencion(self):
        self._registrar_cumplimiento("Encargado de Prevención (Compliance Officer)", "Se designa un Encargado de Prevención conforme a la Ley.")

    # 3. Mapa de Riesgos (Art. 17.2.b, Ley 30424)
    @Rule(
        DocumentoModeloPrevencion(tiene_mapa_riesgos=False),
        ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_mapa_riesgos(self):
        """Verifica la existencia del Mapa de Riesgos (Identificación, Evaluación y Mitigación)"""
        self._registrar_incumplimiento(
            aspecto="Identificación y Mapa de Riesgos",
            descripcion="Falta el Mapa de Riesgos que evalúe y mitigue los riesgos de comisión de delitos (Art. 17.2.b).",
            base_legal="Art. 17.2.b, Ley 30424",
            severidad="crítica",
            recomendacion_texto="Elaborar un Mapa de Riesgos actualizado que identifique procesos vulnerables a los delitos de la Ley 30424."
        )

    @Rule(DocumentoModeloPrevencion(tiene_mapa_riesgos=True), ResultadoEvaluacion30424())
    def cumple_mapa_riesgos(self):
        self._registrar_cumplimiento("Identificación y Mapa de Riesgos", "Se cuenta con un Mapa de Riesgos documentado.")

    # 4. Controles Contables y Financieros (Art. 28.2.1, Reglamento)
    @Rule(
        DocumentoModeloPrevencion(tiene_controles_contables_financieros=False),
        ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_controles_contables(self):
        """Verifica la implementación de controles contables y financieros para prevenir ocultamiento"""
        self._registrar_incumplimiento(
            aspecto="Sistema de Control Contable y Financiero",
            descripcion="No se evidencian controles internos que aseguren el registro completo y veraz de todas las transacciones.",
            base_legal="Art. 28.2.1, Reglamento",
            severidad="alta",
            recomendacion_texto="Implementar procedimientos de control contable y financiero que garanticen la trazabilidad de operaciones."
        )

    @Rule(DocumentoModeloPrevencion(tiene_controles_contables_financieros=True), ResultadoEvaluacion30424())
    def cumple_controles_contables(self):
        self._registrar_cumplimiento("Sistema de Control Contable y Financiero", "Se implementaron controles contables y financieros.")

    # 5. Canal de Denuncia (Art. 28.2.2, Reglamento)
    @Rule(
        DocumentoModeloPrevencion(tiene_canal_denuncia_proteccion=False),
        ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_canal_denuncia(self):
        """Verifica la existencia de un Canal de Denuncia confidencial y procedimientos de protección"""
        self._registrar_incumplimiento(
            aspecto="Canal de Denuncia y Protección",
            descripcion="No se implementó un canal de denuncia confidencial ni mecanismos de protección contra represalias.",
            base_legal="Art. 28.2.2, Reglamento",
            severidad="alta",
            recomendacion_texto="Establecer un Canal de Denuncia seguro y confidencial. Documentar los procedimientos para investigar y proteger al denunciante."
        )

    @Rule(DocumentoModeloPrevencion(tiene_canal_denuncia_proteccion=True), ResultadoEvaluacion30424())
    def cumple_canal_denuncia(self):
        self._registrar_cumplimiento("Canal de Denuncia y Protección", "Se identificó un Canal de Denuncia y mecanismos de protección.")
        
    # 6. Procedimiento Disciplinario (Art. 28.2.2, Reglamento)
    @Rule(
        DocumentoModeloPrevencion(tiene_procedimiento_disciplinario_sancion=False),
        ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_procedimiento_disciplinario(self):
        """Verifica la existencia de un Procedimiento Disciplinario y Régimen Sancionador"""
        self._registrar_incumplimiento(
            aspecto="Régimen Sancionador y Disciplinario",
            descripcion="No existe un régimen sancionador ni un procedimiento disciplinario claro para el incumplimiento del MP.",
            base_legal="Art. 28.2.2, Reglamento",
            severidad="alta",
            recomendacion_texto="Formalizar un régimen disciplinario y sancionador para las violaciones a los códigos y al Modelo de Prevención."
        )

    @Rule(DocumentoModeloPrevencion(tiene_procedimiento_disciplinario_sancion=True), ResultadoEvaluacion30424())
    def cumple_procedimiento_disciplinario(self):
        self._registrar_cumplimiento("Régimen Sancionador y Disciplinario", "Se evidencian procedimientos disciplinarios y sanciones.")
        
    # --- REGLA ADICIONAL (Buena Práctica / Detalle del Reglamento) ---
    @Rule(
        DocumentoModeloPrevencion(tiene_politicas_riesgos_especificos=True),
        ResultadoEvaluacion30424()
    )
    def tiene_politicas_riesgos_especificos_adicional(self):
        """Valora positivamente la existencia de políticas en áreas de riesgo específicas (ej. regalos, donaciones)"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Políticas de Riesgo Específico",
            descripcion="Se cuenta con políticas para áreas de alto riesgo (ej. regalos, hospitalidad, donaciones, etc.)"
        ))
        self.explicaciones.append("BUENA PRÁCTICA: Se implementaron políticas para gestionar riesgos específicos (ej. regalos y hospitalidad).")


    # ------ REGLA DE SINTESIS --------

    @Rule(
        ResultadoEvaluacion30424(cumple_mp = MATCH.cumple),
        salience = -100
    )
    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluacion para Ley 30424"""
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
            cumple_mp = cumple,
            aspectos_cumplidos = cumplimientos,
            aspectos_incumplidos = incumplimientos,
            recomendaciones = self.recomendaciones_generadas,
            explicacion = explicacion_final
        )

    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacion30424):
                return {
                    'cumple_mp': fact.get('cumple_mp'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)