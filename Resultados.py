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

def Discretizacion(periodo, calendario, jornada, bilingue, genero_col, genero_est, departamento, estrato, computador):
    datos = []

    #Periodo
    periodoD = (periodo == 20211) * 1

    #Calendario
    calendarios = ['A', 'B', 'OTRO']
    for i in range(0, len(calendarios)):
        if calendario == calendarios[i]:
            calendarioD = i

    # Jornada
    jornadas = ['COMPLETA', 'MAÑANA', 'NOCHE', 'SABATINA', 'TARDE', 'UNICA']
    for i in range(0, len(jornadas)):
        if jornada == jornadas[i]:
            jornadaD = i

    #Bilingue
    bilingueD = (bilingue == "S") * 1

    #Genero Colegio
    generoscol = ['FEMENINO', 'MASCULINO', 'MIXTO']
    for i in range(0, len(generoscol)):
        if genero_col == generoscol[i]:
            genero_colD = i

    #Genero Estudiante
    genero_estD = (genero_est == "M") * 1

    # Departamento
    departamentos = ['AMAZONAS', 'ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTÁ', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETA',
                     'CASANARE', 'CAUCA', 'CESAR', 'CHOCO', 'CORDOBA', 'CUNDINAMARCA', 'GUAINIA', 'GUAVIARE', 'HUILA',
                     'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO', 'NORTE SANTANDER', 'PUTUMAYO', 'QUINDIO', 'RISARALDA',
                     'SAN ANDRES', 'SANTANDER', 'SUCRE', 'TOLIMA', 'VALLE', 'VAUPES', 'VICHADA']
    for i in range(0, len(departamentos)):
        if departamento == departamentos[i]:
            departamentoD = i

    #Estrato
    estratos = ['Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6', 'No sabe']
    for i in range(0, len(estratos)):
        if estrato == estratos[i]:
            estratoD = i + 1

    #Computador
    computadorD = (computador == "Si") * 1

    datos.append(str(periodoD), str(calendarioD), str(jornadaD), str(bilingueD), str(genero_colD), str(genero_estD), str(departamentoD), str(estratoD), str(computadorD))
    return datos
variables = Discretizacion(periodo, calendario, jornada, bilingue, genero_col, genero_est, departamento, estrato, computador)

posterior_p = infer.query(["Puntaje"], evidence={'Periodo': variables[0], 'Calendario': variables[1],
                                                 'Jornada': variables[2] ,'Bilingue': variables[3],
                                                 'Genero_Colegio': variables[4],'Genero': variables[5],
                                                 'Departamento_Est': variables[6],  'Estrato':variables[7],
                                                 'Computador': variables[8]})

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