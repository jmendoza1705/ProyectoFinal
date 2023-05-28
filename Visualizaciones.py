import pandas as pd
import statistics
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

##
# se importan los datos

datos =  pd.read_csv('Proyecto Final/data.csv')

## Visualizaciones

# puntaje antes y durante pandemia
antes=0
despues=0
for i in range (len(datos["Periodo"])):
    if datos["Periodo"][i]==20211:
        despues+=1
    if datos["Periodo"][i]==20194:
        antes+=1

## Visualización 1
punt_antes, punt_despues = [], []
for i in range (len(datos["Periodo"])):
    if datos["Periodo"][i] == 20194:
        punt_antes.append(datos["Puntaje"][i])
    if datos["Periodo"][i] == 20211:
        punt_despues.append(datos["Puntaje"][i])

prom_antes = statistics.mean(punt_antes)
prom_despues = statistics.mean(punt_despues)

d_x = ["2019", "2021"]
d_y = [prom_antes, prom_despues]

###
fig_v1 = px.bar(x=d_x, y=d_y)
fig_v1.update_traces(marker_color='lightpink')
fig_v1.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Puntaje Promedio en el Saber 11', title_x=0.5, title_font_size=20, font=dict(size=16))
fig_v1.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Periodo',tickfont=dict(size=15))
fig_v1.update_yaxes(range=[0, 360],showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Puntaje Promedio',tickfont=dict(size=15))
fig_v1.show()


