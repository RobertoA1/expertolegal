"""
Reglas de experta para Ley N° 29733 - Ley de Protección de Datos Personales
Reglamento: D.S. 003-2013-JUS
"""

from experta import *

class DocumentoProteccionDatos(Fact):
    """Documento a evaluar según Ley 29733"""
    tiene_politica_privacidad = Field(bool, default=False)
    tiene_consentimiento_informado = Field(bool, default=False)
    tiene_registro_banco_datos = Field(bool, default=False)
    tiene_contrato_encargo = Field(bool, default=False)
    tiene_clausulas_legales = Field(bool, default=False)
    menciona_autoridad_proteccion = Field(bool, default=False)
    especifica_finalidad_datos = Field(bool, default=False)
    menciona_derechos_arco = Field(bool, default=False)  # Acceso, Rectificación, Cancelación, Oposición
    tiene_medidas_seguridad = Field(bool, default=False)
    menciona_plazo_conservacion = Field(bool, default=False)


class ResultadoEvaluacion(Fact):
    """Almacena resultados de la evaluación"""
    cumple = Field(bool, default=True)
    # 🔧 No usar default con listas mutables, se inicializan en __init__
    aspectos_cumplidos = Field(list, mandatory=False)
    aspectos_incumplidos = Field(list, mandatory=False)
    recomendaciones = Field(list, mandatory=False)
    explicacion = Field(str, default="")


