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
    
class CambiarDestino(ProblemaOperator):
    """
    Classe que representa una acción de mover una furgoneta de una estación a otra
    """
    def __init__(self, furgoneta: Furgoneta, estacion_parada: Estacion, new_estacion: Estacion):
        self.furgoneta = furgoneta
        self.estacion_parada = estacion_parada
        self.new_estacion = new_estacion


    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su destino {self.estacion_parada} a {self.new_estacion})"
    
class SwapDestino(ProblemaOperator):
    """
    Classe que representa una acción de intercambiar dos furgonetas de una estación a otra
    """
    def __init__(self, furgoneta1: Furgoneta, parada_furgo1: int, furgoneta2: Furgoneta, parada_furgo2: int):
        self.furgoneta1 = furgoneta1
        self.furgoneta2 = furgoneta2
        self.parada_furgo1 = parada_furgo1
        self.parada_furgo2 = parada_furgo2

    def __repr__(self) -> str:
        return f"{self.furgoneta1} cambia su destino número {self.parada_furgo1}, por el destino número {self.parada_furgo2} de {self.furgoneta2})"
    
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
    def __init__(self, furgoneta: Furgoneta, parada: Estacion):
        self.furgoneta = furgoneta
        self.parada = parada

    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su carga en la parada {self.parada}"
    
class NuevaCarga(ProblemaOperator):
    def __init__(self, furgoneta: Furgoneta, parada: int, nueva_carga: int):
        self.furgoneta = furgoneta
        self.parada = parada
        self.nueva_carga = nueva_carga

    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su carga en la parada {self.parada} a {self.nueva_carga}"
    
class CambiarDestinoYCarga(ProblemaOperator):
    def __init__(self, furgoneta: Furgoneta, estacion_parada: int, new_estacion: Estacion, nueva_carga: int, carga_to_change: int):
        self.furgoneta = furgoneta
        self.estacion_parada = estacion_parada
        self.new_estacion = new_estacion
        self.nueva_carga = nueva_carga
        self.carga_to_change = carga_to_change

    def __repr__(self) -> str:
        return f"{self.furgoneta} cambia su destino {self.estacion_parada} a {self.new_estacion} y su carga a {self.nueva_carga})"
        
    
class MultiOperator(ProblemaOperator):
    def __init__(self, operator: ProblemaOperator, operator2: ProblemaOperator):
        self.operator = operator
        self.operator2 = operator2
    
    def __repr__(self) -> str:
        return f"{self.operator} y {self.operator2}"
    

