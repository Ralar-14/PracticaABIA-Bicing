import abia_bicing
from abia_bicing import Estaciones, Estacion
from Bicing_problem_parameters import ProblemParameters
import heapq
# 
class Furgoneta(object):
    def __init__(self, id: int, origen: Estacion, ToGo: list = [None, None], carga: list = [0, 0]) -> None:
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
        self.__genera_furgonetes_senzill() # Genera furgonetas de manera sencilla (cambiar a greedy si hace falta)
    
    def __genera_furgonetas(self):
        # Genera furgonetas con el algoritmo greedy haciendo dos heaps
        h_sobran = []
        h_faltan = []
        for est in self.estaciones.lista_estaciones:
            bicis_sobrantes = est.num_bicicletas_next - est.demanda
            heapq.heappush(h_faltan, (bicis_sobrantes,est))
            heapq.heappush(h_sobran, (-bicis_sobrantes,est))

        # Genera furgonetas con el algoritmo greedy
        for i in range(self.num_furgonetas):
            bicis_sobrantes = -h_sobran[0][0]
            carga = [bicis_sobrantes if bicis_sobrantes <= 30 else 30, 0]
            self.lista_furgonetas.append(Furgoneta(i, self.heap[0][1],  carga))
            h_sobran[0][0] = -(bicis_sobrantes - carga[0])
            heapq.heapify(h_sobran)

        # Asigna los destinos teniendo en cuenta las bicis que les faltan
        for furgo in self.lista_furgonetas:
            furgo.ToGo[0] = h_faltan[0][1]
            heapq.heapify(h_faltan)

        for furgo in self.lista_furgonetas:
            furgo.ToGo[1] = h_faltan[0][1]
            heapq.heapify(h_faltan)


    # Genera furgonetas de manera sencilla, por orden de estaciones
    def __genera_furgonetes_senzill(self):
        i = 0
        a = 0
        while i < self.num_furgonetas:
            self.lista_furgonetas.append(Furgoneta(i, self.estaciones.lista_estaciones[a], [self.estaciones.lista_estaciones[a+1], self.estaciones.lista_estaciones[a+2]]))
            a += 3
            i += 1

    def __repr__(self):
        return f"Furgonetas({self.lista_furgonetas}, \n \n{self.estaciones})"
    
print(Furgonetas(10, Estaciones(10, 100, 1)))
    
