"""
Reglas de experta para Normativa Ambiental (Ley General del Ambiente - Ley N° 28611) 🌿
Enfoque: Instrumentos de Gestión Ambiental (IGA/IEGA), Licencias y Cumplimiento de ECA/LMP.
"""

from experta import *

class AspectoAmbiental(Fact):
    # Hechos sobre la situacion ambiental de la empresa
    
    # 1. Evaluación de Impacto Ambiental (Ley 27446 / Ley 28611)
    # IEGA: Instrumento de Gestión Ambiental (DIA, EIA-sd, EIA-d)
    tiene_IEGA_aprobado = Field(bool, default=False) 
    
    # 2. Fiscalización y Monitoreo
    # Plan de monitoreo e informes periódicos a OEFA/autoridad sectorial
    monitoreo_ambiental_activo = Field(bool, default=False) 
    
    # 3. Cumplimiento de Estándares
    # Límites Máximos Permisibles y Estándares de Calidad Ambiental
    cumple_LMP_ECA = Field(bool, default=False) 
    
    # 4. Licencias Específicas (ejemplos)
    # Registro de generador o manejo de residuos no municipales
    tiene_registro_residuos_solidos = Field(bool, default=False) 
    # Autorización de vertimientos de agua (ANA) u otra licencia sectorial
    tiene_autorizacion_vertimientos = Field(bool, default=False) 

class ResultadoEvaluacionAmbiental(Fact):
    # Almacena Resultados de la evaluación de Normativa Ambiental
    cumple_ambiental = Field(bool, default=True) 
    aspectos_cumplidos = Field(list, default=[])
    aspectos_incumplidos = Field(list, default=[])
    recomendaciones = Field(list, default=[])
    explicacion = Field(str, default="")

