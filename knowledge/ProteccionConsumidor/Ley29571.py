"""
Reglas de experta para Ley N° 29571 - Código de Protección y Defensa del Consumidor
Reglamentos: D.S. N° 011-2011-PCM (Reglamento del Libro de Reclamaciones)
Enfoque: Idoneidad, Transparencia, Publicidad y Mecanismos de Reclamo.
"""

from experta import *

class DocumentoConsumidor(Fact):
    # Documento a evaluar (ej. Contrato, Publicidad, Web, Manual de Atención)
    
    # 1. Deber de Idoneidad y Seguridad (Art. 18, 25)
    garantiza_idoneidad = Field(bool, default=False) 
    menciona_riesgos_seguridad = Field(bool, default=False)
    
    # 2. Derecho a la Información y Transparencia (Art. 2)
    es_publicidad_clara_veraz = Field(bool, default=False) 
    tiene_clausulas_transparentes = Field(bool, default=False) 
    
    # 3. Mecanismos de Reclamo (Libro de Reclamaciones - Art. 150)
    tiene_libro_reclamaciones_fisico_virtual = Field(bool, default=False)
    cumple_plazo_respuesta_reclamos = Field(bool, default=False)
    
    # 4. Derecho a Elegir (Art. 68)
    ofrece_posibilidad_pago_anticipado = Field(bool, default=False)

class ResultadoEvaluacion29571(Fact):
    # Almacena Resultados de la evaluación de Ley 29571
    cumple_consumidor = Field(bool, default=True)
    aspectos_cumplidos = Field(list, mandatory=False)
    aspectos_incumplidos = Field(list, mandatory=False)
    recomendaciones = Field(list, mandatory=False)
    explicacion = Field(str, default="")

