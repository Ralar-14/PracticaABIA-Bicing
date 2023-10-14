import abia_bicing
from typing import touple

# 
class Furgoneta:
    def __init__(self, id: int, origen: touple, destino1: touple, destino2: touple = None, carga: int = 0) -> None:
        self.max_bicis = 30
        self.id = id
        self.origen = origen
        self.destino = (destino1, destino2)
        self.carga = carga
        assert carga <= self.max_bicis, "La carga no puede ser mayor que la capacidad de la furgoneta"
        assert id >= 20, "No puede haber mas de 20 furgonetas"
    def __str__(self):
        return f"Furgoneta {self.id}, origen: {self.origen}, carga: {self.carga}"
    
