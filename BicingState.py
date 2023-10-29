from __future__ import annotations
import math
from typing import List, Dict, Generator
from Bicing_problem_parameters import ProblemParameters
from abia_bicing import Estacion, Estaciones
from operators import *
from furgoneta import Furgoneta, Furgonetas
from copy import deepcopy



class StateRepresentation(object):
    estaciones: Estaciones = None

    def __init__(self, params: ProblemParameters, furgonetas = None):
        self.params = params
        self.furgonetas = furgonetas
        self.a = 0

    def copy(self) -> StateRepresentation:
        return StateRepresentation(self.params, self.furgonetas.copy())
    
    def __repr__(self) -> str:
        return f"{self.params}"
        
    def generate_actions(self) -> Generator[ProblemaOperator, None, None]:
        for furgoneta in self.furgonetas.lista_furgonetas:
            for estacion in StateRepresentation.estaciones.lista_estaciones:
                if furgoneta.origen != estacion and furgoneta.ToGo[0] != estacion and furgoneta.ToGo[1] != estacion:
                    if estacion not in [furgoneta2.origen for furgoneta2 in self.furgonetas.lista_furgonetas]:
                        for i in range(max(min(estacion.num_bicicletas_next - estacion.demanda, estacion.num_bicicletas_no_usadas, 30), 0)):
                            if self.params.operators_used[0]:
                                yield MultiOperator(CambiarOrigen(furgoneta, estacion), NuevaCarga(furgoneta, 0 ,i))
                    
                    if self.params.operators_used[1]: 
                        for i in range(max(min(estacion.demanda - estacion.num_bicicletas_next, estacion.num_bicicletas_no_usadas, 30), 0)):
                            yield CambiarDestinoYCarga(furgoneta, 0, estacion, i, 0)
                            yield CambiarDestinoYCarga(furgoneta, 1, estacion, i, 0)
                            yield CambiarDestinoYCarga(furgoneta, 0, estacion, i, 1)
                            yield CambiarDestinoYCarga(furgoneta, 1, estacion, i, 1)
                            
                    if self.params.operators_used[2]:
                        yield CambiarDestino(furgoneta, furgoneta.ToGo[0], estacion)
                        yield CambiarDestino(furgoneta, furgoneta.ToGo[1], estacion)
                        
            if self.params.operators_used[3]:
                
                for furgoneta2 in self.furgonetas.lista_furgonetas:
                    if furgoneta.origen != furgoneta2.ToGo[0] and furgoneta2.origen != furgoneta.ToGo[0]:
                        yield SwapDestino(furgoneta, 0, furgoneta2, 0)
                            
                    if furgoneta.origen != furgoneta2.ToGo[1] and furgoneta2.origen != furgoneta.ToGo[0]:
                        yield SwapDestino(furgoneta, 0, furgoneta2, 1)
                            
                    if furgoneta.origen != furgoneta2.ToGo[0] and furgoneta2.origen != furgoneta.ToGo[1]:
                        yield SwapDestino(furgoneta, 1, furgoneta2, 0)
                        
                    if furgoneta.origen != furgoneta2.ToGo[1] and furgoneta2.origen != furgoneta.ToGo[1]:
                        yield SwapDestino(furgoneta, 1, furgoneta2, 1)
                        
            if self.params.operators_used[4]:  
                      
                yield CambiarCargaODescarga(furgoneta, 0)
            
                yield CambiarCargaODescarga(furgoneta, 1)
            
            if self.params.operators_used[5]:
                
                for i in range(max(min(furgoneta.origen.num_bicicletas_next - furgoneta.origen.demanda, furgoneta.origen.num_bicicletas_no_usadas, 30), 0)):
                    yield NuevaCarga(furgoneta, 0 ,i)
                
                aux_for_loop = max(min(furgoneta.ToGo[0].num_bicicletas_next - furgoneta.ToGo[0].demanda, furgoneta.ToGo[0].num_bicicletas_no_usadas, 30), 0)
                
                if furgoneta.carga[0] > aux_for_loop:    
                    for i in range(furgoneta.carga[0] - aux_for_loop):
                        yield NuevaCarga(furgoneta, 1 ,i)

    def generate_actions_simulated_annealing(self) -> Generator[ProblemaOperator, None, None]:
        for furgoneta in self.furgonetas.lista_furgonetas:
            for estacion in StateRepresentation.estaciones.lista_estaciones:
                if furgoneta.origen != estacion:
                    if estacion not in [furgoneta2.origen for furgoneta2 in self.furgonetas.lista_furgonetas]:
                        if furgoneta.origen != estacion and furgoneta.ToGo[0] != estacion and furgoneta.ToGo[1] != estacion:
                            yield CambiarOrigen(furgoneta, estacion)
                            
                if furgoneta.origen != estacion and furgoneta.ToGo[0] != estacion and furgoneta.ToGo[1] != estacion:
                    yield CambiarDestino(furgoneta, furgoneta.ToGo[0], estacion)
                    for i in range(max(min(estacion.demanda - estacion.num_bicicletas_next, estacion.num_bicicletas_no_usadas, 30), 0)): 
                        yield CambiarDestinoYCarga(furgoneta, 0, estacion, i, 0)
                        yield CambiarDestinoYCarga(furgoneta, 1, estacion, i, 0)
                        yield CambiarDestinoYCarga(furgoneta, 0, estacion, i, 1)
                        yield CambiarDestinoYCarga(furgoneta, 1, estacion, i, 1)
                    
                if furgoneta.origen != estacion and furgoneta.ToGo[0] != estacion and furgoneta.ToGo[1] != estacion:
                    yield CambiarDestino(furgoneta, furgoneta.ToGo[1], estacion)
                
            yield CambiarCargaODescarga(furgoneta, 0)
            
            yield CambiarCargaODescarga(furgoneta, 1)
            
            for i in range(max(min(furgoneta.origen.num_bicicletas_next - furgoneta.origen.demanda, furgoneta.origen.num_bicicletas_no_usadas, 30), 0)):
                yield NuevaCarga(furgoneta, 0 ,i)
            
            aux_for_loop = max(min(furgoneta.ToGo[0].num_bicicletas_next - furgoneta.ToGo[0].demanda, furgoneta.ToGo[0].num_bicicletas_no_usadas, 30), 0)
            
            if furgoneta.carga[0] > aux_for_loop:    
                for i in range(furgoneta.carga[0] - aux_for_loop):
                    yield NuevaCarga(furgoneta, 1 ,i)
                            

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

        elif isinstance(action, NuevaCarga):
            furgo_nueva = new_state.furgonetas.lista_furgonetas[action.furgoneta.id]
            furgo_nueva.carga[action.parada] = action.nueva_carga

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
                    
        elif isinstance(action, CambiarDestinoYCarga):
            furgo_nueva = new_state.furgonetas.lista_furgonetas[action.furgoneta.id]
            furgo_nueva.ToGo[action.estacion_parada] = action.new_estacion
            furgo_nueva.carga[action.carga_to_change] = action.nueva_carga
            if action.carga_to_change == 0:
                if furgo_nueva.ToGo[0] is not None:
                    if furgo_nueva.carga[0] >= furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next >= 0:
                        furgo_nueva.carga[1] = furgo_nueva.carga[0] - \
                        (furgo_nueva.ToGo[0].demanda - furgo_nueva.ToGo[0].num_bicicletas_next)
                    else:
                        furgo_nueva.carga[1] = 0

        elif isinstance(action, SwapDestino):
            # Intercambia el destino de dos furgonetas tambien actualiza la carga de forma 'inteligente'
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
                
        elif isinstance(action, EliminarParada):
            #Elimina la carga de una furgoneta en una estación
            furgo_nueva = new_state.furgonetas.lista_furgonetas[action.furgoneta.id]
            furgo_nueva.carga[action.parada] = 0

            if action.parada == 0:
                furgo_nueva.carga[1] = 0

        elif isinstance(action, MultiOperator):
            new_state = self.apply_action(action.operator)
            new_state = new_state.apply_action(action.operator2)
                        
        return new_state
    
    def heuristic(self):      
        return self.furgonetas.profit() if self.params.free_gas else self.furgonetas.profit() - self.furgonetas.gas_cost()
    
def generate_initial_state(params: ProblemParameters) -> StateRepresentation:
    StateRepresentation.estaciones = Estaciones(params.num_estaciones, params.num_bicicletas, params.seed)
    Furgonetas.estaciones = StateRepresentation.estaciones
    Furgonetas.parameters = params
    furgonetas = Furgonetas(params.num_furgonetas)
    return StateRepresentation(params, furgonetas)
