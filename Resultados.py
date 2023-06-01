import pandas as pd
import numpy as np
from pgmpy.readwrite import BIFReader
import plotly.graph_objs as go
import plotly.io as pio
import math
import plotly.express as px
from pgmpy.inference import VariableElimination
pio.renderers.default = "browser"
##
reader = BIFReader("Proyecto Final/modeloPFinal.bif")
modelo = reader.get_model()
modelo.check_model()

# Infering the posterior probability
infer = VariableElimination(modelo)
posterior_p = infer.query(["Puntaje"], evidence={'Periodo': '0', 'Calendario': '0', 'Bilingue': '0', 'Departamento_Est': '7',
                                                 'Jornada': '5', 'Genero_Colegio': '0', 'Genero': '0', 'Estrato':'5', 'Computador': '0'})

print(posterior_p)
valores1 = round(posterior_p.values[0],2)
valores2 = round(posterior_p.values[1],2)
valores3 = round(posterior_p.values[2],2)
valores4 = round(posterior_p.values[3],2)

valores = [valores1, valores2, valores3, valores4]
maximo = max(valores)
posicion = 0
datos = [0,0,0]
for i in range(0, len(valores)):
    if valores[i] == maximo:
        maximo = valores[i]
        posicion = i

if posicion == 0:
    percentil = '0 y 25'
elif posicion == 1:
    percentil = '25 y 50'
elif posicion == 2:
    percentil = '50 y 75'
elif posicion == 22:
    percentil = '75 y 100'
datos = np.append(maximo, datos)
data2 = pd.DataFrame({'Probabilidad': datos})

lineas0 = [0,0,0]
lineas25 = [0.25, 0.25, 0.25]
lineas50 = [0.5,0.5, 0.5]
lineas75 = [0.75,0.75,0.75]
lineas1 = [1,1,1]
valoresy = [-0.4, 0, 0.4]
data0 = pd.DataFrame({'lineas0': lineas0, 'valoresy': valoresy})
data25 = pd.DataFrame({'lineas25': lineas25, 'valoresy': valoresy})
data50 = pd.DataFrame({'lineas50': lineas50, 'valoresy': valoresy})
data75 = pd.DataFrame({'lineas75': lineas75, 'valoresy': valoresy})
data1 = pd.DataFrame({'lineas1': lineas1, 'valoresy': valoresy})
etiquetasx = ['0', '25', '50', '75', '100']

##
# Se crea la gráfica de barras
pio.renderers.default = "browser"

fig = px.bar(data2, x='Probabilidad', height=300, text_auto=True, orientation = 'h')
fig.update_traces(marker_color='#A4D2BC')

fig.add_trace(go.Scatter(x = data0['lineas0'], y = data0['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 0, y = 0.4, text = '0', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data25['lineas25'], y = data25['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 0.25, y = 0.4, text = '25%', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data50['lineas50'], y = data50['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 0.50, y = 0.4, text = '50%', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data75['lineas75'], y = data75['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 0.75, y = 0.4, text = '75%', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data1['lineas1'], y = data1['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 1, y = 0.4, text = '100%', arrowhead = False, showarrow = False)

if math.isnan(valores1) or math.isnan(valores2) or math.isnan(valores3) or math.isnan(valores4):
    fig.update_layout(width=900, bargap=0.8,
                      plot_bgcolor="rgba(255,255,255,255)",
                      title_text='No es posible calcular la probabilidad con los datos ingresados')
else:
    fig.update_layout(width=900, bargap=0.8,
                      plot_bgcolor="rgba(255,255,255,255)",
                      title_text='El estudiante se encuentra entre los percentiles ' + percentil + ' con una probabilidad de ' + str(maximo), title_x=0.5)

fig.update_xaxes(range=[-0.05, 1.05], showline=True, linewidth=1, linecolor='black', showticklabels=False, title = ' ')
fig.update_yaxes(range=[-0.4, 0.4], showline=True, linewidth=1, mirror=True, showticklabels=False, title = ' ')
fig.show()