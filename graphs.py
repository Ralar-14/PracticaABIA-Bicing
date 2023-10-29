import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Listas para almacenar los datos
operadores_usados = []
mean_time = []
mean_profit = []

# Abre el archivo CSV en modo lectura
with open('results_experiment1.csv', 'r') as archivo_csv:
    lector_csv = csv.reader(archivo_csv)
    encabezados = next(lector_csv)  # Lee y descarta la fila de encabezados

    for fila in lector_csv:
        operador = eval(fila[0])  # Evalúa la cadena como una lista de Python
        tiempo = float(fila[1])
        beneficio = float(fila[2])

        operadores_usados.append(operador)
        mean_time.append(tiempo)
        mean_profit.append(beneficio)

# Convierte las listas en arrays NumPy
operadores_usados = np.array(operadores_usados)
mean_time = np.array(mean_time)
mean_profit = np.array(mean_profit)

# Crea una figura 3D
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Crea las barras 3D
ax.bar(mean_profit, mean_time, bottom=0, zs=np.arange(len(operadores_usados)), zdir='y', color='b', alpha=0.7)

# Etiquetas de los ejes
ax.set_xlabel('Mean Profit')
ax.set_ylabel('Mean Time')
ax.set_zlabel('Operadores Usados')

plt.show()