class ProteccionConsumidorKB(KnowledgeEngine):
    """Motor de inferencia para Ley 29571 - Protección al Consumidor - VERSIÓN CORREGIDA"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
    
    # ============= REGLAS DE EVALUACIÓN CORREGIDAS =============
    
    # 1. Idoneidad y Seguridad (CRÍTICO)
    @Rule(
        DocumentoConsumidor(garantiza_idoneidad=False),
        AS.resultado << ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_garantia_idoneidad(self, resultado):
        """Verifica el deber de idoneidad (correspondencia con la oferta)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Idoneidad del Producto/Servicio",
            descripcion="El producto o servicio no garantiza o no corresponde a lo ofrecido, incurriendo en falta de idoneidad.",
            base_legal="Art. 18, Ley 29571 (Deber de Idoneidad)",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Idoneidad del Producto/Servicio. "
            "El producto o servicio no garantiza o no corresponde a lo ofrecido, incurriendo en falta de idoneidad. "
            "(Art. 18, Ley 29571)"
        )
        
        self.modify(resultado, cumple_consumidor=False)

    @Rule(
        DocumentoConsumidor(garantiza_idoneidad=True),
        ResultadoEvaluacion29571()
    )
    def cumple_garantia_idoneidad(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Idoneidad del Producto/Servicio",
            descripcion="El producto/servicio cumple con el deber de idoneidad."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Idoneidad del Producto/Servicio.")

    # 2. Publicidad y Transparencia de Contrato (CRÍTICO)
    @Rule(
        DocumentoConsumidor(es_publicidad_clara_veraz=False),
        AS.resultado << ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_publicidad_veraz(self, resultado):
        """Verifica que la publicidad no sea engañosa o inexacta"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Publicidad Clara y Veraz",
            descripcion="La publicidad o anuncios no son claros, veraces, o inducen a error al consumidor.",
            base_legal="Art. 32, Ley 29571 (Deber de Veracidad)",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta Publicidad Clara y Veraz. "
            "La publicidad o anuncios no son claros, veraces, o inducen a error al consumidor. "
            "(Art. 32, Ley 29571)"
        )
        
        self.modify(resultado, cumple_consumidor=False)

    @Rule(
        DocumentoConsumidor(es_publicidad_clara_veraz=True),
        ResultadoEvaluacion29571()
    )
    def cumple_publicidad_veraz(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Publicidad Clara y Veraz",
            descripcion="La publicidad cumple con el principio de veracidad."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Publicidad Clara y Veraz.")

    # 3. Libro de Reclamaciones (ALTA)
    @Rule(
        DocumentoConsumidor(tiene_libro_reclamaciones_fisico_virtual=False),
        AS.resultado << ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_libro_reclamaciones(self, resultado):
        """Verifica la existencia del Libro de Reclamaciones (físico o virtual)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Libro de Reclamaciones",
            descripcion="El establecimiento comercial (físico o virtual) no cuenta con el Libro de Reclamaciones (físico o virtual) o aviso visible.",
            base_legal="Art. 150, Ley 29571 / D.S. 011-2011-PCM",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Libro de Reclamaciones. "
            "El establecimiento comercial (físico o virtual) no cuenta con el Libro de Reclamaciones (físico o virtual) o aviso visible. "
            "(Art. 150, Ley 29571 / D.S. 011-2011-PCM)"
        )
        
        self.modify(resultado, cumple_consumidor=False)

    @Rule(
        DocumentoConsumidor(tiene_libro_reclamaciones_fisico_virtual=True),
        ResultadoEvaluacion29571()
    )
    def cumple_libro_reclamaciones(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Libro de Reclamaciones",
            descripcion="Se cuenta con Libro de Reclamaciones y aviso."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Libro de Reclamaciones.")

    # 4. Plazo de Respuesta (ALTA)
    @Rule(
        DocumentoConsumidor(tiene_libro_reclamaciones_fisico_virtual=True, cumple_plazo_respuesta_reclamos=False),
        AS.resultado << ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_cumplir_plazo_respuesta(self, resultado):
        """Verifica el cumplimiento del plazo máximo de respuesta a reclamos"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Plazo de Respuesta a Reclamos",
            descripcion="El proveedor no garantiza la respuesta a los reclamos en el plazo máximo de 30 días calendario (prorrogable a 30 días más).",
            base_legal="Art. 24.1.c, D.S. 011-2011-PCM",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Plazo de Respuesta a Reclamos. "
            "El proveedor no garantiza la respuesta a los reclamos en el plazo máximo de 30 días calendario (prorrogable a 30 días más). "
            "(Art. 24.1.c, D.S. 011-2011-PCM)"
        )
        
        self.modify(resultado, cumple_consumidor=False)

    @Rule(
        DocumentoConsumidor(cumple_plazo_respuesta_reclamos=True),
        ResultadoEvaluacion29571()
    )
    def cumple_plazo_respuesta(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Plazo de Respuesta a Reclamos",
            descripcion="Se cumple con el plazo de respuesta de 30 días calendario."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Plazo de Respuesta a Reclamos.")

    # 5. Cláusulas Abusivas/oscuras (ALTA)
    @Rule(
        DocumentoConsumidor(tiene_clausulas_transparentes=False),
        AS.resultado << ResultadoEvaluacion29571(cumple_consumidor=True)
    )
    def falta_clausulas_transparentes(self, resultado):
        """Verifica la ausencia de cláusulas abusivas o de difícil lectura"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Cláusulas Contractuales Transparentes",
            descripcion="El contrato contiene cláusulas de difícil lectura, ambiguas o que podrían ser consideradas abusivas (ej. exoneración de responsabilidad).",
            base_legal="Art. 49, Ley 29571",
            severidad="alta"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO: Falta Cláusulas Contractuales Transparentes. "
            "El contrato contiene cláusulas de difícil lectura, ambiguas o que podrían ser consideradas abusivas (ej. exoneración de responsabilidad). "
            "(Art. 49, Ley 29571)"
        )
        
        self.modify(resultado, cumple_consumidor=False)

    @Rule(
        DocumentoConsumidor(tiene_clausulas_transparentes=True),
        ResultadoEvaluacion29571()
    )
    def cumple_clausulas_transparentes(self):
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Cláusulas Contractuales Transparentes",
            descripcion="Los contratos no contienen cláusulas abusivas o de difícil lectura."
        ))
        self.explicaciones.append("CUMPLE: Se identificó Cláusulas Contractuales Transparentes.")

    # 6. Pago Anticipado (MODERADA/ADICIONAL)
    @Rule(
        DocumentoConsumidor(ofrece_posibilidad_pago_anticipado=True),
        ResultadoEvaluacion29571()
    )
    def cumple_pago_anticipado(self):
        """Valora positivamente el derecho a pagar anticipadamente sin penalidades"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Derecho a Pago Anticipado",
            descripcion="Se permite al consumidor el pago anticipado sin penalidades."
        ))
        self.explicaciones.append("BUENA PRÁCTICA: Se reconoce el derecho al pago anticipado sin penalidades (Art. 68).")

    # 7. Medidas de Seguridad (COMPLEMENTARIA)
    @Rule(
        DocumentoConsumidor(menciona_riesgos_seguridad=True),
        ResultadoEvaluacion29571()
    )
    def menciona_medidas_seguridad(self):
        """Valora la mención de riesgos y medidas de seguridad"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Información sobre Riesgos y Seguridad",
            descripcion="Se informa sobre riesgos y medidas de seguridad del producto/servicio."
        ))
        self.explicaciones.append("BUENA PRÁCTICA: Se informa sobre riesgos y medidas de seguridad (Art. 25).")

    # ============= REGLA DE SÍNTESIS CORREGIDA =============
    
    @Rule(
        AS.resultado << ResultadoEvaluacion29571(cumple_consumidor=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),
        salience=-1000
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluacion para Ley 29571 - VERSIÓN CORREGIDA"""
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
            if 'Idoneidad' in aspecto:
                recomendaciones.append("Asegurar que los productos/servicios se correspondan exactamente con la descripción y expectativas generadas en la publicidad y contratos.")
            elif 'Publicidad' in aspecto:
                recomendaciones.append("Revisar toda la comunicación comercial para asegurar que sea veraz, suficiente y no omita información relevante para la decisión de compra.")
            elif 'Libro de Reclamaciones' in aspecto:
                recomendaciones.append("Implementar el Libro de Reclamaciones (físico o virtual), incluyendo el aviso obligatorio en un lugar visible.")
            elif 'Plazo de Respuesta' in aspecto:
                recomendaciones.append("Asegurar el cumplimiento del plazo de respuesta de 30 días calendario a todo reclamo o queja registrado en el Libro.")
            elif 'Cláusulas' in aspecto:
                recomendaciones.append("Eliminar cualquier cláusula que restrinja derechos o exonere responsabilidad del proveedor. Asegurar que la letra sea legible y clara.")
        
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            resultado,
            cumple_consumidor=cumple,
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
                if hasattr(fact, '__class__') and fact.__class__.__name__ == 'ResultadoEvaluacion29571':
                    return {
                        'cumple_consumidor': fact.get('cumple_consumidor', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),
                        'recomendaciones': list(fact.get('recomendaciones', [])),
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Fallback si no encuentra resultados
            return {
                'cumple_consumidor': False,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
            return {
                'cumple_consumidor': False,
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