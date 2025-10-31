"""
Reglas de experta para Ley N° 29571 - Código de Protección y Defensa del Consumidor
Reglamentos: D.S. N° 011-2011-PCM (Reglamento del Libro de Reclamaciones)
Enfoque: Idoneidad, Transparencia, Publicidad y Mecanismos de Reclamo.
"""

from experta import *

class DocumentoConsumidor(Fact):
    # Documento a evaluar (ej. Contrato, Publicidad, Web, Manual de Atención)
    
    # 1. Deber de Idoneidad y Seguridad (Art. 18, 25)
    garantiza_idoneidad = Field(bool, default=False) # Producto/servicio conforme a lo ofrecido
    menciona_riesgos_seguridad = Field(bool, default=False) # Adopción de medidas de seguridad y advertencia
    
    # 2. Derecho a la Información y Transparencia (Art. 2)
    es_publicidad_clara_veraz = Field(bool, default=False) # Publicidad que no induce a error
    tiene_clausulas_transparentes = Field(bool, default=False) # Cláusulas sin ambigüedad o abusivas
    
    # 3. Mecanismos de Reclamo (Libro de Reclamaciones - Art. 150)
    tiene_libro_reclamaciones_fisico_virtual = Field(bool, default=False)
    cumple_plazo_respuesta_reclamos = Field(bool, default=False) # Respuesta en 30 días calendario (máx. 60)
    
    # 4. Derecho a Elegir (Art. 68)
    ofrece_posibilidad_pago_anticipado = Field(bool, default=False) # (Aplica a créditos/servicios periódicos)

