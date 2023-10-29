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
