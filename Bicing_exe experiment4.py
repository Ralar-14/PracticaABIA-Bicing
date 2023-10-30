import time
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np

with open('results_experiment4.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)  
    escritor_csv.writerow(['State_proved', 'Mean_time'])
    archivo_csv.close()
    
    for state_proved in range(1,6):
        tiempos = []            
        for i in range(10):
            start = time.time()
            params = ProblemParameters(state_proved*1250, state_proved*5, state_proved*25, 42, 0, True)
            initial_state = generate_initial_state(params)
            n = hill_climbing(BicingProblem(initial_state))
            end = time.time()
            tiempos.append(end - start)

        media_tiempo = np.mean(tiempos)

        with open('results_experiment4.csv', 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([state_proved, media_tiempo])
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