import time
from aima.search import hill_climbing, simulated_annealing, exp_schedule
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np

with open('results_experiment5_free_gas_simulated_annealing.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)  
    escritor_csv.writerow(['State_proved', 'Mean_time', 'Mean_profit', 'Mean_distance'])
    archivo_csv.close()

for seed in range(10):
    with open('experiment5.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['Time', 'Profit', 'Gas_cost'])
                    
        for _ in range(20):
            start = time.time()
            params = ProblemParameters(1250, 5, 25, seed, 0, True)
            initial_state = generate_initial_state(params)
            n = simulated_annealing(BicingProblem(initial_state), exp_schedule(k=12, lam=0.003, limit=900))
            end = time.time()
            aux = 0
            for furgoneta in n.furgonetas.lista_furgonetas:
                aux += furgoneta.distancia(0) + furgoneta.distancia(1)
                
            escritor_csv.writerow([end - start, n.heuristic(), aux])

    tiempos = []
    beneficios = []
    distance = []

    with open('experiment5.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        encabezados = next(lector_csv)

        for fila in lector_csv:
            tiempo, beneficio, gas_cost = map(float, fila)
            tiempos.append(tiempo)
            beneficios.append(beneficio)
            distance.append(gas_cost)
            
        archivo_csv.close()

    media_tiempo = np.mean(tiempos)
    media_beneficio = np.mean(beneficios)
    media_distance = np.mean(distance)

    with open('results_experiment5_free_gas_simulated_annealing.csv', 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([seed, media_tiempo, media_beneficio, media_distance])
    archivo_csv.close()
