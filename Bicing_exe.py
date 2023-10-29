import time
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem
import csv
import numpy as np


alternativas_binarias = []

for i in range(2 ** 6):
    binario = bin(i)[2:] 
    binario = binario.zfill(6)
    binario_lista = [int(bit) for bit in binario]
    alternativas_binarias.append(binario_lista)
    
with open('results_experiment1.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        escritor_csv.writerow(['Operatos_used, Mean_time, Mean_profit'])
        archivo_csv.close()
        
for operators in alternativas_binarias:
    with open('experiment1.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        escritor_csv.writerow(['Time, Profit, Seed'])
        
        
        for seed in range(5):
            for _ in range(20):
                start = time.time()
                params = ProblemParameters(1250, 5, 25, seed, 2, True, operators)
                initial_state = generate_initial_state(params)
                n = hill_climbing(BicingProblem(initial_state))
                end = time.time()
                escritor_csv.writerow([end - start, n.heuristic(), seed])

    tiempos = []
    beneficios = []

    with open('experiment1.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        encabezados = next(lector_csv)

        for fila in lector_csv:
            tiempo, beneficio, _ = map(float, fila)
            tiempos.append(tiempo)
            beneficios.append(beneficio)
        archivo_csv.close()

    media_tiempo = np.mean(tiempos)
    media_beneficio = np.mean(beneficios)

    with open('results_experiment1.csv', 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        
        escritor_csv.writerow([operators, media_tiempo, media_beneficio])
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