class NormativaAmbientalKB(KnowledgeEngine):
    """Motor de inferencia para Ley 28611 - Ley General del Ambiente"""

    def __init__(self):
        super().__init__()
        self.explicaciones = []
        self.recomendaciones_generadas = []
    
    @DefFacts()
    def inicializar(self):
        """Inicializar el resultado de la evaluacion"""
        yield ResultadoEvaluacionAmbiental()
    
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
        if resultado_fact and resultado_fact.get('cumple_ambiental'):
             self.modify(self.facts[1], cumple_ambiental = False)

    def _registrar_cumplimiento(self, aspecto, descripcion):
        """Registra un cumplimiento"""
        self.declare(Fact(
            tipo="cumplimiento",
            aspecto=aspecto,
            descripcion=descripcion
        ))
        self.explicaciones.append(f"CUMPLE: Se identificó {aspecto}.")


    # --- REGLAS DE EVALUACIÓN DE OBLIGACIONES CLAVE ---
    
    # 1. Instrumento de Gestión Ambiental (IEGA) (CRÍTICO)
    @Rule(
        AspectoAmbiental(tiene_IEGA_aprobado=False),
        ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_IEGA(self):
        """Verifica la existencia del Instrumento de Gestión Ambiental (DIA, EIA, etc.)"""
        self._registrar_incumplimiento(
            aspecto="Instrumento de Gestión Ambiental (IEGA)",
            descripcion="Todo proyecto o actividad con potencial impacto ambiental debe contar con un IEGA (DIA, EIA-sd, EIA-d) aprobado por la autoridad sectorial competente (SENACE/Sector).",
            base_legal="Art. 28, Ley 28611 / Ley 27446 (SEIA)",
            severidad="crítica", 
            recomendacion_texto="Determinar la categoría del proyecto (SEIA) y tramitar la aprobación del Instrumento de Gestión Ambiental correspondiente (DIA o EIA)."
        )

    @Rule(AspectoAmbiental(tiene_IEGA_aprobado=True), ResultadoEvaluacionAmbiental())
    def cumple_IEGA(self):
        self._registrar_cumplimiento("Instrumento de Gestión Ambiental (IEGA)", "El proyecto cuenta con IEGA (DIA/EIA) aprobado y vigente.")

    # 2. Cumplimiento de LMP y ECA (CRÍTICO)
    @Rule(
        AspectoAmbiental(cumple_LMP_ECA=False),
        ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def incumplimiento_LMP_ECA(self):
        """Verifica el cumplimiento de los Límites Máximos Permisibles (LMP) y Estándares de Calidad Ambiental (ECA)"""
        self._registrar_incumplimiento(
            aspecto="Límites Máximos Permisibles (LMP) y ECA",
            descripcion="Se han detectado valores de vertimiento/emisión (LMP) o de calidad del entorno (ECA) que superan los límites establecidos, resultando en contaminación o riesgo ambiental.",
            base_legal="Art. 34, Ley 28611",
            severidad="crítica",
            recomendacion_texto="Implementar medidas correctivas y tecnológicas (PAMA) para garantizar que las emisiones y efluentes cumplan con los LMP sectoriales vigentes y que no se afecte la calidad ambiental (ECA)."
        )

    @Rule(AspectoAmbiental(cumple_LMP_ECA=True), ResultadoEvaluacionAmbiental())
    def cumple_LMP_ECA(self):
        self._registrar_cumplimiento("LMP y ECA", "Se cumplen los Límites Máximos Permisibles y los Estándares de Calidad Ambiental en los monitoreos.")

    # 3. Monitoreo Ambiental y Reporte (ALTA)
    @Rule(
        AspectoAmbiental(monitoreo_ambiental_activo=False),
        ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_monitoreo(self):
        """Verifica la ejecución y reporte del monitoreo ambiental"""
        self._registrar_incumplimiento(
            aspecto="Monitoreo y Reporte Ambiental",
            descripcion="El plan de monitoreo ambiental, detallado en el IEGA, no se está ejecutando o los informes no se presentan periódicamente a la autoridad fiscalizadora (OEFA/Sector).",
            base_legal="D.S. 004-2017-MINAM (Reglamento OEFA)",
            severidad="alta",
            recomendacion_texto="Establecer un Plan de Monitoreo Ambiental continuo y presentar los Informes de Monitoreo Ambiental (IMA) según la periodicidad exigida por la autoridad competente."
        )

    @Rule(AspectoAmbiental(monitoreo_ambiental_activo=True), ResultadoEvaluacionAmbiental())
    def cumple_monitoreo(self):
        self._registrar_cumplimiento("Monitoreo Ambiental Activo", "El programa de monitoreo se ejecuta y se reporta a la autoridad competente.")

    # 4. Gestión de Residuos Sólidos (MEDIA/ALTA)
    @Rule(
        AspectoAmbiental(tiene_registro_residuos_solidos=False),
        ResultadoEvaluacionAmbiental(cumple_ambiental=True)
    )
    def falta_registro_residuos(self):
        """Verifica el registro de generador o el Plan de Manejo de Residuos Sólidos"""
        self._registrar_incumplimiento(
            aspecto="Registro y Plan de Residuos Sólidos",
            descripcion="No se cuenta con el Plan de Manejo de Residuos Sólidos ni con el registro de generador (declaración anual de residuos).",
            base_legal="D.L. 1278 (Ley de Gestión Integral de Residuos Sólidos)",
            severidad="media",
            recomendacion_texto="Implementar un Plan de Manejo de Residuos Sólidos (municipales y no municipales) y realizar la Declaración Anual de Residuos no Municipales (D.A.R.)."
        )

    @Rule(AspectoAmbiental(tiene_registro_residuos_solidos=True), ResultadoEvaluacionAmbiental())
    def cumple_registro_residuos(self):
        self._registrar_cumplimiento("Registro de Residuos Sólidos", "Se lleva un Plan de Manejo de Residuos Sólidos y se ha cumplido con la Declaración Anual.")

    # ------ REGLA DE SINTESIS --------

    @Rule(
        ResultadoEvaluacionAmbiental(cumple_ambiental = MATCH.cumple),
        salience = -100
    )
    def generar_resultado_final(self, cumple):
        """Generar el resumen final de evaluacion para Ley 28611"""
        cumplimientos = []
        incumplimientos = []
        
        for fact in self.facts.values():
            if isinstance(fact, Fact):
                if fact.get('tipo') in ['cumplimiento']:
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
            cumple_ambiental = cumple,
            aspectos_cumplidos = cumplimientos,
            # Se usa una lista de strings para 'aspectos_incumplidos' por simplicidad en el output del engine
            aspectos_incumplidos = [i['aspecto'] for i in incumplimientos],
            recomendaciones = self.recomendaciones_generadas,
            explicacion = explicacion_final
        )

    def obtener_resultados(self):
        """Retorna el resultado de la evaluación"""
        for fact in self.facts.values():
            if isinstance(fact, ResultadoEvaluacionAmbiental):
                return {
                    'cumple_ambiental': fact.get('cumple_ambiental'),
                    'aspectos_cumplidos': fact.get('aspectos_cumplidos'),
                    'aspectos_incumplidos': fact.get('aspectos_incumplidos'),
                    'recomendaciones': fact.get('recomendaciones'),
                    'explicacion': fact.get('explicacion')
                }
        return None
    
    def obtener_explicacion(self):
        """Retorna la explicación de la decisión tomada"""
        return "\n\n".join(self.explicaciones)