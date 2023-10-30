import time
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np

with open('results_experiment6_with_free_gas.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)  
    escritor_csv.writerow(['State_proved', 'Mean_time', 'Mean_profit'])
    archivo_csv.close()
    
    for state_proved in range(1,6):
        tiempos = []
        profit = []
        for seed in range(5):
            for _ in range(1):
                start = time.time()
                params = ProblemParameters(1250, 5*state_proved, 25, seed, free_gas=True)
                initial_state = generate_initial_state(params)
                n = hill_climbing(BicingProblem(initial_state))
                end = time.time()
                tiempos.append(end - start)
                profit.append(n.heuristic())

        media_tiempo = np.mean(tiempos)
        media_profit = np.mean(profit)

        with open('results_experiment6_with_free_gas.csv', 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([state_proved, media_tiempo, media_profit])
            archivo_csv.close()

# print(initial_state.furgonetas.lista_furgonetas)
# print(f"Beneficio inicial: {initial_state.heuristic()}")
# n = simulated_annealing(BicingProblem(initial_state)) 
# print(f"Dinero ganado: {n.heuristic()}")
# print(f"Profit: {n.furgonetas.profit()}")
# print(f"Gasolina: {n.furgonetas.gas_cost()}")
# print(f"Numero de acciones: {n.a}")
# print(n.furgonetas.lista_furgonetas)
# print(end - start, "seconds")