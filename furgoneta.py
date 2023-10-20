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
        if carga[0] > self.max_bicis:
            carga[0] = 30 #"La carga no puede ser mayor que la capacidad de la furgoneta"
    #No puede haber mas de 20 furgonetas"
        
    def get_origen(self):
        return self.origen
    
    def __repr__(self) -> str:
        return f"Furgoneta({self.id}, {self.origen}, {self.ToGo}, {self.carga})"
    
class Furgonetas(object):
    def __init__(self, num_furgonetas: int, estaciones: Estaciones) -> None:
        self.num_furgonetas = num_furgonetas
        self.estaciones = estaciones
        self.lista_furgonetas = []
        self.__genera_furgonetas_greedy() # Genera furgonetas de manera sencilla (cambiar a greedy si hace falta)
    
    def __genera_furgonetas_meh(self):
        # Ordenamos las estaciones segun el numero de bicicletas sobrantes que tienen
        self.estaciones.lista_estaciones.sort(key=lambda x: x.num_bicicletas_next - x.demanda, reverse=True)
        i = 0
        a = 0
        while i < self.num_furgonetas:
            self.lista_furgonetas.append(Furgoneta(i, self.estaciones.lista_estaciones[a]))
            i += 1
            a += 1

    def __genera_furgonetas_greedy(self):     
        # Genera furgonetas con el algoritmo greedy haciendo dos heaps
        h_sobran = []
        h_faltan = []
        for i, est in enumerate(self.estaciones.lista_estaciones):
            bicis_sobrantes = est.num_bicicletas_next - est.demanda
            heapq.heappush(h_faltan, [bicis_sobrantes,i,est]) #Minheap bicis falten
            heapq.heappush(h_sobran, [-bicis_sobrantes,i,est]) #Maxheap bicis sobran

        # Genera furgonetas con el algoritmo greedy
        for i in range(self.num_furgonetas):
            bicis_sobrantes = -h_sobran[0][0]

            if 0 < min(bicis_sobrantes,h_sobran[0][2].num_bicicletas_no_usadas):
                carga = [min(bicis_sobrantes, h_sobran[0][2].num_bicicletas_no_usadas, 30), 0]
            else:
                carga = [0,0]
            #Genera el origen de las furgonetas y su carga inicial
            self.lista_furgonetas.append(Furgoneta(i, h_sobran[0][2], carga))
            h_sobran[0][0] = -(bicis_sobrantes - carga[0])
            heapq.heapify(h_sobran)

        # Asigna los destinos teniendo en cuenta las bicis que les faltan
        for furgo in self.lista_furgonetas:
            furgo.ToGo[0] = h_faltan[0][2]
            heapq.heapify(h_faltan)

        for furgo in self.lista_furgonetas:
            furgo.ToGo[1] = h_faltan[0][2]
            heapq.heapify(h_faltan)
        
        for furgo in self.lista_furgonetas:
            bicis_faltan = furgo.ToGo[0].demanda - furgo.ToGo[0].num_bicicletas_next
            if bicis_faltan > 0:
                furgo.carga[1] = (furgo.carga[0] - min(furgo.carga[0],bicis_faltan)) 
            else:
                furgo.carga[1] = furgo.carga[0] 

    # Genera furgonetas de manera sencilla, por orden de estaciones
    def __genera_furgonetes_senzill(self):
        i = 0
        a = 0
        while i < self.num_furgonetas:
            if a >= len(self.estaciones.lista_estaciones)-3:
                a = 0
            self.lista_furgonetas.append(Furgoneta(i, self.estaciones.lista_estaciones[a], [self.estaciones.lista_estaciones[a+1], self.estaciones.lista_estaciones[a+2]]))
            a += 3
            i += 1

    def profit(self):
        profit = 0
        lista_estaciones_demanda = {}
        for estacion in self.estaciones.lista_estaciones:
            lista_estaciones_demanda[estacion] = estacion.num_bicicletas_next - estacion.demanda

        for furgoneta in self.lista_furgonetas:
            if (furgoneta.ToGo[0] is not None and furgoneta.ToGo[0] in lista_estaciones_demanda and (furgoneta.carga[0] - furgoneta.carga[1] <= lista_estaciones_demanda[furgoneta.ToGo[0]])):
                profit += furgoneta.carga[0] - furgoneta.carga[1]
            elif furgoneta.ToGo[0] in lista_estaciones_demanda and lista_estaciones_demanda[furgoneta.ToGo[0]] > 0:
                profit += lista_estaciones_demanda[furgoneta.ToGo[0]]

            if (furgoneta.ToGo[1] is not None and furgoneta.ToGo[1] in lista_estaciones_demanda and (furgoneta.carga[1] <= lista_estaciones_demanda[furgoneta.ToGo[1]])):
                profit += furgoneta.carga[1]
            elif furgoneta.ToGo[1] in lista_estaciones_demanda and lista_estaciones_demanda[furgoneta.ToGo[1]] > 0:
                profit += lista_estaciones_demanda[furgoneta.ToGo[1]]

        return profit
    
    def __repr__(self) -> str:
        return f"Furgonetas({self.num_furgonetas}, {self.lista_furgonetas})"
    
