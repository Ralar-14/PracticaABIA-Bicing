from __future__ import annotations
import math
from typing import List, Dict, Generator
from Bicing_problem_parameters import ProblemParameters
from abia_bicing import Estacion, Estaciones
from operators import *
from furgoneta import Furgoneta, Furgonetas
from copy import deepcopy

class StateRepresentation(object):
    def __init__(self, params: ProblemParameters, estaciones = None, furgonetas = None):
        self.params = params
        self.estaciones = estaciones
        self.furgonetas = furgonetas

    def copy(self) -> StateRepresentation:
        estaciones = deepcopy(self.estaciones)
        furgonetas = deepcopy(self.furgonetas)
        return StateRepresentation(self.params, estaciones, furgonetas)
    
    def __repr__(self) -> str:
        return f"{self.params}"
        
    def generate_actions(self) -> Generator[ProblemaOperator, None, None]:
        for furgoneta in self.furgonetas.lista_furgonetas:
            for estacion in self.estaciones.lista_estaciones:
                if furgoneta.origen != estacion:
                    yield CambiarOrigen(furgoneta, estacion)
                    for i in range(min(furgoneta.ToGo[0].num_bicicletas_next - furgoneta.ToGo[0].demanda, furgoneta.ToGo[0].num_bicicletas_no_usadas)):
                        yield CambiarOrigenYCarga(furgoneta, estacion, i)

                    for i in range(furgoneta.carga[0]):
                        yield CambiarOrigenYCarga(furgoneta, estacion, i)

                if furgoneta.ToGo[0] != estacion:
                    yield CambiarDestino(furgoneta, furgoneta.ToGo[0], estacion)

                if furgoneta.ToGo[1] != estacion:
                    yield CambiarDestino(furgoneta, furgoneta.ToGo[1], estacion)
                #if furgoneta.ToGo[1] == None:
                    #yield AñadirParada(furgoneta, estacion)
                             
            #yield EliminarParada(furgoneta, 0)
            #yield EliminarParada(furgoneta, 1)

            for furgoneta2 in self.furgonetas.lista_furgonetas:
                yield SwapDestino(furgoneta, 0, furgoneta2, 0)
                yield SwapDestino(furgoneta, 0, furgoneta2, 1)
                yield SwapDestino(furgoneta, 1, furgoneta2, 0)
                yield SwapDestino(furgoneta, 1, furgoneta2, 1)
                
            for i in range(min(furgoneta.ToGo[0].num_bicicletas_next - furgoneta.ToGo[0].demanda, furgoneta.ToGo[0].num_bicicletas_no_usadas)):
                yield CambiarCargaODescarga(furgoneta, 0, i)
            
            for i in range(furgoneta.carga[0]):    
                yield CambiarCargaODescarga(furgoneta, 1, i)

            

    def apply_action(self, action: ProblemaOperator) -> StateRepresentation:
        new_state = self.copy()
        
        if isinstance(action, CambiarOrigen):
            # Cambia el origen de la furgoneta y de forma 'inteligente' la carga
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].origen = action.new_origen
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] = max(min(new_state.furgonetas.lista_furgonetas[action.furgoneta.id].origen.num_bicicletas_next - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].origen.demanda, new_state.furgonetas.lista_furgonetas[action.furgoneta.id].origen.num_bicicletas_no_usadas, 30), 0)
            if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0] is not None:
                if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] >= new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next >= 0:
                    new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] - \
                    (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next)
                else:
                    new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = 0

        elif isinstance(action, AñadirParada):
            # Añade parada a la furgoneta y actualiza la carga de forma 'inteligente'
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1] = action.estacion
            
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] = max(min(action.estacion.num_bicicletas_next - action.estacion.demanda, action.estacion.num_bicicletas_no_usadas, 30), 0)
            
            if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] >= (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next >= 0):
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] - \
                (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next)
            else:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = 0
            print(new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga)

        elif isinstance(action, EliminarParada):
            # Elimina parada de la furgoneta y actualiza la carga (todas las bicis se descargan en el destino 0)
            if action.parada == 1:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1] = None
            
            else:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1]
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1] = None
                
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = 0 

        elif isinstance(action, CambiarOrigenYCarga):
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].origen = action.new_origen
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] = action.new_carga
            if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] >= (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next) >= 0:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] - \
                (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next)
            else:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = 0

        elif isinstance(action, CambiarDestino):
            # Cambia el destino de la furgoneta pero no la carga
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0] = action.new_estacion

        elif isinstance(action, SwapDestino):
            # Intercambia el destino de dos furgonetas (No toca la carga)
            new_state.furgonetas.lista_furgonetas[action.furgoneta1.id].ToGo[action.parada_furgo1], new_state.furgonetas.lista_furgonetas[action.furgoneta2.id].ToGo[action.parada_furgo2] = action.furgoneta2.ToGo[action.parada_furgo2], action.furgoneta1.ToGo[action.parada_furgo1]
            
        elif isinstance(action, CambiarCargaODescarga):
            # Cambia la carga o descarga de una furgoneta en una estación y actualiza la carga de forma 'inteligente'
            if action.parada == 0:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] = action.carga
                if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] >= (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next) >= 0:
                    new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] - \
                    (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas_next)
                else:
                    new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = 0
                
            else:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = action.carga
            
        return new_state
    
    def heuristic(self):      
        return self.furgonetas.profit()
   
    
def generate_initial_state(params: ProblemParameters) -> StateRepresentation:
    estaciones = Estaciones(params.num_estaciones, params.num_bicicletas, params.seed)
    furgonetas = Furgonetas(params.num_furgonetas, estaciones)
    return StateRepresentation(params, estaciones, furgonetas)
