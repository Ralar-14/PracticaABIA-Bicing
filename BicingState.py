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
        self.a = 0

    def copy(self) -> StateRepresentation:
        return deepcopy(self)
    
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


            for furgoneta2 in self.furgonetas.lista_furgonetas:
                yield SwapDestino(furgoneta, 0, furgoneta2, 0)
                yield SwapDestino(furgoneta, 0, furgoneta2, 1)
                yield SwapDestino(furgoneta, 1, furgoneta2, 0)
                yield SwapDestino(furgoneta, 1, furgoneta2, 1)
                
                yield CambiarCargaODescarga(furgoneta, 0)

            

    def apply_action(self, action: ProblemaOperator) -> StateRepresentation:
        new_state = self.copy()
        self.a += 1
        
        if isinstance(action, CambiarOrigen):
            # Cambia el origen de la furgoneta y de forma 'inteligente' la carga
            
            furgo_nueva = new_state.furgonetas.lista_furgonetas[action.furgoneta.id]
            furgo_nueva.origen = action.new_origen
            furgo_nueva.carga[0] = max(min(furgo_nueva.origen.num_bicicletas_next - furgo_nueva.origen.demanda, furgo_nueva.origen.num_bicicletas_no_usadas, 30), 0)
            if furgo_nueva.ToGo[0] is not None:
                if furgo_nueva.carga[0] >= furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next >= 0:
                    furgo_nueva.carga[1] = furgo_nueva.carga[0] - \
                    (furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next)
                else:
                    furgo_nueva.carga[1] = 0

        elif isinstance(action, CambiarDestino):
            # Cambia el destino de la furgoneta y de forma 'inteligente' la carga
            furgo_nueva = new_state.furgonetas.lista_furgonetas[action.furgoneta.id]
            furgo_nueva.estacion_parada = action.new_estacion
            furgo_nueva.carga[0] = max(min(furgo_nueva.origen.num_bicicletas_next - furgo_nueva.origen.demanda, furgo_nueva.origen.num_bicicletas_no_usadas, 30), 0)
            if furgo_nueva.ToGo[0] is not None:
                if furgo_nueva.carga[0] >= furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next >= 0:
                    furgo_nueva.carga[1] = furgo_nueva.carga[0] - \
                    (furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next)
                else:
                    furgo_nueva.carga[1] = 0

        elif isinstance(action, SwapDestino):
            # Intercambia el destino de dos furgonetas (No toca la carga)
            new_state.furgonetas.lista_furgonetas[action.furgoneta1.id].ToGo[action.parada_furgo1], new_state.furgonetas.lista_furgonetas[action.furgoneta2.id].ToGo[action.parada_furgo2] = action.furgoneta2.ToGo[action.parada_furgo2], action.furgoneta1.ToGo[action.parada_furgo1]
            furgo_nueva1 = new_state.furgonetas.lista_furgonetas[action.furgoneta1.id]
            furgo_nueva2 = new_state.furgonetas.lista_furgonetas[action.furgoneta1.id]
            
            furgo_nueva1.carga[0] = max(min(furgo_nueva1.origen.num_bicicletas_next - furgo_nueva1.origen.demanda, furgo_nueva1.origen.num_bicicletas_no_usadas, 30), 0)
            if furgo_nueva1.ToGo[0] is not None:
                if furgo_nueva1.carga[0] >= furgo_nueva1.ToGo[0].demanda - furgo_nueva1.ToGo[0].num_bicicletas_next >= 0:
                    furgo_nueva1.carga[1] = furgo_nueva1.carga[0] - \
                    (furgo_nueva1.ToGo[0].demanda - furgo_nueva1.ToGo[0].num_bicicletas_next)
                else:
                    furgo_nueva1.carga[1] = 0
                    
            furgo_nueva2.carga[0] = max(min(furgo_nueva2.origen.num_bicicletas_next - furgo_nueva2.origen.demanda, furgo_nueva2.origen.num_bicicletas_no_usadas, 30), 0)
            if furgo_nueva2.ToGo[0] is not None:
                if furgo_nueva2.carga[0] >= furgo_nueva2.ToGo[0].demanda - furgo_nueva2.ToGo[0].num_bicicletas_next >= 0:
                    furgo_nueva2.carga[1] = furgo_nueva2.carga[0] - \
                    (furgo_nueva2.ToGo[0].demanda - furgo_nueva2.ToGo[0].num_bicicletas_next)
                else:
                    furgo_nueva2.carga[1] = 0

        elif isinstance(action, CambiarCargaODescarga):
            # Cambia la carga o descarga de una furgoneta en una estación y actualiza la carga de forma 'inteligente'
            furgo_nueva = new_state.furgonetas.lista_furgonetas[action.furgoneta.id]
            furgo_nueva.carga[0] = max(min(furgo_nueva.origen.num_bicicletas_next - furgo_nueva.origen.demanda, furgo_nueva.origen.num_bicicletas_no_usadas, 30), 0)
            if furgo_nueva.ToGo[0] is not None:
                if furgo_nueva.carga[0] >= furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next >= 0:
                    furgo_nueva.carga[1] = furgo_nueva.carga[0] - \
                    (furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next)
                else:
                    furgo_nueva.carga[1] = 0
            
        return new_state
    
    def heuristic(self):      
        return self.furgonetas.profit()
   
    
def generate_initial_state(params: ProblemParameters) -> StateRepresentation:
    estaciones = Estaciones(params.num_estaciones, params.num_bicicletas, params.seed)
    furgonetas = Furgonetas(params.num_furgonetas, estaciones)
    return StateRepresentation(params, estaciones, furgonetas)
