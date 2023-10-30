import time
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np

with open('results_experiment2.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)  
    escritor_csv.writerow(['Initial_state', 'Mean_time', 'Mean_profit'])
    archivo_csv.close()

for init_state in range(3):
    with open('experiment2.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        escritor_csv.writerow(['Time', 'Profit', 'Seed'])
        
        for seed in range(5):
            for _ in range(20):
                start = time.time()
                params = ProblemParameters(1250, 5, 25, seed, init_state, True)
                initial_state = generate_initial_state(params)
                n = hill_climbing(BicingProblem(initial_state))
                end = time.time()
                escritor_csv.writerow([end - start, n.heuristic(), seed])

    tiempos = []
    beneficios = []

    with open('experiment2.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        encabezados = next(lector_csv)

        for fila in lector_csv:
            tiempo, beneficio, _ = map(float, fila)
            tiempos.append(tiempo)
            beneficios.append(beneficio)
        archivo_csv.close()

    media_tiempo = np.mean(tiempos)
    media_beneficio = np.mean(beneficios)

    with open('results_experiment2.csv', 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([init_state, media_tiempo, media_beneficio])
        archivo_csv.close()

