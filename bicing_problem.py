from typing import Generator

from aima.search import Problem

from BicingState import StateRepresentation
from operators import ProblemaOperator

class BicingProblem(Problem):
    def __init__(self, initial_state: StateRepresentation):
        super().__init__(initial_state)

    def actions(self, state: StateRepresentation) -> Generator[ProblemaOperator, None, None]:
        return state.generate_actions()
    
    #Cambiar a state.generate_actions_simulated annealing() si se va a utilizar este algoritmo

    def result(self, state: StateRepresentation, action: ProblemaOperator) -> StateRepresentation:
        return state.apply_action(action)
    
    def value(self, state: StateRepresentation) -> float:
        return state.heuristic()

    def goal_test(self, state: StateRepresentation) -> bool:
        return False
