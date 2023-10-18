from __future__ import annotations
import math
from typing import List, Dict, Generator
from Bicing_problem_parameters import ProblemParameters
from abia_bicing import Estacion, Estaciones
from operators import *
from furgoneta import Furgoneta, Furgonetas

class StateRepresentation(object):
    def __init__(self, params: ProblemParameters):
        self.params = params
        self.estaciones = Estaciones(self.params.num_estaciones, self.params.num_bicicletas, self.params.seed)
        self.furgonetas = Furgonetas(self.params.num_furgonetas, self.estaciones)

    def copy(self) -> StateRepresentation:
        return StateRepresentation(self.params)
    
    def __repr__(self) -> str:
        return f"{self.params}"
        
    def generate_actions(self) -> Generator[ProblemaOperator, None, None]:
        for furgoneta in self.furgonetas.lista_furgonetas:
            for estacion in self.estaciones.lista_estaciones:
                if furgoneta.origen != estacion:
                    yield CambiarOrigen(furgoneta, estacion)
                if furgoneta.ToGo[0] != estacion:
                    yield CambiarDestino(furgoneta, furgoneta.ToGo[0], estacion)
                if furgoneta.ToGo[1] != estacion:
                    yield CambiarDestino(furgoneta, furgoneta.ToGo[1], estacion)
                if furgoneta.ToGo[1] == None:
                    yield AñadirParada(furgoneta, estacion)       
                             
            yield EliminarParada(furgoneta, 0)
            yield EliminarParada(furgoneta, 1)

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
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] = min(action.new_origen.num_bicicletas_next - action.new_origen.demanda, action.new_origen.num_bicicletas_no_usadas, 30)
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] - \
                (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas.next) \
                    if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] >= (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas.next) else 0

        elif isinstance(action, CambiarDestino):
            # Cambia el destino de la furgoneta pero no la carga
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0] = action.new_estacion
            
        elif isinstance(action, AñadirParada):
            # Añade parada a la furgoneta y actualiza la carga de forma 'inteligente'
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1] = action.estacion
            
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] = min(action.estacion.num_bicicletas_next - action.estacion.demanda, action.estacion.num_bicicletas_no_usadas, 30)
            
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] - \
                (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas.next) \
                    if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] >= (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas.next) else 0
                
        elif isinstance(action, EliminarParada):
            # Elimina parada de la furgoneta y actualiza la carga (todas las bicis se descargan en el destino 0)
            if action.parada == 1:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1] = None
            
            else:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1]
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[1] = None
                
            new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = 0
            
        elif isinstance(action, SwapDestino):
            # Intercambia el destino de dos furgonetas (No toca la carga)
            new_state.furgonetas.lista_furgonetas[action.furgoneta1.id].ToGo[action.parada_furgo1], new_state.furgonetas.lista_furgonetas[action.furgoneta2.id].ToGo[action.parada_furgo2] = action.furgoneta2.ToGo[action.parada_furgo2], action.furgoneta1.ToGo[action.parada_furgo1]
            
        elif isinstance(action, CambiarCargaODescarga):
            # Cambia la carga o descarga de una furgoneta en una estación y actualiza la carga de forma 'inteligente'
            if action.parada == 0:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] = action.new_carga
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] - \
                    (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas.next) \
                        if new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[0] >= (new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].demanda - new_state.furgonetas.lista_furgonetas[action.furgoneta.id].ToGo[0].num_bicicletas.next) else 0
                
            else:
                new_state.furgonetas.lista_furgonetas[action.furgoneta.id].carga[1] = action.new_carga

        return new_state
    
"""
    def heuristic_count(self) -> float:
        non_empty_containers = 0
        for c_i, free_sp in self.free_spaces.items():
            if free_sp != 0:
                non_empty_containers = non_empty_containers + 1
        return non_empty_containers

    def heuristic_entropy(self) -> float:
        h_max = self.params.h_max
        total_entropy = 0
        for c_i in self.free_spaces:
            h_c_i = self.free_spaces[c_i]
            occupancy = 1 - (h_c_i / h_max)
            if occupancy > 0:
                total_entropy = total_entropy - (occupancy * math.log(occupancy))
        return total_entropy
"""