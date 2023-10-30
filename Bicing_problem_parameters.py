from typing import List

class ProblemParameters(object):
    def __init__(self, num_bicicletas: int, num_furgonetas: int, num_estaciones: int, seed: int = 1, initial_strat: int = 0, free_gas: bool = False, operators_used: List[int] = [1]*6): #Operators used es una lista de 6 elementos, cada uno de los cuales es 0 o 1, indicando si se usa o no el operador correspondiente (una vez acabada la práctica, no se usa, lo dejamos para que se pueda ver como se ha hecho el experimento 1)
        self.num_bicicletas = num_bicicletas
        self.num_furgonetas = num_furgonetas
        self.num_estaciones = num_estaciones 
        self.seed = seed
        self.inital_strat = initial_strat
        self.free_gas = free_gas
        self.operators_used = operators_used

    def __repr__(self):
        return f"Params(num_bicicletas={self.num_bicicletas}, num_furgonetas={self.num_furgonetas}, num_estaciones={self.num_estaciones})"
    
    def __str__(self):
        return self.__repr__()