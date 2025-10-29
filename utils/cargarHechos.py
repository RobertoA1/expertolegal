import pkgutil
import importlib
import inspect
from experta import Fact

def leerHechosDePaquete(nombrePaquete):
    paquete = importlib.import_module(nombrePaquete)
    hechos = {}
    for loader, nombreModulo, esPaquete in pkgutil.iter_modules(paquete.__path__):
        modulo = importlib.import_module(f"{nombrePaquete}.{nombreModulo}")
        for nombre, objeto in inspect.getmembers(modulo, inspect.isclass):
            if issubclass(objeto, Fact) and objeto is not Fact:
                hechos[nombre] = objeto
    return hechos