class ProteccionDatosPersonalesKB(KnowledgeEngine):
    """Motor de inferencia para Ley 29733"""

    def __init__(self):
        super().__init__()
        self.aspectos_evaluados = []
        self.explicaciones = []
        self.resultado_fact_id = None  # 🔧 Guardamos el ID del fact ResultadoEvaluacion
        self.resultado_generado = False  # 🔧 Bandera para evitar bucle infinito
    
    # 🔧 ELIMINADO: No declaramos ResultadoEvaluacion aquí
    # Se declara desde la aplicación
    
    # ============= REGLAS DE INCUMPLIMIENTO =============
    
    @Rule(
        DocumentoProteccionDatos(tiene_politica_privacidad=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)  # 🔧 Capturamos el fact
    )
    def falta_politica_privacidad(self, resultado):
        """Verifica que exista política de privacidad"""
        self.declare(Fact(
            tipo="incumplimiento",
            aspecto="Política de Privacidad",
            descripcion="No se identificó una política de privacidad clara",
            base_legal="Ley 29733",
            severidad="crítica"
        ))
        
        self.explicaciones.append(
            "INCUMPLIMIENTO CRÍTICO: El documento debe contener una política de privacidad "
            "que informe sobre el tratamiento de datos personales (Art. 18, Ley 29733)"
        )
        
        # 🔧 Usar el fact capturado
        self.modify(resultado, cumple=False)
    
    @Rule(
        DocumentoProteccionDatos(tiene_politica_privacidad=True),
        ResultadoEvaluacion()
    )
    def cumple_politica_privacidad(self):
        """Confirma presencia de política de privacidad"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto="Política de Privacidad",
            descripcion="Se identificó política de privacidad"
        ))
        
        self.explicaciones.append(
            "CUMPLE: El documento contiene política de privacidad según Ley 29733"
        )
    
    @Rule(
        DocumentoProteccionDatos(tiene_consentimiento_informado=False),
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_consentimiento_informado(self, resultado):
        """Verifica consentimiento informado (Ley 29733)"""
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
        
        self.modify(resultado, cumple=False)
    
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
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_registro_banco_datos(self, resultado):
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
        
        self.modify(resultado, cumple=False)
    
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
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_finalidad_datos(self, resultado):
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
        
        self.modify(resultado, cumple=False)
    
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
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_derechos_arco(self, resultado):
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
        
        self.modify(resultado, cumple=False)
    
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
        AS.resultado << ResultadoEvaluacion(cumple=True)
    )
    def falta_medidas_seguridad(self, resultado):
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
        
        self.modify(resultado, cumple=False)
    
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
    
    # ============= REGLAS COMPLEMENTARIAS =============
    
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
    
    # ============= REGLA DE SÍNTESIS =============
    
    @Rule(
        AS.resultado << ResultadoEvaluacion(cumple=MATCH.cumple),
        NOT(Fact(sintesis_generada=True)),  # 🔧 Solo si NO existe este fact
        salience=-100
    )
    def generar_resultado_final(self, resultado, cumple):
        """Generar el resumen final de evaluación"""
        
        cumplimientos = []
        incumplimientos = []
        recomendaciones = []
        
        for fact in self.facts.values():
            if isinstance(fact, Fact):
                tipo = fact.get('tipo')
                
                if tipo == 'cumplimiento':
                    cumplimientos.append(fact.get('aspecto'))
                    
                elif tipo == 'incumplimiento':
                    incumplimientos.append({
                        'aspecto': fact.get('aspecto'),
                        'descripcion': fact.get('descripcion'),
                        'base_legal': fact.get('base_legal'),
                        'severidad': fact.get('severidad')
                    })
                    
                    # Generar recomendación
                    aspecto = fact.get('aspecto', '')
                    if 'Política de Privacidad' in aspecto:
                        recomendaciones.append(
                            "Elaborar e implementar una política de privacidad conforme al Art. 18 de la Ley 29733"
                        )
                    elif 'Consentimiento' in aspecto:
                        recomendaciones.append(
                            "Implementar mecanismos de consentimiento informado previo al tratamiento de datos"
                        )
                    elif 'Registro' in aspecto:
                        recomendaciones.append(
                            "Inscribir el banco de datos ante la Autoridad Nacional de Protección de Datos Personales"
                        )
                    elif 'Finalidad' in aspecto:
                        recomendaciones.append(
                            "Especificar claramente la finalidad del tratamiento de datos personales"
                        )
                    elif 'ARCO' in aspecto:
                        recomendaciones.append(
                            "Informar claramente sobre los derechos de Acceso, Rectificación, Cancelación y Oposición"
                        )
                    elif 'Seguridad' in aspecto:
                        recomendaciones.append(
                            "Implementar medidas técnicas y organizativas de seguridad de datos personales"
                        )
        
        # Modificar el resultado final
        explicacion_final = "\n".join(self.explicaciones)
        
        self.modify(
            resultado,
            cumple=cumple,
            aspectos_cumplidos=cumplimientos,
            aspectos_incumplidos=incumplimientos,
            recomendaciones=recomendaciones,
            explicacion=explicacion_final
        )
        
        # 🔧 DECLARAR FACT DE CONTROL para que esta regla no se ejecute de nuevo
        self.declare(Fact(sintesis_generada=True))
    
    # ============= MÉTODOS DE UTILIDAD =============
    
    def obtener_resultados(self):
        """Retorna el resultado de la evaluación - VERSIÓN ROBUSTA"""
        try:
            # Buscar el fact ResultadoEvaluacion
            for fact_id, fact in self.facts.items():
                # 🔧 CORRECCIÓN: Verificar por tipo de clase directamente
                if fact.__class__.__name__ == 'ResultadoEvaluacion':
                    # 🔧 Acceder a los atributos directamente (no con getattr)
                    return {
                        'cumple': fact.get('cumple', False),
                        'aspectos_cumplidos': list(fact.get('aspectos_cumplidos', [])),  # 🔧 Convertir frozenlist a list
                        'aspectos_incumplidos': list(fact.get('aspectos_incumplidos', [])),  # 🔧 Convertir frozenlist a list
                        'recomendaciones': list(fact.get('recomendaciones', [])),  # 🔧 Convertir frozenlist a list
                        'explicacion': fact.get('explicacion', '')
                    }
            
            # Si no encuentra el fact, crear resultado básico
            print("⚠️ No se encontró ResultadoEvaluacion, creando resultado básico")
            return {
                'cumple': True,
                'aspectos_cumplidos': self._extraer_cumplimientos(),
                'aspectos_incumplidos': self._extraer_incumplimientos(),
                'recomendaciones': ['Revisar documento manualmente'],
                'explicacion': 'Evaluación básica completada'
            }
        
        except Exception as e:
            print(f"❌ Error en obtener_resultados: {e}")
            import traceback
            traceback.print_exc()
            return {
                'cumple': False,
                'aspectos_cumplidos': [],
                'aspectos_incumplidos': ['Error en evaluación'],
                'recomendaciones': ['Contactar soporte técnico'],
                'explicacion': f'Error: {str(e)}'
            }
    
    def _extraer_cumplimientos(self):
        """Extrae cumplimientos de los hechos"""
        cumplimientos = []
        for fact in self.facts.values():
            if hasattr(fact, 'get') and fact.get('tipo') == 'cumplimiento':
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