import time
from aima.search import hill_climbing, simulated_annealing, exp_schedule
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np
"""
with open('results_experiment3.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)  
    escritor_csv.writerow(['State_proved', 'Mean_time', 'Mean_profit'])
    archivo_csv.close()

for limit in range(1000, 2500, 50):
    with open('experiment3_limit.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['Time', 'Profit', 'Seed'])
                
        for i in range(4):
            start = time.time()
            params = ProblemParameters(1250, 5, 25, i, 0, True)
            initial_state = generate_initial_state(params)
            n = simulated_annealing(BicingProblem(initial_state), exp_schedule(k=20, lam=0.005, limit=limit))
            end = time.time()
            escritor_csv.writerow([end - start, n.heuristic(), i])
            
    tiempos = []
    beneficios = []

    with open('experiment3_limit.csv', 'r') as archivo_csv:
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
        escritor_csv.writerow([limit, media_tiempo, media_beneficio])
        archivo_csv.close()
"""        
# Per veure k y lambda

with open('results_experiment3_kilambda.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)  
    escritor_csv.writerow(['State_proved', 'Mean_time', 'Mean_profit'])
    archivo_csv.close()

for k in range(5, 150, 5):
    for lam in range(1, 11):
        with open('experiment3_kilambda.csv', 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow(['Time', 'Profit', 'Seed'])
                    
            for i in range(20):
                start = time.time()
                params = ProblemParameters(1250, 5, 25, i, 0, True)
                initial_state = generate_initial_state(params)
                n = simulated_annealing(BicingProblem(initial_state), exp_schedule(k=k, lam=lam, limit=900))
                end = time.time()
                escritor_csv.writerow([end - start, n.heuristic(), i])
                
        tiempos = []
        beneficios = []

        with open('experiment3_kilambda.csv', 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            encabezados = next(lector_csv)

            for fila in lector_csv:
                tiempo, beneficio, _ = map(float, fila)
                tiempos.append(tiempo)
                beneficios.append(beneficio)
            archivo_csv.close()

        media_tiempo = np.mean(tiempos)
        media_beneficio = np.mean(beneficios)

        with open('results_experiment3_kilambda.csv', 'a', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([[k, lam], media_tiempo, media_beneficio])
            archivo_csv.close()