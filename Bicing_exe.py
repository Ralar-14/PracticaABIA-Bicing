import time
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np

start = time.time()
params = ProblemParameters(1250, 5, 25, 42, 0, True)
initial_state = generate_initial_state(params)
n = hill_climbing(BicingProblem(initial_state))
#n = simulated_annealing(BicingProblem(initial_state))
end = time.time()

print(f"Dinero ganado: {n.heuristic()}")
print(f"Profit: {n.furgonetas.profit()}")
print(f"Gasolina: {n.furgonetas.gas_cost()}")
print(end - start, "seconds")

# print(initial_state.furgonetas.lista_furgonetas)
# print(f"Beneficio inicial: {initial_state.heuristic()}")
# n = simulated_annealing(BicingProblem(initial_state)) 
# print(f"Dinero ganado: {n.heuristic()}")
# print(f"Profit: {n.furgonetas.profit()}")
# print(f"Gasolina: {n.furgonetas.gas_cost()}")
# print(f"Numero de acciones: {n.a}")
# print(n.furgonetas.lista_furgonetas)
# print(end - start, "seconds")