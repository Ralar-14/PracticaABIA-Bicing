from furgoneta import Furgoneta
from abia_bicing import Estacion, Estaciones

class FurgonetaAction(object):
    """
    Classe abstracta que representa una acción posible de la furgoneta
    """
    pass

class MoveTo(FurgonetaAction):
    """
    Clase que representa la acción de mover la furgoneta a una estación
    """
    def __init__(self, estacionIni: Estacion, estacionFin: Estacion, furgoneta: Furgoneta):
        """
        Constructora de MoveTo
        * estacion: identificador de la estación a la que se mueve la furgoneta
        """
        self.estacionIni: Estacion = estacionIni
        self.estacionFin: Estacion = estacionFin
        self.furgoneta: Furgoneta = furgoneta

    def __str__(self) -> str:
        return "{self.furgoneta} moved from {self.estacionIni} to {self.estacionFin}"

    def __repr__(self) -> str:
        return self.__str__()
    
class Descargar(FurgonetaAction):
    """
    Clase que representa la acción de descargar bicicletas de la furgoneta
    """
    def __init__(self, estacion: Estacion, num_bicicletas: int, furgoneta: Furgoneta):
        """
        Constructora de Descargar
        * estacion: identificador de la estación a la que se mueve la furgoneta
        * num_bicicletas: número de bicicletas a descargar
        """
        self.estacion: Estacion = estacion
        self.num_bicicletas: int = num_bicicletas
        self.furgoneta: Furgoneta = furgoneta

    def __str__(self) -> str:
        return "{self.furgoneta} unloaded {self.num_bicicletas} bikes at {self.estacion}"

    def __repr__(self) -> str:
        return self.__str__()
    
class Cargar(FurgonetaAction):
    """
    Clase que representa la acción de cargar bicicletas en la furgoneta
    """
    def __init__(self, estacion: Estacion, num_bicicletas: int, furgoneta: Furgoneta):
        """
        Constructora de Cargar
        * estacion: identificador de la estación a la que se mueve la furgoneta
        """
        self.estacion: Estacion = estacion
        self.num_bicicletas: int = num_bicicletas
        self.furgoneta: Furgoneta = furgoneta
        
    def __str__(self) -> str:
        return "{self.furgoneta} loaded {self.num_bicicletas} bikes at {self.estacion}"
    
    def __repr__(self) -> str:
        return self.__str__()
        