"""
Reglas de experta para Ley N° 29733 - Ley de Protección de Datos Personales
Reglamento: D.S. 003-2013-JUS
"""

from experta import *

class DocumentoProteccionDatos(Fact):
    # Documento a evaluar según Ley 29733
    tiene_politica_privacidad = Field(bool, default=False)
    tiene_consentimiento_informado = Field(bool, default=False)
    tiene_registro_banco_datos = Field(bool, default=False)
    tiene_contrato_encargo = Field(bool, default=False)
    tiene_clausulas_legales = Field(bool, default=False)
    menciona_autoridad_proteccion = Field(bool, default=False)
    especifica_finalidad_datos = Field(bool,default=False)
    menciona_derechos_arco = Field(bool,default=False) # Acceso, Retifiacion, cancelación, oposición
    tiene_medidadas_seguridad = Field(bool,default=False)
    menciona_plazo_conservacion = Field(bool,default=False)

class ResultadoEvaluacion(Fact):
    #Almacena Resultados de la evaluacion
    cumple = Field(bool,default=True)
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class ProteccionDatosPersonalesKB(KnowledgeEngine):
    """Motor de inferencia para Ley 29733"""

    def __init__(self):
        super().__init__()
        self.aspectos_evaluados = []
        self.explicaciones = []
    
    @DefFacts()

    def inicializar(self):
        """Inicializar el resultado de la evaluacion"""
        yield ResultadoEvaluacion()
    
    @Rule(
        DocumentoProteccionDatos(tiene_politica_privacidad=False),
        ResultadoEvaluacion(cumple=True)
    )

    def falta_politica_privacidad(self):
        """Verifica que exista politica de privacidad"""
        
        self.declare(Fact(
            tipo = "incumplimiento",
            aspecto = "Politica de Privacidad",
            descripcion = "No se identifico una política de privacidad clara",
            base_legal = "Ley 27933",
            severidad = "crítica"
        ))

        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: El documento debe contener una politica de privacidad"
            "que informe sobre el tratamiento de datos personales (Art. 18, Ley 29733)"
        )

        self.modify(self.facts[1], cumple = False)

    @Rule(
        DocumentoProteccionDatos(tiene_politica_privacidad=True),
        ResultadoEvaluacion()
    )

    def cumple_politica_privacidad(self):
        """Confirma precencia de politica de privacidad"""
        self.declare(Fact(
            tipo = "cumplimiento",
            aspecto = "Politica de Privacidad",
            descripcion = "Se identificó politica de privacidad"
        ))

        self.explicaciones(
            "CUMPLE: El documento contiene politica de privacidad según Ley 29733"
        )

    @Rule(
        DocumentoProteccionDatos(tiene_consentimiento_informado=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_consentimiento_informado(self):
        """ Verifica consentimiento informado (Ley 29733)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Consentimiento Informado",
            descripcion="No se identificó mecanismo de consentimiento informado",
            base_legal="Ley 29733",
            severidad="crítica"
        ))
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Falta consentimiento previo, libre, inequívoco, expreso e informado "
            "del titular de datos personales (Ley 29733)"
        )
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoProteccionDatos(tiene_consentimiento_informado=True),
        ResultadoEvaluacion()
    )
    def cumple_consentimiento_informado(self):
        """Confirma presencia de consentimiento informado"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Consentimiento Informado",
            descripcion="Se identificó mecanismo de consentimiento"
        ))
        self.explicaciones.append(
            "CUMPLE: Documento incluye consentimiento informado según Ley 29733"
        )
    
    @Rule(
        DocumentoProteccionDatos(tiene_registro_banco_datos=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_registro_banco_datos(self):
        """Verifica mención de registro ante ANPDP (Ley 29733)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Registro de Banco de Datos",
            descripcion="No se menciona registro ante la Autoridad Nacional de Protección de Datos Personales",
            base_legal="Ley 29733",
            severidad="alta"
        ))
        self.explicaciones.append(
            "INCUMPLIMIENTO: El banco de datos personales debe estar inscrito ante la "
            "Autoridad Nacional de Protección de Datos Personales (Ley 29733)"
        )
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoProteccionDatos(tiene_registro_banco_datos=True),
        ResultadoEvaluacion()
    )
    def cumple_registro_banco_datos(self):
        """Confirma mención de registro ante ANPDP"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Registro de Banco de Datos",
            descripcion="Se menciona registro ante ANPDP"
        ))
        self.explicaciones.append(
            "CUMPLE: Se identifica mención de registro ante ANPDP (Ley 29733)"
        )
    
    @Rule(
        DocumentoProteccionDatos(especifica_finalidad_datos=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_finalidad_datos(self):
        """Verifica especificación de finalidad (Ley 29733)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Finalidad del Tratamiento",
            descripcion="No se especifica la finalidad del tratamiento de datos",
            base_legal="Ley 29733 (Principio de Finalidad)",
            severidad="crítica"
        ))
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: Debe especificarse claramente la finalidad determinada, "
            "explícita y lícita del tratamiento (Principio de Finalidad)"
        )
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoProteccionDatos(especifica_finalidad_datos=True),
        ResultadoEvaluacion()
    )
    def cumple_finalidad_datos(self):
        """Confirma especificación de finalidad"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Finalidad del Tratamiento",
            descripcion="Se especifica finalidad del tratamiento"
        ))
        self.explicaciones.append(
            "CUMPLE: El documento especifica la finalidad del tratamiento de datos"
        )
    
    @Rule(
        DocumentoProteccionDatos(menciona_derechos_arco=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_derechos_arco(self):
        """Verifica mención de derechos ARCO (Ley 29733)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Derechos ARCO",
            descripcion="No se informan los derechos de Acceso, Rectificación, Cancelación y Oposición",
            base_legal="Ley 29733",
            severidad="alta"
        ))
        self.explicaciones.append(
            "INCUMPLIMIENTO: Debe informarse sobre los derechos de Acceso, Rectificación, "
            "Cancelación y Oposición del titular (Ley 29733)"
        )
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoProteccionDatos(menciona_derechos_arco=True),
        ResultadoEvaluacion()
    )
    def cumple_derechos_arco(self):
        """Confirma mención de derechos ARCO"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Derechos ARCO",
            descripcion="Se informan los derechos ARCO"
        ))
        self.explicaciones.append(
            "CUMPLE: Se informan los derechos ARCO del titular"
        )
    
    @Rule(
        DocumentoProteccionDatos(tiene_medidas_seguridad=False),
        ResultadoEvaluacion(cumple=True)
    )
    def falta_medidas_seguridad(self):
        """Verifica mención de medidas de seguridad (Art. 39 Reglamento)"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Medidas de Seguridad",
            descripcion="No se mencionan medidas técnicas y organizativas de seguridad",
            base_legal="Art. 39, D.S. 003-2013-JUS",
            severidad="alta"
        ))
        self.explicaciones.append(
            "INCUMPLIMIENTO: Deben implementarse medidas técnicas y organizativas para "
            "garantizar la seguridad de datos personales (Art. 39, Reglamento)"
        )
        self.modify(self.facts[1], cumple=False)
    
    @Rule(
        DocumentoProteccionDatos(tiene_medidas_seguridad=True),
        ResultadoEvaluacion()
    )
    def cumple_medidas_seguridad(self):
        """Confirma medidas de seguridad"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Medidas de Seguridad",
            descripcion="Se mencionan medidas de seguridad"
        ))
        self.explicaciones.append(
            "CUMPLE: Se identifican medidas de seguridad para datos personales (Art. 39)"
        )
    
    #Complenetarias

    @Rule(
        DocumentoProteccionDatos(tiene_contrato_encargo=True),
        ResultadoEvaluacion()
    )
    def tiene_contrato_encargo_tratamiento(self):
        """Valora positivamente la presencia de contrato de encargo"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Contrato de Encargo",
            descripcion="Se identifica contrato de encargo de tratamiento",
            base_legal="Art. 8 del Reglamento"
        ))
        self.explicaciones.append(
            "BUENA PRÁCTICA: Se identifica contrato de encargo cuando corresponde (Art. 8, Reglamento)"
        )
    
    @Rule(
        DocumentoProteccionDatos(menciona_plazo_conservacion=True),
        ResultadoEvaluacion()
    )
    def tiene_plazo_conservacion(self):
        """Valora la especificación del plazo de conservación"""
        self.declare(Fact(
            tipo="cumplimiento_adicional",
            aspecto="Plazo de Conservación",
            descripcion="Se especifica plazo de conservación de datos"
        ))
        self.explicaciones.append(
            "BUENA PRÁCTICA: Se especifica el plazo de conservación de datos personales"
        )
    
    # ------ REGLA SE SINTESIS --------

    @Rule(
        ResultadoEvaluacion(cumple = MATCH.cumple),
        salience = -100
    )

    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluacion"""
        cumplimientos = []
        incumplimientos = []
        recomendaciones = []

        for fact in self.facts.values():
            if isinstance(fact, Fact):
                if fact.get('tipo') == 'cumplimiento':
                    cumplimientos.append(fact.get('aspecto'))
                elif fact.get('tipo') == 'incumplimiento':
                    incumplimientos.append({
                        'aspecto': fact.get('aspecto'),
                        'descripcion': fact.get('descripcion'),
                        'base_legal': fact.get('base_legal'),
                        'severidad': fact.get('severidad')
                    })

                    #Generar recomendacion

                    if 'Política de Privacidad' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Elaborar e implementar una política de privacidad conforme al Art. 18 de la Ley 29733"
                        )
                    elif 'Consentimiento' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Implementar mecanismos de consentimiento informado previo al tratamiento de datos"
                        )
                    elif 'Registro' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Inscribir el banco de datos ante la Autoridad Nacional de Protección de Datos Personales"
                        )
                    elif 'Finalidad' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Especificar claramente la finalidad del tratamiento de datos personales"
                        )
                    elif 'ARCO' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Informar claramente sobre los derechos de Acceso, Rectificación, Cancelación y Oposición"
                        )
                    elif 'Seguridad' in fact.get('aspecto', ''):
                        recomendaciones.append(
                            "Implementar medidas técnicas y organizativas de seguridad de datos personales"
                        )

        # Modificar el resultado final
        explicacion_final = "\n".join(self.explicaciones)

        self.modify(
            self.facts[1],
            cumple = cumple,
            aspectos_cumplidos = cumplimientos,
            aspectos_incumplidos = incumplimientos,
            recomendaciones = recomendaciones,
            explicacion = explicacion_final
        )

    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacion):
                return {
                    'cumple': fact.get('cumple'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicacion de la desicion tomada"""
        return "\n\n".join(self.explicaciones)

