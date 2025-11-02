# Compatibilidad Python 3.10+: asegurar collections.Mapping para librerías antiguas (p.ej., experta)
import collections
import collections.abc as _collections_abc

if not hasattr(collections, "Mapping"):
    collections.Mapping = _collections_abc.Mapping
