import abia_bicing
from abia_bicing import Estaciones, Estacion
from Bicing_problem_parameters import ProblemParameters

# 
class Furgoneta(object):
    def __init__(self, id: int, origen: tuple, ToGo: list = [(-1, -1), (-1, -1)], carga: tuple = [0, 0]) -> None:
        self.max_bicis = 30
        self.id = id
        self.origen = origen
        self.ToGo = ToGo
        self.carga = carga
        self.movimientos = 0
        assert carga <= self.max_bicis, "La carga no puede ser mayor que la capacidad de la furgoneta"
        assert id <= 20, "No puede haber mas de 20 furgonetas"
        
    def get_origen(self):
        return self.origen
        
    def __repr__(self):
        return f"Furgoneta {self.id}, origen: {self.origen}, carga: {self.carga}"
    
class Furgonetas(object):
    def __init__(self, num_furgonetas: int, estaciones: Estaciones) -> None:
        self.num_furgonetas = num_furgonetas
        self.estaciones = estaciones
        self.lista_furgonetas = []
        self.__genera_furgonetas()
        
    def __genera_furgonetas(self):
        # Ordenamos las estaciones segun el numero de bicicletas sobrantes que tienen
        self.estaciones.lista_estaciones.sort(key=lambda x: x.num_bicicletas_next - x.demanda, reverse=True)
        
        for i in range(self.num_furgonetas):
            bicis_sobrantes = self.estaciones.lista_estaciones[i].num_bicicletas_next - self.estaciones.lista_estaciones[i].demanda
            self.lista_furgonetas.append(Furgoneta(i, self.estaciones.lista_estaciones[i].get_origen(), carga = [bicis_sobrantes if bicis_sobrantes <= 30 else 30, 0]))
            # Actualizar heap de llista.estaciones
        
        self.estaciones.lista_estaciones.reverse()

        for i, furgo in enumerate(self.lista_furgonetas):
            furgo.ToGo[0] = self.estaciones.lista_estaciones[furgo].get_posicion()
            furgo.carga[1] = furgo.carga[0] - (self.estaciones.lista_estaciones[furgo].demanda - self.estaciones.lista_estaciones[furgo].next)
            self.estaciones.lista_estaciones[furgo].num_bicicletas_next -= furgo.carga[1]
            
            if furgo.carga[1] > 0:
                furgo.ToGo[1] = self.estaciones.lista_estaciones[i + 1].get_posicion()
                


    def __repr__(self):
        return f"Furgonetas({self.lista_furgonetas}, \n \n{self.estaciones})"
    
print(Furgonetas(10, Estaciones(10, 100, 1)))
    
