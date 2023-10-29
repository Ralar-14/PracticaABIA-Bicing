from typing import List


class ProblemParameters(object):
    def __init__(self, num_bicicletas: int, num_furgonetas: int, num_estaciones: int, seed: int = 1, initial_strat: int = 0, free_gas: bool = False):
        self.num_bicicletas = num_bicicletas
        self.num_furgonetas = num_furgonetas
        self.num_estaciones = num_estaciones 
        self.seed = seed
        self.inital_strat = initial_strat
        self.free_gas = free_gas

    def __repr__(self):
        return f"Params(num_bicicletas={self.num_bicicletas}, num_furgonetas={self.num_furgonetas}, num_estaciones={self.num_estaciones})"
    
    def __str__(self):
        return self.__repr__()