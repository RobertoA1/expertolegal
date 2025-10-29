from engine.MotorLegal import getEngine
from experta import engine

PAQUETE_REGLAS = 'knowledge'

motorLegal = getEngine()
motorLegal.reset()
motorLegal.declare(engine.Fact(edad=12, tiene_consentimiento=False))
motorLegal.run()