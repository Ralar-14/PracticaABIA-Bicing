"""
import pandas as pd
import plotly.express as px

# Cargar los datos desde el archivo CSV
data = pd.read_csv("results_experiment1.csv")

# Convertir las listas de la columna "Operators_used" en números enteros en base 2
data["Operators_used"] = data["Operators_used"].apply(lambda x: int("".join(map(str, x[1:-1].split(', '))), 2))

# Extraer las columnas
operators = data.iloc[:, 0]
mean_time = data.iloc[:, 1]
mean_profit = data.iloc[:, 2]

# Crear un DataFrame con los datos
df = pd.DataFrame({'Operador': operators, 'Mean Time': mean_time, 'Mean Profit': mean_profit})

# Crear un gráfico de barras en 3D simulando la profundidad con scatter_3d
fig = px.scatter_3d(df, x='Operador', y='Mean Time', z='Mean Profit', size_max=10)

# Ajustar el tamaño de la figura
fig.update_layout(scene=dict(
    aspectmode='cube',
))

# Mostrar el gráfico
fig.show()


import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo CSV
data = pd.read_csv("results_experiment4.csv")

# Extraer las columnas State_proved y Mean_time
state_proved = data["State_proved"]
mean_time = data["Mean_time"]

# Crear un gráfico de línea para representar el crecimiento del tiempo
plt.figure(figsize=(10, 6))
plt.plot(state_proved, mean_time, marker='o', linestyle='-')
plt.title('Crecimiento del Tiempo por Estado')
plt.xlabel('Estado (State_proved)')
plt.ylabel('Tiempo Medio (Mean_time)')
plt.grid(True)

# Mostrar el gráfico
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo CSV
data = pd.read_csv("results_experiment6_with_free_gas.csv")

# Extraer las columnas State_proved, Mean_time y Mean_profit
state_proved = data["State_proved"]
mean_time = data["Mean_time"]
mean_profit = data["Mean_profit"]

# Crear una figura y dos ejes Y
fig, ax1 = plt.subplots(figsize=(10, 6))

# Configurar el primer eje Y (Mean_time)
ax1.set_xlabel('State_proved')
ax1.set_ylabel('Mean Time', color='tab:blue')
ax1.plot(state_proved, mean_time, marker='o', linestyle='-', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Crear el segundo eje Y (Mean_profit)
ax2 = ax1.twinx()
ax2.set_ylabel('Mean Profit', color='tab:red')
ax2.plot(state_proved, mean_profit, marker='s', linestyle='--', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Configurar el título y etiquetas
plt.title('Crecimiento de Mean Time y Mean Profit por State_proved')
plt.xlabel('State_proved')

# Mostrar el gráfico
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Cargar los datos desde el archivo CSV
data = pd.read_csv("results_experiment3_kilambda.csv")

# Dividir la columna "State_proved" en dos columnas: k y lambda
data['k'], data['lambda'] = data['State_proved'].str.split(',').str

# Convertir las columnas k y lambda a valores numéricos
data['k'] = data['k'].str.extract('(\d+)').astype(int)
data['lambda'] = data['lambda'].str.extract('(\d+)').astype(int)

# Extraer las columnas k, lambda y Mean Profit
k = data['k']
lambda_val = data['lambda']
mean_profit = data['Mean_time']

# Crear un gráfico 3D
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Agregar los datos al gráfico 3D
ax.scatter(k, lambda_val, mean_profit, c=mean_profit, cmap='viridis')

# Configurar etiquetas de ejes
ax.set_xlabel('k')
ax.set_ylabel('lambda')
ax.set_zlabel('Mean Time')

# Configurar título
ax.set_title('Gráfico 3D de k, lambda y Mean Time')

# Mostrar el gráfico 3D
plt.show()

"""

import pandas as pd
import matplotlib.pyplot as plt

# Crear el primer DataFrame con los datos de la primera tabla adicional
data1 = pd.DataFrame({
    'State_proved': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    'Mean_time_1': [0.2150362491607666, 0.11905293464660645, 0.2811698913574219, 0.12009205818176269, 0.1408623695373535, 0.25773372650146487, 0.18240675926208497, 0.1975428581237793, 0.23324317932128907, 0.1728388786315918],
    'Mean_profit_1': [64.64, 76.6, 51.8, 40.5, 54.2, 52.220000000000006, 57.67999999999999, 56.3, 47.6, 54.1],
    'Mean_distance_1': [10.4, 27.9, 40.8, 36.6, 53.3, 38.22, 32.58, 35.5, 34.72, 34.0]
})

# Crear el segundo DataFrame con los datos de la segunda tabla adicional
data2 = pd.DataFrame({
    'State_proved': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    'Mean_time_2': [2.6321486949920656, 2.519380521774292, 2.5246560096740724, 2.5740825176239013, 2.531605768203735, 2.528333902359009, 2.5156476974487303, 2.622769594192505, 2.5777699947357178, 2.5449268341064455],
    'Mean_profit_2': [48.62, 63.98, 23.54, 28.439999999999998, 27.439999999999998, 33.64, 40.5, 43.620000000000005, 30.119999999999997, 43.92],
    'Mean_distance_2': [21.52, 38.800000000000004, 58.999999999999986, 49.32000000000001, 81.86, 44.8, 57.2, 45.919999999999995, 38.32, 37.12]
})

# Calcular la diferencia entre las dos tablas adicionales
data_diff = data2.copy()  # Copia el segundo DataFrame
data_diff['Mean_time_diff'] = data2['Mean_time_2'] - data1['Mean_time_1']
data_diff['Mean_profit_diff'] = data2['Mean_profit_2'] - data1['Mean_profit_1']
data_diff['Mean_distance_diff'] = data2['Mean_distance_2'] - data1['Mean_distance_1']

# Crear un gráfico de barras para mostrar las diferencias
fig, ax = plt.subplots(figsize=(10, 6))

# Configurar las barras para las diferencias de las tres variables
ax.bar(data_diff['State_proved'], data_diff['Mean_time_diff'], width=0.2, label='Mean Time Difference', color='red')
ax.bar(data_diff['State_proved'] + 0.2, data_diff['Mean_profit_diff'], width=0.2, label='Mean Profit Difference', color='green')
ax.bar(data_diff['State_proved'] + 0.4, data_diff['Mean_distance_diff'], width=0.2, label='Mean Distance Difference', color='blue')

# Configurar etiquetas y leyenda
ax.set_xlabel('State_proved')
ax.set_ylabel('Difference')
ax.set_title('Differences between No_free_gas_simulated_annealing and No_free_gas_hill_climbing')
ax.legend()

# Mostrar el gráfico de diferencias
plt.show()



