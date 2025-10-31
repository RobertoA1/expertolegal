"""
Reglas de experta para Ley N° 26887 - Ley General de Sociedades (LGS)
Enfoque: Formalidad del acto constitutivo, capital y libros societarios obligatorios.
"""

from experta import *

class DocumentoSocietario(Fact):
    # Documento a evaluar (ej. Minuta, Escritura Pública, Libro de Actas, Matrícula de Acciones)
    
    # 1. Formalidad Constitutiva (Art. 5, 20)
    esta_constituida_escritura_publica = Field(bool, default=False)
    esta_inscrita_registros_publicos = Field(bool, default=False)
    tiene_estatuto_actualizado = Field(bool, default=False)
    
    # 2. Capital y Aportes (Art. 52, 72)
    capital_suscrito_totalmente = Field(bool, default=False)
    capital_pagado_minimo = Field(bool, default=False) # Mínimo 25% de cada acción suscrita
    
    # 3. Pluralidad de Socios (Art. 4)
    mantiene_pluralidad_socios = Field(bool, default=False) # Mínimo 2 socios (salvo excepciones)
    
    # 4. Libros Societarios Obligatorios (Ejemplo: S.A. o S.A.C. - Art. 114, 245)
    tiene_libro_actas_junta_general = Field(bool, default=False)
    tiene_libro_matricula_acciones = Field(bool, default=False) # Si es S.A. o S.A.C.
    tiene_libro_actas_directorio = Field(bool, default=False) # Si tiene Directorio
    
