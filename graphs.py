import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ast  # Para analizar las listas en formato de cadena

# Cargar los datos desde el archivo CSV
data = pd.read_csv("results_experiment1.csv")

# Convertir las listas de la columna "Operatos_used" en listas de Python
data["Operatos_used"] = data["Operatos_used"].apply(ast.literal_eval)

# Transformar los valores binarios en la columna "Operatos_used" a números decimales
data["Operatos_used"] = data["Operatos_used"].apply(lambda x: int("".join(map(str, x)), 2))

# Extraer las columnas
operators = data["Operatos_used"]
mean_time = data["Mean_time"]
mean_profit = data["Mean_profit"]

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configurar los ejes y etiquetas
ax.set_xlabel('Operador')
ax.set_ylabel('Mean Time')
ax.set_zlabel('Mean Profit')

# Crear una lista de colores para los operadores
colors = ['b', 'g', 'r', 'c', 'm', 'y']

# Crear un gráfico de barras en 3D
for i, operator in enumerate(operators):
    x = operator
    y = mean_time[i]
    z = mean_profit[i]
    ax.bar(x, z, zs=y, zdir='y', width=0.1, color=colors[x])

# Mostrar el gráfico
plt.show()
