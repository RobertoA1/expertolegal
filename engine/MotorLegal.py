from experta import KnowledgeEngine
from utils.cargarHechos import leerHechosDePaquete

def getEngine():
    class MotorLegal(KnowledgeEngine):
        pass

    hechos = leerHechosDePaquete('knowledge')
    for i, funcionRegla in enumerate(hechos):
        metodo = funcionRegla()
        setattr(MotorLegal, f'regla_{i}', metodo)

    return MotorLegal()