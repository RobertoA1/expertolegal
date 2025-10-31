"""
Reglas de experta para D.S. N° 133-2013-EF - Texto Único Ordenado del Código Tributario (TUO CT)
Enfoque: Libros y Registros Contables, Comprobantes de Pago y Declaraciones Juradas.
"""

from experta import *

class DocumentoTributario(Fact):
    # Documento a evaluar (ej. Libros Contables, Declaraciones, Comprobantes de Pago)
    
    # 1. Libros y Registros Contables (Art. 87 TUO CT)
    tiene_libros_obligatorios_vigentes = Field(bool, default=False)
    libros_cumplen_plazo_maximo_atraso = Field(bool, default=False)
    
    # 2. Comprobantes de Pago (Art. 87 TUO CT)
    emite_comprobantes_pago_por_ventas = Field(bool, default=False)
    comprobantes_sustentan_costo_gasto = Field(bool, default=False)
    
    # 3. Declaraciones Juradas (Art. 87 TUO CT)
    presenta_declaracion_jurada_mensual = Field(bool, default=False) # IGV/Renta
    presenta_declaracion_jurada_anual = Field(bool, default=False) # Renta Anual
    
    # 4. Domicilio Fiscal (Art. 11 TUO CT)
    domicilio_fiscal_comunicado_sunat = Field(bool, default=False)

