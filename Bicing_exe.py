import time
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv

with open('experiment1.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    
    escritor_csv.writerow(['Time, Profit, Seed'])
    
    for seed in range(5):
        for _ in range(20):
            start = time.time()
            params = ProblemParameters(1250, 5, 25, seed, 0, True)
            initial_state = generate_initial_state(params)
            n = hill_climbing(BicingProblem(initial_state))
            end = time.time()
            escritor_csv.writerow([end - start, n.heuristic(), seed])
    

# print(initial_state.furgonetas.lista_furgonetas)
# print(f"Beneficio inicial: {initial_state.heuristic()}")
# n = simulated_annealing(BicingProblem(initial_state)) 
# print(f"Dinero ganado: {n.heuristic()}")
# print(f"Profit: {n.furgonetas.profit()}")
# print(f"Gasolina: {n.furgonetas.gas_cost()}")
# print(f"Numero de acciones: {n.a}")
# print(n.furgonetas.lista_furgonetas)
# print(end - start, "seconds")