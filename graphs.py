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
"""

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
