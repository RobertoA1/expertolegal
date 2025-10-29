from engine.MotorLegal import getEngine
from experta import engine
from ui.app import main


# Llamando a streamlit para ejecutar la aplicación
if __name__ == "__main__":
    main()


PAQUETE_REGLAS = 'knowledge'

motorLegal = getEngine()
motorLegal.reset()
motorLegal.declare(engine.Fact(edad=12, tiene_consentimiento=False))
motorLegal.run()