class ResultadoEvaluacionSocietaria(Fact):
    # Almacena Resultados de la evaluación de Ley 26887
    cumple_societario = Field(bool, default=True)
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class NormativaSocietariaKB(KnowledgeEngine):
    """Motor de inferencia para Ley 26887 - Ley General de Sociedades - VERSIÓN CORREGIDA"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    @DefFacts()
    def _inicializar(self):
        yield ResultadoEvaluacionSocietaria()

    # ============= REGLAS DE EVALUACIÓN CORREGIDAS =============
    
    # 1. Constitución por Escritura Pública (CRÍTICO)
    @Rule(
        DocumentoSocietario(esta_constituida_escritura_publica=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_escritura_publica(self, resultado):
        """Verifica que la sociedad esté constituida por Escritura Pública"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Constitución por Escritura Pública",
            descripcion="La sociedad no está constituida mediante Escritura Pública.",
            base_legal="Art. 5, Ley 26887",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Constitución por Escritura Pública. "
            "La sociedad no está constituida mediante Escritura Pública. "
            "(Art. 5, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(esta_constituida_escritura_publica=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_escritura_publica(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Constitución por Escritura Pública",
            descripcion="La sociedad está constituida mediante Escritura Pública."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Constitución por Escritura Pública.")

    # 2. Inscripción en Registros Públicos (CRÍTICO)
    @Rule(
        DocumentoSocietario(esta_inscrita_registros_publicos=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_inscripcion_registral(self, resultado):
        """Verifica la inscripción en SUNARP"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Inscripción en Registros Públicos",
            descripcion="La sociedad no está inscrita en los Registros Públicos.",
            base_legal="Art. 9, Ley 26887",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Inscripción en Registros Públicos. "
            "La sociedad no está inscrita en los Registros Públicos. "
            "(Art. 9, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(esta_inscrita_registros_publicos=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_inscripcion_registral(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Inscripción en Registros Públicos",
            descripcion="La sociedad está inscrita en SUNARP."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Inscripción en Registros Públicos.")

    # 3. Pluralidad de Socios (CRÍTICO)
    @Rule(
        DocumentoSocietario(mantiene_pluralidad_socios=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_pluralidad_socios(self, resultado):
        """Verifica que la sociedad mantenga el mínimo de dos socios"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Pluralidad de Socios",
            descripcion="La sociedad opera con un único socio, lo que constituye causal de disolución.",
            base_legal="Art. 4, Ley 26887",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Pluralidad de Socios. "
            "La sociedad opera con un único socio, lo que constituye causal de disolución. "
            "(Art. 4, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(mantiene_pluralidad_socios=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_pluralidad_socios(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Pluralidad de Socios",
            descripcion="La sociedad mantiene el mínimo de dos socios."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Pluralidad de Socios.")

    # 4. Libro de Actas de Junta General (ALTA)
    @Rule(
        DocumentoSocietario(tiene_libro_actas_junta_general=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_libro_actas(self, resultado):
        """Verifica la existencia del Libro de Actas de Junta General"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Libro de Actas de Junta General",
            descripcion="Falta el Libro de Actas de Junta General de Accionistas.",
            base_legal="Art. 114, Ley 26887",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Libro de Actas de Junta General. "
            "Falta el Libro de Actas de Junta General de Accionistas. "
            "(Art. 114, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(tiene_libro_actas_junta_general=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_libro_actas(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Libro de Actas de Junta General",
            descripcion="Se cuenta con Libro de Actas de Junta General."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Libro de Actas de Junta General.")

    # 5. Libro de Matrícula de Acciones (ALTA)
    @Rule(
        DocumentoSocietario(tiene_libro_matricula_acciones=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_libro_matricula(self, resultado):
        """Verifica la existencia del Libro de Matrícula de Acciones"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Libro de Matrícula de Acciones",
            descripcion="Falta el Libro de Matrícula de Acciones.",
            base_legal="Art. 245, Ley 26887",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Libro de Matrícula de Acciones. "
            "Falta el Libro de Matrícula de Acciones. "
            "(Art. 245, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(tiene_libro_matricula_acciones=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_libro_matricula(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Libro de Matrícula de Acciones",
            descripcion="Se cuenta con Libro de Matrícula de Acciones."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Libro de Matrícula de Acciones.")

    # 6. Capital Suscrito Totalmente (ALTA)
    @Rule(
        DocumentoSocietario(capital_suscrito_totalmente=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_capital_suscrito(self, resultado):
        """Verifica la suscripción total del capital"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Capital Suscrito Totalmente",
            descripcion="El capital no está suscrito en su totalidad.",
            base_legal="Art. 52, Ley 26887",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Capital Suscrito Totalmente. "
            "El capital no está suscrito en su totalidad. "
            "(Art. 52, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(capital_suscrito_totalmente=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_capital_suscrito(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Capital Suscrito Totalmente",
            descripcion="El capital está suscrito en su totalidad."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Capital Suscrito Totalmente.")

    # 7. Capital Pagado Mínimo (ALTA)
    @Rule(
        DocumentoSocietario(capital_pagado_minimo=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_capital_pagado(self, resultado):
        """Verifica el pago mínimo del 25% del capital"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Capital Pagado Mínimo (25%)",
            descripcion="No se ha pagado el mínimo del 25% del valor nominal de cada acción suscrita.",
            base_legal="Art. 52, Ley 26887",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Capital Pagado Mínimo (25%). "
            "No se ha pagado el mínimo del 25% del valor nominal de cada acción suscrita. "
            "(Art. 52, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(capital_pagado_minimo=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_capital_pagado(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Capital Pagado Mínimo (25%)",
            descripcion="Se cumple con el pago mínimo del 25% del capital."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Capital Pagado Mínimo (25%).")

    # 8. Libro de Actas de Directorio (MODERADA)
    @Rule(
        DocumentoSocietario(tiene_libro_actas_directorio=False),
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_libro_directorio(self, resultado):
        """Verifica la existencia del Libro de Actas de Directorio (si aplica)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Libro de Actas de Directorio",
            descripcion="Falta el Libro de Actas de Directorio.",
            base_legal="Art. 161, Ley 26887",
            severidad="moderada"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Libro de Actas de Directorio. "
            "Falta el Libro de Actas de Directorio. "
            "(Art. 161, Ley 26887)"
        )
        
        self.modify(resultado, cumple_societario=False)

    @Rule(
        DocumentoSocietario(tiene_libro_actas_directorio=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_libro_directorio(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Libro de Actas de Directorio",
            descripcion="Se cuenta con Libro de Actas de Directorio."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Libro de Actas de Directorio.")

    # 9. Estatutos Actualizados (ADICIONAL)
    @Rule(
        DocumentoSocietario(tiene_estatuto_actualizado=True),
        ResultadoEvaluacionSocietaria()
    )
    def cumple_estatutos_actualizados(self):
        """Valora la actualización de estatutos"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Estatutos Actualizados",
            descripcion="Los estatutos sociales están actualizados."
        ))
        self.explicaciones.append("BUENA PRÁCTICA: Se cuenta con estatutos actualizados.")

    # ============= REGLA DE SÍNTESIS CORREGIDA =============
    
    @Rule(
        AS.resultado << ResultadoEvaluacionSocietaria(cumple_societario=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),
        salience=-1000
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluacion para Ley 26887 - VERSIÓN CORREGIDA"""
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
            if 'Escritura Pública' in aspecto:
                recomendaciones.append("Constituir la sociedad mediante Escritura Pública ante notario.")
            elif 'Inscripción' in aspecto:
                recomendaciones.append("Inscribir la sociedad en los Registros Públicos (SUNARP) para adquirir personalidad jurídica.")
            elif 'Pluralidad' in aspecto:
                recomendaciones.append("Reconstituir la pluralidad de socios (mínimo 2) o transformarse en EIRL.")
            elif 'Libro de Actas' in aspecto and 'Directorio' not in aspecto:
                recomendaciones.append("Legalizar y mantener actualizado el Libro de Actas de Junta General.")
            elif 'Matrícula' in aspecto:
                recomendaciones.append("Legalizar y mantener actualizado el Libro de Matrícula de Acciones.")
            elif 'Capital Suscrito' in aspecto:
                recomendaciones.append("Regularizar la suscripción total del capital social.")
            elif 'Capital Pagado' in aspecto:
                recomendaciones.append("Asegurar el pago mínimo del 25% del valor nominal de cada acción suscrita.")
            elif 'Directorio' in aspecto:
                recomendaciones.append("Legalizar y mantener actualizado el Libro de Actas de Directorio.")
        
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            resultado,
            cumple_societario=cumple,
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
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacionSocietaria':
                    return {
                        'cumple_societario': fact.get('cumple_societario', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Fallback si no encuentra resultados
            return {
                'cumple_societario': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
            return {
                'cumple_societario': False,
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