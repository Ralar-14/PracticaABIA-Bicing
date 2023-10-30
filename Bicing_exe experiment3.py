import time
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np

with open('results_experiment3.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)  
    escritor_csv.writerow(['State_proved', 'Mean_time', 'Mean_profit'])
    archivo_csv.close()

for k in range(0, 101, 10):
    for lam in range(0, 10001, 1000):
        for limit in range(0, 751, 250):
            with open('experiment3.csv', 'w', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow(['Time', 'Profit', 'Seed'])
                
                for _ in range(2):
                    start = time.time()
                    params = ProblemParameters(1250, 5, 25, 42, 0, True)
                    initial_state = generate_initial_state(params)
                    n = simulated_annealing(BicingProblem(initial_state), lambda t: (k * np.exp(-lam/10000 * t) if t < limit else 0))
                    end = time.time()
                    escritor_csv.writerow([end - start, n.heuristic(), 42])

            tiempos = []
            beneficios = []

            with open('experiment3.csv', 'r') as archivo_csv:
                lector_csv = csv.reader(archivo_csv)
                encabezados = next(lector_csv)

                for fila in lector_csv:
                    tiempo, beneficio, _ = map(float, fila)
                    tiempos.append(tiempo)
                    beneficios.append(beneficio)
                archivo_csv.close()

            media_tiempo = np.mean(tiempos)
            media_beneficio = np.mean(beneficios)

            with open('results_experiment3.csv', 'a', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow([[k, lam, limit], media_tiempo, media_beneficio])
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