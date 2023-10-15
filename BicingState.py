from __future__ import annotations
import math
from typing import List, Dict, Generator
from Bicing_problem_parameters import ProblemParameters
from abia_bicing import Estacion, Estaciones

class StateRepresentation(object):
    def __init__(self, params: ProblemParameters):
        self.params = params
        self.estaciones = Estaciones()
        
        
    def copy(self) -> StateRepresentation:
        return StateRepresentation(self.params)
    
    def __repr__(self) -> str:
        return f"{self.params}"
        
"""
    def generate_actions(self) -> Generator[BinPackingOperator, None, None]:
        

    def apply_action(self, action: BinPackingOperator) -> StateRepresentation:
        new_state = self.copy()
        if isinstance(action, MoveParcel):
            p_i = action.p_i
            h_p_i = new_state.params.v_h[p_i]

            c_j = action.c_j
            c_k = action.c_k

            new_state.v_p[p_i] = c_k
            new_state.free_spaces[c_j] = new_state.free_spaces[c_j] + h_p_i
            new_state.free_spaces[c_k] = new_state.free_spaces[c_k] - h_p_i

        elif isinstance(action, SwapParcels):
            p_i = action.p_i
            p_j = action.p_j
            h_p_i = new_state.params.v_h[p_i]
            h_p_j = new_state.params.v_h[p_j]

            c_i = new_state.v_p[p_i]
            c_j = new_state.v_p[p_j]

            new_state.v_p[p_i] = c_j
            new_state.v_p[p_j] = c_i
            new_state.free_spaces[c_i] = new_state.free_spaces[c_i] + h_p_i - h_p_j
            new_state.free_spaces[c_j] = new_state.free_spaces[c_j] - h_p_i + h_p_j

        return new_state

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