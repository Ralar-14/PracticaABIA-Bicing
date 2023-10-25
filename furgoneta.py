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
    estaciones: Estaciones = None

    def __init__(self, num_furgonetas: int) -> None:
        self.num_furgonetas = num_furgonetas
        self.lista_furgonetas = []
        self.__genera_furgonetes_senzill() # Genera furgonetas de manera sencilla (cambiar a greedy si hace falta)

    def __genera_furgonetas_meh(self):
        # Ordenamos las estaciones segun el numero de bicicletas sobrantes que tienen
        Furgonetas.estaciones.lista_estaciones.sort(key=lambda x: x.num_bicicletas_next - x.demanda, reverse=True)
        i = 0
        a = 0
        while i < self.num_furgonetas:
            self.lista_furgonetas.append(Furgoneta(i, Furgonetas.estaciones.lista_estaciones[a]))
            i += 1
            a += 1

    def __genera_furgonetas_greedy(self):     
        # Genera furgonetas con el algoritmo greedy haciendo dos heaps
        h_sobran = []
        h_faltan = []
        for i, est in enumerate(Furgonetas.estaciones.lista_estaciones):
            bicis_sobrantes = est.num_bicicletas_next - est.demanda #Si es negativo, faltan bicis, si es positivo, sobran
            heapq.heappush(h_faltan, [bicis_sobrantes,i,est]) #Minheap bicis faltan
            heapq.heappush(h_sobran, [-bicis_sobrantes,i,est]) #Maxheap bicis sobran
            
        #print("heap sobran: \n", h_sobran)
        #print("heap faltan: \n", h_faltan)
        
        # Genera furgonetas con el algoritmo greedy
        for i in range(self.num_furgonetas):
            bicis_sobrantes = - h_sobran[0][0] #Puede ser negativo!!!!
        
            if 0 < min(bicis_sobrantes,h_sobran[0][2].num_bicicletas_no_usadas, 30):
                Carga = [min(bicis_sobrantes, h_sobran[0][2].num_bicicletas_no_usadas, 30), 0] #sí que es positivo
            else:
                Carga = [0,0]
            #Genera el origen de las furgonetas y su carga inicial
            self.lista_furgonetas.append(Furgoneta(i, h_sobran[0][2], carga=Carga))
            h_sobran[0][0] = -(bicis_sobrantes - Carga[0])
            heapq.heapify(h_sobran)

        # Asigna los destinos teniendo en cuenta las bicis que les faltan
        for furgo in self.lista_furgonetas:
            furgo.ToGo[0] = h_faltan[0][2]
            bicis_faltan = - h_faltan[0][0] #Si es negativo, sobran bicis, si es positivo, faltan
            if bicis_faltan > 0:
                furgo.carga[1] = (furgo.carga[0] - min(furgo.carga[0],bicis_faltan)) 
            else:
                furgo.carga[1] = furgo.carga[0]

            h_faltan[0][0] = -(bicis_faltan - (furgo.carga[0]-furgo.carga[1]))
            heapq.heapify(h_faltan)

        for furgo in self.lista_furgonetas:
            furgo.ToGo[1] = h_faltan[0][2]
            bicis_faltan = -h_faltan[0][0]
            h_faltan[0][0] = -(bicis_faltan - furgo.carga[1])
            heapq.heapify(h_faltan)
        print("Furgonetas: \n", self.lista_furgonetas)

    # Genera furgonetas de manera sencilla, por orden de estaciones
    def __genera_furgonetes_senzill(self):
        i = 0
        a = 0
        while i < self.num_furgonetas:
            if a >= len(Furgonetas.estaciones.lista_estaciones)-3:
                a = 0
            self.lista_furgonetas.append(Furgoneta(i, Furgonetas.estaciones.lista_estaciones[a], [Furgonetas.estaciones.lista_estaciones[a+1], Furgonetas.estaciones.lista_estaciones[a+2]], carga= [0,0]))
            a += 3
            i += 1
    
    def profit(self):
        profit = 0
        lista_estaciones_demanda = {}
        for estacion in Furgonetas.estaciones.lista_estaciones:
            lista_estaciones_demanda[estacion] = estacion.demanda - estacion.num_bicicletas_next #Si es negativo, faltan bicis, si es positivo, sobran

        for furgoneta in self.lista_furgonetas:
            if (furgoneta.ToGo[0] is not None and furgoneta.ToGo[0] in lista_estaciones_demanda and (furgoneta.carga[0] - furgoneta.carga[1] <= lista_estaciones_demanda[furgoneta.ToGo[0]])):
                profit += (furgoneta.carga[0] - furgoneta.carga[1])
                lista_estaciones_demanda[furgoneta.ToGo[0]] -= (furgoneta.carga[0] - furgoneta.carga[1])

            elif furgoneta.ToGo[0] in lista_estaciones_demanda and lista_estaciones_demanda[furgoneta.ToGo[0]] > 0:
                profit += lista_estaciones_demanda[furgoneta.ToGo[0]]
                lista_estaciones_demanda[furgoneta.ToGo[0]] = 0

            if (furgoneta.ToGo[1] is not None and furgoneta.ToGo[1] in lista_estaciones_demanda and (furgoneta.carga[1] <= lista_estaciones_demanda[furgoneta.ToGo[1]])):
                profit += furgoneta.carga[1]
                lista_estaciones_demanda[furgoneta.ToGo[1]] -= furgoneta.carga[1]

            elif furgoneta.ToGo[1] in lista_estaciones_demanda and lista_estaciones_demanda[furgoneta.ToGo[1]] > 0:
                profit += lista_estaciones_demanda[furgoneta.ToGo[1]]
                lista_estaciones_demanda[furgoneta.ToGo[1]] = 0
        return profit

    
    """
    def profit(self):
        profit = 0
        lista_estaciones_demanda = {}
        for estacion in Furgonetas.estaciones.lista_estaciones:
            lista_estaciones_demanda[estacion] = estacion.num_bicicletas_next - estacion.demanda

        for furgoneta in self.lista_furgonetas:
            if (furgoneta.ToGo[0] is not None and furgoneta.ToGo[0] in Furgonetas.estaciones.lista_estaciones and (furgoneta.carga[0] - furgoneta.carga[1] <= lista_estaciones_demanda[furgoneta.ToGo[0]])):
                profit += (furgoneta.carga[0] - furgoneta.carga[1])
            elif furgoneta.ToGo[0] in lista_estaciones_demanda and lista_estaciones_demanda[furgoneta.ToGo[0]] > 0:
                profit += lista_estaciones_demanda[furgoneta.ToGo[0]]
            else:
                pass

            if (furgoneta.ToGo[1] is not None and furgoneta.ToGo[1] in Furgonetas.estaciones.lista_estaciones and furgoneta.carga[1] <= lista_estaciones_demanda[furgoneta.ToGo[1]]):
                profit += furgoneta.carga[1] 
            elif (furgoneta.ToGo[1] is not None and furgoneta.ToGo[1] in Furgonetas.estaciones.lista_estaciones and lista_estaciones_demanda[furgoneta.ToGo[1]] > 0):
                profit += lista_estaciones_demanda[furgoneta.ToGo[1]]
            else:
                pass
        return profit
    """
    """
    def profit(self): #profit diferente
        beneficis = 0
        for f in self.lista_furgonetas:
            if f.ToGo[0] is not None:
                if f.ToGo[0].num_bicicletas_next + (f.carga[0]-f.carga[1]) <= f.ToGo[0].demanda:
                    beneficis += (f.carga[0]-f.carga[1]) #Es positivo pq carga[0] > 0 y carga[1] <= carga[0]
                else:
                    beneficis += (f.ToGo[0].demanda - f.ToGo[0].num_bicicletas_next) if (f.ToGo[0].num_bicicletas_next < f.ToGo[0].demanda) else 0
                    
            if f.ToGo[1] is not None:
                if f.ToGo[1].num_bicicletas_next + (f.carga[1]) <= f.ToGo[1].demanda:
                    beneficis += (f.carga[1])
                else:
                    beneficis += (f.ToGo[1].demanda - f.ToGo[1].num_bicicletas_next) if (f.ToGo[1].num_bicicletas_next < f.ToGo[1].demanda) else 0
        return beneficis
    """
    """
    def __repr__(self) -> str:
        return f"Furgonetas({self.num_furgonetas}, {self.lista_furgonetas})"
    """