class ResultadoEvaluacion29571(Fact):
    # Almacena Resultados de la evaluación de Ley 29571
    cumple_consumidor = Field(bool, default=True) # Cumple con las obligaciones clave de protección al consumidor
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class ProteccionConsumidorKB(KnowledgeEngine):
    """Motor de inferencia para Ley 29571 - Protección al Consumidor"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
        self.recomendaciones_generadas = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluacion"""
        yield ResultadoEvaluacion29571()
    
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
        if resultado_fact and resultado_fact.get('cumple_consumidor'):
             self.modify(self.facts[1], cumple_consumidor = False)

    def _registrar_cumplimiento(self, aspecto, descripcion):
        """Registra un cumplimiento"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto=aspecto,
            descripcion=descripcion
        ))
        self.explicaciones.append(f"CUMPLE: Se identificó {aspecto}.")


    # --- REGLAS DE EVALUACIÓN DE OBLIGACIONES CLAVE ---
    
    # 1. Idoneidad y Seguridad (CRÍTICO)
    @Rule(
        DocumentoConsumidor(garantiza_idoneidad=False),
        ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_garantia_idoneidad(self):
        """Verifica el deber de idoneidad (correspondencia con la oferta)"""
        self._registrar_incumplimiento(
            aspecto="Idoneidad del Producto/Servicio",
            descripcion="El producto o servicio no garantiza o no corresponde a lo ofrecido, incurriendo en falta de idoneidad.",
            base_legal="Art. 18, Ley 29571 (Deber de Idoneidad)",
            severidad="crítica", 
            recomendacion_texto="Asegurar que los productos/servicios se correspondan exactamente con la descripción y expectativas generadas en la publicidad y contratos."
        )

    @Rule(DocumentoConsumidor(garantiza_idoneidad=True), ResultadoEvaluacion29571())
    def cumple_garantia_idoneidad(self):
        self._registrar_cumplimiento("Idoneidad del Producto/Servicio", "El producto/servicio cumple con el deber de idoneidad.")

    # 2. Publicidad y Transparencia de Contrato (CRÍTICO)
    @Rule(
        DocumentoConsumidor(es_publicidad_clara_veraz=False),
        ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_publicidad_veraz(self):
        """Verifica que la publicidad no sea engañosa o inexacta"""
        self._registrar_incumplimiento(
            aspecto="Publicidad Clara y Veraz",
            descripcion="La publicidad o anuncios no son claros, veraces, o inducen a error al consumidor.",
            base_legal="Art. 32, Ley 29571 (Deber de Veracidad)",
            severidad="crítica",
            recomendacion_texto="Revisar toda la comunicación comercial para asegurar que sea veraz, suficiente y no omita información relevante para la decisión de compra."
        )

    @Rule(DocumentoConsumidor(es_publicidad_clara_veraz=True), ResultadoEvaluacion29571())
    def cumple_publicidad_veraz(self):
        self._registrar_cumplimiento("Publicidad Clara y Veraz", "La publicidad cumple con el principio de veracidad.")

    # 3. Libro de Reclamaciones (ALTA)
    @Rule(
        DocumentoConsumidor(tiene_libro_reclamaciones_fisico_virtual=False),
        ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_libro_reclamaciones(self):
        """Verifica la existencia del Libro de Reclamaciones (físico o virtual)"""
        self._registrar_incumplimiento(
            aspecto="Libro de Reclamaciones",
            descripcion="El establecimiento comercial (físico o virtual) no cuenta con el Libro de Reclamaciones (físico o virtual) o aviso visible.",
            base_legal="Art. 150, Ley 29571 / D.S. 011-2011-PCM",
            severidad="alta",
            recomendacion_texto="Implementar el Libro de Reclamaciones (físico o virtual), incluyendo el aviso obligatorio en un lugar visible."
        )

    @Rule(DocumentoConsumidor(tiene_libro_reclamaciones_fisico_virtual=True), ResultadoEvaluacion29571())
    def cumple_libro_reclamaciones(self):
        self._registrar_cumplimiento("Libro de Reclamaciones", "Se cuenta con Libro de Reclamaciones y aviso.")

    # 4. Plazo de Respuesta (ALTA)
    @Rule(
        DocumentoConsumidor(tiene_libro_reclamaciones_fisico_virtual=True, cumple_plazo_respuesta_reclamos=False),
        ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_cumplir_plazo_respuesta(self):
        """Verifica el cumplimiento del plazo máximo de respuesta a reclamos"""
        self._registrar_incumplimiento(
            aspecto="Plazo de Respuesta a Reclamos",
            descripcion="El proveedor no garantiza la respuesta a los reclamos en el plazo máximo de 30 días calendario (prorrogable a 30 días más).",
            base_legal="Art. 24.1.c, D.S. 011-2011-PCM",
            severidad="alta",
            recomendacion_texto="Asegurar el cumplimiento del plazo de respuesta de 30 días calendario a todo reclamo o queja registrado en el Libro."
        )

    @Rule(DocumentoConsumidor(cumple_plazo_respuesta_reclamos=True), ResultadoEvaluacion29571())
    def cumple_plazo_respuesta(self):
        self._registrar_cumplimiento("Plazo de Respuesta a Reclamos", "Se cumple con el plazo de respuesta de 30 días calendario.")

    # 5. Cláusulas Abusivas/oscuras (ALTA)
    @Rule(
        DocumentoConsumidor(tiene_clausulas_transparentes=False),
        ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_clausulas_transparentes(self):
        """Verifica la ausencia de cláusulas abusivas o de difícil lectura"""
        self._registrar_incumplimiento(
            aspecto="Cláusulas Contractuales Transparentes",
            descripcion="El contrato contiene cláusulas de difícil lectura, ambiguas o que podrían ser consideradas abusivas (ej. exoneración de responsabilidad).",
            base_legal="Art. 49, Ley 29571",
            severidad="alta",
            recomendacion_texto="Eliminar cualquier cláusula que restrinja derechos o exonere responsabilidad del proveedor. Asegurar que la letra sea legible y clara."
        )

    @Rule(DocumentoConsumidor(tiene_clausulas_transparentes=True), ResultadoEvaluacion29571())
    def cumple_clausulas_transparentes(self):
        self._registrar_cumplimiento("Cláusulas Contractuales Transparentes", "Los contratos no contienen cláusulas abusivas o de difícil lectura.")

    # 6. Pago Anticipado (MODERADA/ADICIONAL)
    @Rule(
        DocumentoConsumidor(ofrece_posibilidad_pago_anticipado=True),
        ResultadoEvaluacion29571()
    )
    def cumple_pago_anticipado(self):
        """Valora positivamente el derecho a pagar anticipadamente sin penalidades (servicios crediticios/periódicos)"""
        self._registrar_cumplimiento(
            aspecto="Derecho a Pago Anticipado",
            descripcion="Se permite al consumidor el pago anticipado o adelanto de cuotas sin penalidades ni cobros de naturaleza o efecto similar (para servicios periódicos/créditos).",
            base_legal="Art. 68, Ley 29571",
        )
        self.explicaciones.append("CUMPLE: Se reconoce el derecho al pago anticipado sin penalidades (Art. 68).")


    # ------ REGLA DE SINTESIS --------

    @Rule(
        ResultadoEvaluacion29571(cumple_consumidor = MATCH.cumple),
        salience = -100
    )
    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluacion para Ley 29571"""
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
            cumple_consumidor = cumple,
            aspectos_cumplidos = cumplimientos,
            aspectos_incumplidos = incumplimientos,
            recomendaciones = self.recomendaciones_generadas,
            explicacion = explicacion_final
        )

    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacion29571):
                return {
                    'cumple_consumidor': fact.get('cumple_consumidor'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)