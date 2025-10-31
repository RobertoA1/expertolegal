# -*- coding: utf-8 -*-
"""
Reglas de experta para Ley N° 30424 - Responsabilidad Administrativa de Personas Jurídicas
Reglamento: D.S. N° 002-2019-JUS y modificatorias
Enfoque: Evaluación de la existencia de un Modelo de Prevención (MP) eficaz.
VERSIÓN CORREGIDA - Sin bucles infinitos
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
    cumple_mp = Field(bool, default=True)
    aspectos_cumplidos = Field(list, mandatory=False)
    aspectos_incumplidos = Field(list, mandatory=False)
    recomendaciones = Field(list, mandatory=False)
    explicacion = Field(str, default="")

class ResponsabilidadAdministrativaKB(KnowledgeEngine):
    """Motor de inferencia para Ley 30424 - Modelo de Prevención - VERSIÓN CORREGIDA"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    # ============= REGLAS DE EVALUACIÓN CORREGIDAS =============
    
    @Rule(
        DocumentoModeloPrevencion(compromiso_organo_gobierno=False),
        AS.resultado << ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_compromiso_organo_gobierno(self, resultado):
        """Verifica el compromiso visible y liderazgo de la Alta Dirección"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Compromiso del Órgano de Gobierno",
            descripcion="No existe evidencia del compromiso y liderazgo visible de la alta dirección.",
            base_legal="Art. 28.1, D.S. 002-2019-JUS",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Compromiso del Órgano de Gobierno. "
            "No existe evidencia del compromiso y liderazgo visible de la alta dirección. "
            "(Art. 28.1, D.S. 002-2019-JUS)"
        )
        
        self.modify(resultado, cumple_mp=False)

    @Rule(
        DocumentoModeloPrevencion(compromiso_organo_gobierno=True),
        ResultadoEvaluacion30424()
    )
    def cumple_compromiso_organo_gobierno(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Compromiso del Órgano de Gobierno",
            descripcion="Se evidencia el compromiso y liderazgo visible."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Compromiso del Órgano de Gobierno.")
    
    @Rule(
        DocumentoModeloPrevencion(tiene_encargado_prevencion=False),
        AS.resultado << ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_encargado_prevencion(self, resultado):
        """Verifica la designación del Encargado de Prevención (Compliance Officer)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Encargado de Prevención (Compliance Officer)",
            descripcion="No se designa un Encargado de Prevención o este no cumple con los requisitos de autonomía e independencia.",
            base_legal="Art. 17.2.a, Ley 30424",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Encargado de Prevención (Compliance Officer). "
            "No se designa un Encargado de Prevención o este no cumple con los requisitos de autonomía e independencia. "
            "(Art. 17.2.a, Ley 30424)"
        )
        
        self.modify(resultado, cumple_mp=False)

    @Rule(
        DocumentoModeloPrevencion(tiene_encargado_prevencion=True),
        ResultadoEvaluacion30424()
    )
    def cumple_encargado_prevencion(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Encargado de Prevención (Compliance Officer)",
            descripcion="Se designa un Encargado de Prevención conforme a la Ley."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Encargado de Prevención (Compliance Officer).")

    @Rule(
        DocumentoModeloPrevencion(tiene_mapa_riesgos=False),
        AS.resultado << ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_mapa_riesgos(self, resultado):
        """Verifica la existencia del Mapa de Riesgos (Identificación, Evaluación y Mitigación)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Identificación y Mapa de Riesgos",
            descripcion="Falta el Mapa de Riesgos que evalúe y mitigue los riesgos de comisión de delitos (Art. 17.2.b).",
            base_legal="Art. 17.2.b, Ley 30424",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Identificación y Mapa de Riesgos. "
            "Falta el Mapa de Riesgos que evalúe y mitigue los riesgos de comisión de delitos (Art. 17.2.b). "
            "(Art. 17.2.b, Ley 30424)"
        )
        
        self.modify(resultado, cumple_mp=False)

    @Rule(
        DocumentoModeloPrevencion(tiene_mapa_riesgos=True),
        ResultadoEvaluacion30424()
    )
    def cumple_mapa_riesgos(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Identificación y Mapa de Riesgos",
            descripcion="Se cuenta con un Mapa de Riesgos documentado."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Identificación y Mapa de Riesgos.")

    @Rule(
        DocumentoModeloPrevencion(tiene_controles_contables_financieros=False),
        AS.resultado << ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_controles_contables(self, resultado):
        """Verifica la implementación de controles contables y financieros para prevenir ocultamiento"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Sistema de Control Contable y Financiero",
            descripcion="No se evidencian controles internos que aseguren el registro completo y veraz de todas las transacciones.",
            base_legal="Art. 28.2.1, Reglamento",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Sistema de Control Contable y Financiero. "
            "No se evidencian controles internos que aseguren el registro completo y veraz de todas las transacciones. "
            "(Art. 28.2.1, Reglamento)"
        )
        
        self.modify(resultado, cumple_mp=False)

    @Rule(
        DocumentoModeloPrevencion(tiene_controles_contables_financieros=True),
        ResultadoEvaluacion30424()
    )
    def cumple_controles_contables(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Sistema de Control Contable y Financiero",
            descripcion="Se implementaron controles contables y financieros."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Sistema de Control Contable y Financiero.")

    @Rule(
        DocumentoModeloPrevencion(tiene_canal_denuncia_proteccion=False),
        AS.resultado << ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_canal_denuncia(self, resultado):
        """Verifica la existencia de un Canal de Denuncia confidencial y procedimientos de protección"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Canal de Denuncia y Protección",
            descripcion="No se implementó un canal de denuncia confidencial ni mecanismos de protección contra represalias.",
            base_legal="Art. 28.2.2, Reglamento",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Canal de Denuncia y Protección. "
            "No se implementó un canal de denuncia confidencial ni mecanismos de protección contra represalias. "
            "(Art. 28.2.2, Reglamento)"
        )
        
        self.modify(resultado, cumple_mp=False)

    @Rule(
        DocumentoModeloPrevencion(tiene_canal_denuncia_proteccion=True),
        ResultadoEvaluacion30424()
    )
    def cumple_canal_denuncia(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Canal de Denuncia y Protección",
            descripcion="Se identificó un Canal de Denuncia y mecanismos de protección."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Canal de Denuncia y Protección.")
        
    @Rule(
        DocumentoModeloPrevencion(tiene_procedimiento_disciplinario_sancion=False),
        AS.resultado << ResultadoEvaluacion30424(cumple_mp=True)
    )
    def falta_procedimiento_disciplinario(self, resultado):
        """Verifica la existencia de un Procedimiento Disciplinario y Régimen Sancionador"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Régimen Sancionador y Disciplinario",
            descripcion="No existe un régimen sancionador ni un procedimiento disciplinario claro para el incumplimiento del MP.",
            base_legal="Art. 28.2.2, Reglamento",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Régimen Sancionador y Disciplinario. "
            "No existe un régimen sancionador ni un procedimiento disciplinario claro para el incumplimiento del MP. "
            "(Art. 28.2.2, Reglamento)"
        )
        
        self.modify(resultado, cumple_mp=False)

    @Rule(
        DocumentoModeloPrevencion(tiene_procedimiento_disciplinario_sancion=True),
        ResultadoEvaluacion30424()
    )
    def cumple_procedimiento_disciplinario(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Régimen Sancionador y Disciplinario",
            descripcion="Se evidencian procedimientos disciplinarios y sanciones."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Régimen Sancionador y Disciplinario.")
        
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

    # ============= REGLA DE SÍNTESIS CORREGIDA =============
    
    @Rule(
        AS.resultado << ResultadoEvaluacion30424(cumple_mp=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),
        salience=-1000
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluacion para Ley 30424 - VERSIÓN CORREGIDA"""
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
            if 'Compromiso' in aspecto:
                recomendaciones.append("Asegurar el compromiso y liderazgo visible del Órgano de Gobierno (ej. Declaración de compromiso, asignación de recursos).")
            elif 'Encargado de Prevención' in aspecto:
                recomendaciones.append("Designar formalmente un Encargado de Prevención (Oficial de Cumplimiento) con recursos y autonomía definidos.")
            elif 'Mapa de Riesgos' in aspecto:
                recomendaciones.append("Elaborar un Mapa de Riesgos actualizado que identifique procesos vulnerables a los delitos de la Ley 30424.")
            elif 'Control Contable' in aspecto:
                recomendaciones.append("Implementar procedimientos de control contable y financiero que garanticen la trazabilidad de operaciones.")
            elif 'Canal de Denuncia' in aspecto:
                recomendaciones.append("Establecer un Canal de Denuncia seguro y confidencial. Documentar los procedimientos para investigar y proteger al denunciante.")
            elif 'Régimen Sancionador' in aspecto:
                recomendaciones.append("Formalizar un régimen disciplinario y sancionador para las violaciones a los códigos y al Modelo de Prevención.")
        
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            resultado,
            cumple_mp=cumple,
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
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacion30424':
                    return {
                        'cumple_mp': fact.get('cumple_mp', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Fallback si no encuentra resultados
            return {
                'cumple_mp': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
            return {
                'cumple_mp': False,
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