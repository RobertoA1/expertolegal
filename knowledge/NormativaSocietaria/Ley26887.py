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
    cumple_societario = Field(bool, default=True) # Cumple con las obligaciones societarias formales
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class NormativaSocietariaKB(KnowledgeEngine):
    """Motor de inferencia para Ley 26887 - Ley General de Sociedades"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
        self.recomendaciones_generadas = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluacion"""
        yield ResultadoEvaluacionSocietaria()
    
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
        if resultado_fact and resultado_fact.get('cumple_societario'):
             self.modify(self.facts[1], cumple_societario = False)

    def _registrar_cumplimiento(self, aspecto, descripcion):
        """Registra un cumplimiento"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto=aspecto,
            descripcion=descripcion
        ))
        self.explicaciones.append(f"CUMPLE: Se identificó {aspecto}.")


    # --- REGLAS DE EVALUACIÓN DE OBLIGACIONES CLAVE ---
    
    # 1. Formalidad de la Constitución e Inscripción (CRÍTICO)
    @Rule(
        DocumentoSocietario(esta_constituida_escritura_publica=False) |
        DocumentoSocietario(esta_inscrita_registros_publicos=False),
        ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_formalidad_e_inscripcion(self):
        """Verifica que la sociedad esté constituida por EP e inscrita en Registros Públicos"""
        
        descripcion = ""
        if not self.facts.get(self.facts[0]).get('esta_constituida_escritura_publica'):
            descripcion += "No existe Escritura Pública de Constitución. "
        if not self.facts.get(self.facts[0]).get('esta_inscrita_registros_publicos'):
            descripcion += "La sociedad no está inscrita en Registros Públicos. "
            
        self._registrar_incumplimiento(
            aspecto="Inscripción Registral",
            descripcion=descripcion.strip(),
            base_legal="Art. 5 y Art. 9, Ley 26887",
            severidad="crítica", 
            recomendacion_texto="Asegurar que la Escritura Pública de Constitución esté debidamente inscrita en la SUNARP para adquirir personalidad jurídica plena."
        )

    @Rule(
        DocumentoSocietario(esta_constituida_escritura_publica=True, esta_inscrita_registros_publicos=True), 
        ResultadoEvaluacionSocietaria()
    )
    def cumple_formalidad_e_inscripcion(self):
        self._registrar_cumplimiento("Inscripción Registral", "Se verificó la constitución por EP y la inscripción en Registros Públicos.")

    # 2. Pluralidad de Socios (CRÍTICO)
    @Rule(
        DocumentoSocietario(mantiene_pluralidad_socios=False),
        ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_pluralidad_socios(self):
        """Verifica que la sociedad mantenga el mínimo de dos socios"""
        self._registrar_incumplimiento(
            aspecto="Pluralidad de Socios",
            descripcion="La sociedad opera con un único socio, lo que constituye causal de disolución si no se reconstituye en 6 meses.",
            base_legal="Art. 4, Ley 26887",
            severidad="crítica",
            recomendacion_texto="Reconstituir la pluralidad de socios (mínimo 2) o iniciar la disolución/liquidación, o en su defecto, transformarse en una EIRL si es aplicable."
        )

    @Rule(DocumentoSocietario(mantiene_pluralidad_socios=True), ResultadoEvaluacionSocietaria())
    def cumple_pluralidad_socios(self):
        self._registrar_cumplimiento("Pluralidad de Socios", "La sociedad mantiene el mínimo de dos socios.")

    # 3. Libros Societarios Obligatorios (ALTA)
    @Rule(
        DocumentoSocietario(tiene_libro_actas_junta_general=False) |
        DocumentoSocietario(tiene_libro_matricula_acciones=False),
        ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_libros_obligatorios(self):
        """Verifica la existencia de los libros societarios principales (Actas y Matrícula)"""
        
        descripcion = ""
        recomendacion = ""
        
        if not self.facts.get(self.facts[0]).get('tiene_libro_actas_junta_general'):
            descripcion += "Falta el Libro de Actas de Junta General de Accionistas. "
            
        if not self.facts.get(self.facts[0]).get('tiene_libro_matricula_acciones'):
            descripcion += "Falta el Libro de Matrícula de Acciones. "
        
        recomendacion = "Legalizar y mantener actualizados el Libro de Actas de Junta General y el Libro de Matrícula de Acciones."

        self._registrar_incumplimiento(
            aspecto="Libros Societarios Obligatorios",
            descripcion=descripcion.strip(),
            base_legal="Art. 114 y 245, Ley 26887",
            severidad="alta",
            recomendacion_texto=recomendacion
        )

    @Rule(
        DocumentoSocietario(tiene_libro_actas_junta_general=True, tiene_libro_matricula_acciones=True), 
        ResultadoEvaluacionSocietaria()
    )
    def cumple_libros_obligatorios(self):
        self._registrar_cumplimiento("Libros Societarios Obligatorios (Actas y Matrícula)", "Se cuenta con los libros obligatorios principales.")

    # 4. Aportes de Capital (MODERADA/ALTA)
    @Rule(
        DocumentoSocietario(capital_suscrito_totalmente=False) |
        DocumentoSocietario(capital_pagado_minimo=False),
        ResultadoEvaluacionSocietaria(cumple_societario=True)
    )
    def falta_capital_minimo(self):
        """Verifica el cumplimiento de los requisitos de suscripción y pago mínimo del capital"""
        
        descripcion = ""
        if not self.facts.get(self.facts[0]).get('capital_suscrito_totalmente'):
            descripcion += "El capital no está suscrito en su totalidad. "
        if not self.facts.get(self.facts[0]).get('capital_pagado_minimo'):
            descripcion += "No se ha pagado el mínimo del 25% del valor nominal de cada acción suscrita."
            
        self._registrar_incumplimiento(
            aspecto="Suscripción y Pago del Capital",
            descripcion=descripcion.strip(),
            base_legal="Art. 52, Ley 26887",
            severidad="alta",
            recomendacion_texto="Regularizar la suscripción total del capital y asegurar el desembolso mínimo del 25%."
        )

    @Rule(
        DocumentoSocietario(capital_suscrito_totalmente=True, capital_pagado_minimo=True), 
        ResultadoEvaluacionSocietaria()
    )
    def cumple_capital_minimo(self):
        self._registrar_cumplimiento("Suscripción y Pago del Capital", "Se cumple con los requisitos de suscripción y pago mínimo del capital.")


    # ------ REGLA DE SINTESIS --------

    @Rule(
        ResultadoEvaluacionSocietaria(cumple_societario = MATCH.cumple),
        salience = -100
    )
    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluacion para Ley 26887"""
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
            cumple_societario = cumple,
            aspectos_cumplidos = cumplimientos,
            aspectos_incumplidos = incumplimientos,
            recomendaciones = self.recomendaciones_generadas,
            explicacion = explicacion_final
        )

    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacionSocietaria):
                return {
                    'cumple_societario': fact.get('cumple_societario'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)