class ResultadoEvaluacionTributaria(Fact):
    # Almacena Resultados de la evaluación Tributaria
    cumple_tributario = Field(bool, default=True)
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class NormativaTributariaKB(KnowledgeEngine):
    """Motor de inferencia para D.S. 133-2013-EF - Código Tributario - VERSIÓN CORREGIDA"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    @DefFacts()
    def _inicializar(self):
        yield ResultadoEvaluacionTributaria()

    # ============= REGLAS DE EVALUACIÓN CORREGIDAS =============
    
    # 1. Libros Contables Obligatorios (CRÍTICO)
    @Rule(
        DocumentoTributario(tiene_libros_obligatorios_vigentes=False),
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_libros_obligatorios(self, resultado):
        """Verifica el llevado de libros obligatorios"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Libros Contables Obligatorios",
            descripcion="No se llevan los libros y registros contables obligatorios según el régimen tributario.",
            base_legal="Art. 87.7, TUO CT / R.S. 234-2006/SUNAT",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Libros Contables Obligatorios. "
            "No se llevan los libros y registros contables obligatorios según el régimen tributario. "
            "(Art. 87.7, TUO CT)"
        )
        
        self.modify(resultado, cumple_tributario=False)

    @Rule(
        DocumentoTributario(tiene_libros_obligatorios_vigentes=True),
        ResultadoEvaluacionTributaria()
    )
    def cumple_libros_obligatorios(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Libros Contables Obligatorios",
            descripcion="Se llevan los libros contables obligatorios."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Libros Contables Obligatorios.")

    # 2. Plazo Máximo de Atraso en Libros (CRÍTICO)
    @Rule(
        DocumentoTributario(libros_cumplen_plazo_maximo_atraso=False),
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_plazo_atraso_libros(self, resultado):
        """Verifica que los libros estén dentro del plazo máximo de atraso"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Plazo Máximo de Atraso en Libros",
            descripcion="Los libros obligatorios están atrasados más allá del plazo máximo permitido por SUNAT.",
            base_legal="R.S. 234-2006/SUNAT",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Plazo Máximo de Atraso en Libros. "
            "Los libros obligatorios están atrasados más allá del plazo máximo permitido por SUNAT. "
            "(R.S. 234-2006/SUNAT)"
        )
        
        self.modify(resultado, cumple_tributario=False)

    @Rule(
        DocumentoTributario(libros_cumplen_plazo_maximo_atraso=True),
        ResultadoEvaluacionTributaria()
    )
    def cumple_plazo_atraso_libros(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Plazo Máximo de Atraso en Libros",
            descripcion="Los libros contables están actualizados dentro del plazo permitido."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Plazo Máximo de Atraso en Libros.")

    # 3. Emisión de Comprobantes de Pago (CRÍTICO)
    @Rule(
        DocumentoTributario(emite_comprobantes_pago_por_ventas=False),
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_emision_comprobantes(self, resultado):
        """Verifica la emisión de comprobantes de pago por ventas"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Emisión de Comprobantes de Pago",
            descripcion="No se emiten comprobantes de pago por todas las ventas u operaciones gravadas.",
            base_legal="Art. 87.8, TUO CT",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Emisión de Comprobantes de Pago. "
            "No se emiten comprobantes de pago por todas las ventas u operaciones gravadas. "
            "(Art. 87.8, TUO CT)"
        )
        
        self.modify(resultado, cumple_tributario=False)

    @Rule(
        DocumentoTributario(emite_comprobantes_pago_por_ventas=True),
        ResultadoEvaluacionTributaria()
    )
    def cumple_emision_comprobantes(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Emisión de Comprobantes de Pago",
            descripcion="Se emiten comprobantes de pago por todas las operaciones."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Emisión de Comprobantes de Pago.")

    # 4. Sustento de Costos y Gastos (CRÍTICO)
    @Rule(
        DocumentoTributario(comprobantes_sustentan_costo_gasto=False),
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_sustento_comprobantes(self, resultado):
        """Verifica el sustento de costos y gastos con comprobantes"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Sustento de Costos y Gastos con Comprobantes",
            descripcion="Falta sustento con Comprobantes de Pago válidos para gastos y costos.",
            base_legal="Art. 87.8, TUO CT",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Sustento de Costos y Gastos con Comprobantes. "
            "Falta sustento con Comprobantes de Pago válidos para gastos y costos. "
            "(Art. 87.8, TUO CT)"
        )
        
        self.modify(resultado, cumple_tributario=False)

    @Rule(
        DocumentoTributario(comprobantes_sustentan_costo_gasto=True),
        ResultadoEvaluacionTributaria()
    )
    def cumple_sustento_comprobantes(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Sustento de Costos y Gastos con Comprobantes",
            descripcion="Se sustentan costos y gastos con comprobantes válidos."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Sustento de Costos y Gastos con Comprobantes.")

    # 5. Declaración Jurada Mensual (ALTA)
    @Rule(
        DocumentoTributario(presenta_declaracion_jurada_mensual=False),
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_declaracion_mensual(self, resultado):
        """Verifica la presentación de declaraciones juradas mensuales"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Declaración Jurada Mensual",
            descripcion="Falta presentar las declaraciones juradas mensuales (IGV/Renta) en el plazo establecido.",
            base_legal="Art. 79, TUO Ley Impuesto a la Renta",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Declaración Jurada Mensual. "
            "Falta presentar las declaraciones juradas mensuales (IGV/Renta) en el plazo establecido. "
            "(Art. 79, TUO Ley Impuesto a la Renta)"
        )
        
        self.modify(resultado, cumple_tributario=False)

    @Rule(
        DocumentoTributario(presenta_declaracion_jurada_mensual=True),
        ResultadoEvaluacionTributaria()
    )
    def cumple_declaracion_mensual(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Declaración Jurada Mensual",
            descripcion="Se presentan las declaraciones juradas mensuales."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Declaración Jurada Mensual.")

    # 6. Declaración Jurada Anual (ALTA)
    @Rule(
        DocumentoTributario(presenta_declaracion_jurada_anual=False),
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_declaracion_anual(self, resultado):
        """Verifica la presentación de declaración jurada anual"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Declaración Jurada Anual",
            descripcion="Falta presentar la Declaración Jurada Anual del Impuesto a la Renta.",
            base_legal="Art. 87.1, TUO CT",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Declaración Jurada Anual. "
            "Falta presentar la Declaración Jurada Anual del Impuesto a la Renta. "
            "(Art. 87.1, TUO CT)"
        )
        
        self.modify(resultado, cumple_tributario=False)

    @Rule(
        DocumentoTributario(presenta_declaracion_jurada_anual=True),
        ResultadoEvaluacionTributaria()
    )
    def cumple_declaracion_anual(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Declaración Jurada Anual",
            descripcion="Se presenta la declaración jurada anual."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Declaración Jurada Anual.")

    # 7. Domicilio Fiscal Comunicado (MODERADA)
    @Rule(
        DocumentoTributario(domicilio_fiscal_comunicado_sunat=False),
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_domicilio_fiscal(self, resultado):
        """Verifica que el domicilio fiscal esté comunicado a SUNAT"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Domicilio Fiscal Comunicado",
            descripcion="El domicilio fiscal no está comunicado o no se notificó el cambio a SUNAT.",
            base_legal="Art. 11, TUO CT",
            severidad="moderada"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Domicilio Fiscal Comunicado. "
            "El domicilio fiscal no está comunicado o no se notificó el cambio a SUNAT. "
            "(Art. 11, TUO CT)"
        )
        
        self.modify(resultado, cumple_tributario=False)

    @Rule(
        DocumentoTributario(domicilio_fiscal_comunicado_sunat=True),
        ResultadoEvaluacionTributaria()
    )
    def cumple_domicilio_fiscal(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Domicilio Fiscal Comunicado",
            descripcion="El domicilio fiscal está debidamente comunicado a SUNAT."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Domicilio Fiscal Comunicado.")

    # ============= REGLA DE SÍNTESIS CORREGIDA =============
    
    @Rule(
        AS.resultado << ResultadoEvaluacionTributaria(cumple_tributario=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),
        salience=-1000
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluacion para D.S. 133-2013-EF - VERSIÓN CORREGIDA"""
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
            if 'Libros Contables' in aspecto:
                recomendaciones.append("Asegurar el llevado de todos los libros obligatorios (electrónicos o físicos, según corresponda).")
            elif 'Plazo Máximo' in aspecto:
                recomendaciones.append("Mantener los libros contables actualizados dentro del plazo máximo de atraso permitido por SUNAT.")
            elif 'Emisión de Comprobantes' in aspecto:
                recomendaciones.append("Asegurar la emisión de Comprobantes Electrónicos por todas las ventas y operaciones gravadas.")
            elif 'Sustento' in aspecto:
                recomendaciones.append("Exigir y verificar la validez de los comprobantes para sustentar costos y gastos deducibles.")
            elif 'Declaración Jurada Mensual' in aspecto:
                recomendaciones.append("Establecer un calendario estricto para la presentación de las declaraciones juradas mensuales.")
            elif 'Declaración Jurada Anual' in aspecto:
                recomendaciones.append("Presentar la Declaración Jurada Anual del Impuesto a la Renta dentro del plazo establecido.")
            elif 'Domicilio Fiscal' in aspecto:
                recomendaciones.append("Verificar y mantener actualizado el domicilio fiscal ante SUNAT para asegurar la recepción de notificaciones.")
        
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            resultado,
            cumple_tributario=cumple,
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
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacionTributaria':
                    return {
                        'cumple_tributario': fact.get('cumple_tributario', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Fallback si no encuentra resultados
            return {
                'cumple_tributario': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
            return {
                'cumple_tributario': False,
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