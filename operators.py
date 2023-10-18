from furgoneta import Furgoneta
from abia_bicing import Estacion, Estaciones

class ProblemaOperator(object):
    """
    Classe abstracta que representa una acción posible de la furgoneta
    """
    pass

class CambiarOrigen(ProblemaOperator):
    """
    Classe que representa una acción de cambiar el origen de una furgoneta
    """
    def __init__(self, furgoneta: Furgoneta, new_origen: Estacion):
        self.furgoneta = furgoneta
        self.new_origen = new_origen

    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su origen a {self.new_origen})"
    
class CambiarOrigenYCarga(ProblemaOperator):
    """
    Classe que representa una acción de cambiar el origen de una furgoneta
    """
    def __init__(self, furgoneta: Furgoneta, new_origen: Estacion, new_carga: int):
        self.furgoneta = furgoneta
        self.new_origen = new_origen

    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su origen a {self.new_origen} y su carga en esa posición a {self.new_carga})"

class CambiarDestino(ProblemaOperator):
    """
    Classe que representa una acción de mover una furgoneta de una estación a otra
    """
    def __init__(self, furgoneta: Furgoneta, parada: int, estacion: Estacion):
        self.furgoneta = furgoneta
        self.parada = parada
        self.estacion = estacion


    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su destino {self.parada} a {self.estacion})"
    
class CambiarDestinoYCarga(ProblemaOperator):
    """
    Classe que representa una acción de mover una furgoneta de una estación a otra
    """
    def __init__(self, furgoneta: Furgoneta, parada: int, estacion: Estacion, new_carga: int):
        self.furgoneta = furgoneta
        self.parada = parada
        self.estacion = estacion
        self.new_carga = new_carga

    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su destino {self.parada} a {self.estacion} y su carga en esa posición a {self.new_carga})"
    
class AñadirParada(ProblemaOperator):
    """
    Classe que representa una acción de añadir una parada a una furgoneta
    """
    def __init__(self, furgoneta: Furgoneta, estacion: Estacion):
        self.furgoneta = furgoneta
        self.estacion = estacion

    def __repr__(self) -> str:
        return f"{self.furgoneta} añade una parada en {self.estacion})"
    
class SwapDestino(ProblemaOperator):
    """
    Classe que representa una acción de intercambiar dos furgonetas de una estación a otra
    """
    def __init__(self, furgoneta1: Furgoneta, estacion_furgo1: int, furgoneta2: Furgoneta, estacion_furgo2: int):
        self.furgoneta1 = furgoneta1
        self.furgoneta2 = furgoneta2
        self.estacion_furgo1 = estacion_furgo1
        self.estacion_furgo2 = estacion_furgo2

    def __repr__(self) -> str:
        return f"{self.furgoneta1} cambia su destino número {self.estacion_furgo1}, por el destino número {self.estacion_furgo2} de {self.furgoneta2})"
    
class EliminarParada(ProblemaOperator):
    """
    Classe que representa una acción de eliminar una parada de una furgoneta
    """
    def __init__(self, furgoneta: Furgoneta, parada: int):
        self.furgoneta = furgoneta
        self.parada = parada

    def __repr__(self) -> str:
        return f"{self.furgoneta} elimina su parada número {self.parada})"
    
class CambiarCargaODescarga(ProblemaOperator):
    """
    Classe que representa una acción de cambiar la carga de una furgoneta
    """
    def __init__(self, furgoneta: Furgoneta, carga: tuple, parada: int):
        self.furgoneta = furgoneta
        self.carga = carga
        self.parada = parada
        assert parada <= 1, "No se puede modificar el número de bicis que se descargan en la última parada"

    def __repr__(self) -> str:
        if self.parada == 0:
            return f"{self.furgoneta} cambia su carga a {self.carga} en la parada de origen)"
        else:
            return f"{self.furgoneta} cambia su carga a {self.carga} en la parada 1 (Dejando {self.furgoneta.carga[0]-self.fur})"
    

