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
    cumple_tributario = Field(bool, default=True) # Cumple con las obligaciones tributarias formales
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class NormativaTributariaKB(KnowledgeEngine):
    """Motor de inferencia para D.S. 133-2013-EF - Código Tributario"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
        self.recomendaciones_generadas = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluacion"""
        yield ResultadoEvaluacionTributaria()
    
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
        if resultado_fact and resultado_fact.get('cumple_tributario'):
             self.modify(self.facts[1], cumple_tributario = False)

    def _registrar_cumplimiento(self, aspecto, descripcion):
        """Registra un cumplimiento"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto=aspecto,
            descripcion=descripcion
        ))
        self.explicaciones.append(f"CUMPLE: Se identificó {aspecto}.")


    # --- REGLAS DE EVALUACIÓN DE OBLIGACIONES CLAVE ---
    
    # 1. Libros Contables y Registros (CRÍTICO)
    @Rule(
        DocumentoTributario(tiene_libros_obligatorios_vigentes=False) |
        DocumentoTributario(libros_cumplen_plazo_maximo_atraso=False),
        ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_libros_y_atraso(self):
        """Verifica el llevado de libros obligatorios y su registro dentro del plazo máximo de atraso"""
        
        descripcion = ""
        if not self.facts.get(self.facts[0]).get('tiene_libros_obligatorios_vigentes'):
            descripcion += "No se llevan los libros y registros contables obligatorios según el régimen tributario. "
        if not self.facts.get(self.facts[0]).get('libros_cumplen_plazo_maximo_atraso'):
            descripcion += "Los libros obligatorios están atrasados más allá del plazo máximo permitido por SUNAT."
            
        self._registrar_incumplimiento(
            aspecto="Llevado de Libros Contables",
            descripcion=descripcion.strip(),
            base_legal="Art. 87.7, TUO CT / R.S. 234-2006/SUNAT",
            severidad="crítica", 
            recomendacion_texto="Asegurar el llevado de todos los libros obligatorios (electrónicos o físicos, según corresponda) y mantenerlos actualizados dentro del plazo máximo de atraso."
        )

    @Rule(
        DocumentoTributario(tiene_libros_obligatorios_vigentes=True, libros_cumplen_plazo_maximo_atraso=True), 
        ResultadoEvaluacionTributaria()
    )
    def cumple_libros_y_atraso(self):
        self._registrar_cumplimiento("Llevado de Libros Contables", "Los libros contables se llevan y están actualizados.")

    # 2. Emisión y Sustento con Comprobantes de Pago (CRÍTICO)
    @Rule(
        DocumentoTributario(emite_comprobantes_pago_por_ventas=False) |
        DocumentoTributario(comprobantes_sustentan_costo_gasto=False),
        ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_comprobantes_y_sustento(self):
        """Verifica la emisión de Comprobantes de Pago y el sustento de costos/gastos"""
        
        descripcion = ""
        if not self.facts.get(self.facts[0]).get('emite_comprobantes_pago_por_ventas'):
            descripcion += "No se emiten comprobantes de pago por todas las ventas u operaciones gravadas. "
        if not self.facts.get(self.facts[0]).get('comprobantes_sustentan_costo_gasto'):
            descripcion += "Falta sustento con Comprobantes de Pago válidos (Facturas, Boletas, etc.) para gastos y costos."
            
        self._registrar_incumplimiento(
            aspecto="Comprobantes de Pago",
            descripcion=descripcion.strip(),
            base_legal="Art. 87.8, TUO CT",
            severidad="crítica",
            recomendacion_texto="Asegurar la emisión de Comprobantes Electrónicos por todas las ventas. Exigir y verificar la validez de los comprobantes para sustentar costos y gastos deducibles."
        )

    @Rule(
        DocumentoTributario(emite_comprobantes_pago_por_ventas=True, comprobantes_sustentan_costo_gasto=True), 
        ResultadoEvaluacionTributaria()
    )
    def cumple_comprobantes_y_sustento(self):
        self._registrar_cumplimiento("Comprobantes de Pago", "Se emiten y se sustentan correctamente las operaciones con Comprobantes de Pago válidos.")

    # 3. Declaraciones Juradas (ALTA)
    @Rule(
        DocumentoTributario(presenta_declaracion_jurada_mensual=False) |
        DocumentoTributario(presenta_declaracion_jurada_anual=False),
        ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_declaraciones_juradas(self):
        """Verifica la presentación de Declaraciones Juradas (mensual y anual)"""
        
        descripcion = ""
        if not self.facts.get(self.facts[0]).get('presenta_declaracion_jurada_mensual'):
            descripcion += "Falta presentar las declaraciones juradas mensuales (IGV/Renta) en el plazo establecido. "
        if not self.facts.get(self.facts[0]).get('presenta_declaracion_jurada_anual'):
            descripcion += "Falta presentar la Declaración Jurada Anual del Impuesto a la Renta (si aplica)."
            
        self._registrar_incumplimiento(
            aspecto="Declaraciones Juradas",
            descripcion=descripcion.strip(),
            base_legal="Art. 79, TUO Ley Impuesto a la Renta / Art. 87.1, TUO CT",
            severidad="alta",
            recomendacion_texto="Establecer un calendario estricto para la presentación de todas las Declaraciones Juradas, evitando multas por presentación fuera de plazo."
        )

    @Rule(
        DocumentoTributario(presenta_declaracion_jurada_mensual=True, presenta_declaracion_jurada_anual=True), 
        ResultadoEvaluacionTributaria()
    )
    def cumple_declaraciones_juradas(self):
        self._registrar_cumplimiento("Declaraciones Juradas", "Se cumplen con la presentación de las Declaraciones Juradas (mensual y anual).")

    # 4. Domicilio Fiscal (MODERADA)
    @Rule(
        DocumentoTributario(domicilio_fiscal_comunicado_sunat=False),
        ResultadoEvaluacionTributaria(cumple_tributario=True)
    )
    def falta_domicilio_fiscal(self):
        """Verifica que el domicilio fiscal esté debidamente comunicado y actualizado"""
        self._registrar_incumplimiento(
            aspecto="Domicilio Fiscal",
            descripcion="El domicilio fiscal no está comunicado, no corresponde a la realidad o no se notificó el cambio a SUNAT.",
            base_legal="Art. 11, TUO CT",
            severidad="moderada",
            recomendacion_texto="Verificar y mantener actualizado el domicilio fiscal ante SUNAT para asegurar la recepción de notificaciones."
        )

    @Rule(DocumentoTributario(domicilio_fiscal_comunicado_sunat=True), ResultadoEvaluacionTributaria())
    def cumple_domicilio_fiscal(self):
        self._registrar_cumplimiento("Domicilio Fiscal", "El domicilio fiscal está debidamente comunicado a SUNAT.")


    # ------ REGLA DE SINTESIS --------

    @Rule(
        ResultadoEvaluacionTributaria(cumple_tributario = MATCH.cumple),
        salience = -100
    )
    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluacion para D.S. 133-2013-EF"""
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
            cumple_tributario = cumple,
            aspectos_cumplidos = cumplimientos,
            aspectos_incumplidos = incumplimientos,
            recomendaciones = self.recomendaciones_generadas,
            explicacion = explicacion_final
        )

    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacionTributaria):
                return {
                    'cumple_tributario': fact.get('cumple_tributario'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)