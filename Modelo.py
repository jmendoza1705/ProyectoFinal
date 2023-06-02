import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import K2Score
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.readwrite import BIFReader
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.io as pio
import math
import plotly.express as px
pio.renderers.default = "browser"

####
data = pd.read_csv('Proyecto Final/Datos Discretizados3.csv')
names = data.columns.values
data = data.to_numpy()
##
dataEntrenamiento = data[0:615000,:]
dataValidacion = data[615000:,:]

##
#Se definen las muestras con los datos de entrenamiento
muestras = pd.DataFrame(dataEntrenamiento, columns = names)

##
modelo = BayesianNetwork([("Departamento_Est", "Genero_Colegio"), ("Genero_Colegio", "Puntaje"), ("Genero", "Puntaje"),
                        ("Estrato", "Computador"), ("Estrato", "Jornada"),("Estrato", "Bilingue"), ("Computador", "Puntaje"),
                        ("Jornada", "Puntaje"), ("Bilingue", "Puntaje"), ("Calendario", "Puntaje"), ("Periodo", "Puntaje")])
##

scoring_method = K2Score(data=muestras)
esth = HillClimbSearch(data=muestras)
estimated_modelh = esth.estimate(scoring_method=scoring_method, max_indegree=7, max_iter=int(1e4),
                        fixed_edges = {("Departamento_Est", "Genero_Colegio"),("Genero_Colegio", "Puntaje"),
                                       ("Genero", "Puntaje"), ("Estrato", "Jornada"),
                                       ("Estrato", "Bilingue"), ("Computador", "Periodo"), ("Jornada", "Puntaje"),
                                       ("Bilingue", "Puntaje"),("Calendario", "Puntaje"), ("Periodo", "Puntaje")},

                        black_list = {("Genero_Colegio", "Departamento_Est"), ("Bilingue", "Departamento_Est"),
                                      ("Estrato", "Departamento_Est"), ("Puntaje", "Departamento_Est"),
                                      ("Computador", "Departamento_Est"), ("Genero", "Departamento_Est"),
                                      ("Periodo", "Departamento_Est"), ("Jornada", "Departamento_Est"),
                                      ("Calendario", "Departamento_Est"),

                                      ("Departamento_Est", "Genero"),("Departamento_Est", "Puntaje"),
                                      ("Departamento_Est", "Computador"), ("Departamento_Est", "Jornada"),
                                      ("Departamento_Est", "Calendario"), ("Departamento_Est", "Bilingue"),
                                      ("Departamento_Est", "Periodo"), ("Departamento_Est", "Estrato"),

                                      ("Computador", "Genero"), ("Computador", "Calendario"),
                                      ("Computador", "Departamento_Est"), ("Computador", "Jornada"),
                                      ("Camputador", "Genero_Colegio"), ("Computador", "Bilingue"),
                                      ("Computador", "Puntaje"), ("Computador", "Estrato"),

                                      ("Genero_Colegio", "Estrato"), ("Bilingue", "Estrato"),
                                      ("Departamento_Est", "Estrato"), ("Puntaje", "Estrato"),
                                      ("Computador", "Estrato"), ("Genero", "Estrato"),
                                      ("Periodo", "Estrato"), ("Jornada", "Estrato"),
                                      ("Calendario", "Estrato"),

                                      ("Genero_Colegio", "Genero"), ("Bilingue", "Genero"),
                                      ("Estrato", "Genero"), ("Puntaje", "Genero"),
                                      ("Computador", "Genero"), ("Departamento_Est", "Genero"),
                                      ("Periodo", "Genero"), ("Jornada", "Genero"),
                                      ("Calendario", "Genero"),

                                      ("Genero_Colegio", "Periodo"), ("Bilingue", "Periodo"),
                                      ("Estrato", "Periodo"), ("Puntaje", "Periodo"),
                                      ("Genero", "Periodo"),
                                      ("Departamento_Est", "Periodo"), ("Jornada", "Periodo"),
                                      ("Calendario", "Periodo"),

                                      ("Genero", "Computador"), ("Genero", "Calendario"),
                                      ("Genero", "Departamento_Est"), ("Genero", "Jornada"),
                                      ("Genero", "Genero_Colegio"), ("Genero", "Bilingue"),
                                      ("Genero", "Periodo"), ("Genero", "Estrato"),

                                      ("Estrato", "Calendario"), ("Estrato", "Periodo"),
                                      ("Estrato", "Puntaje"), ("Estrato", "Genero"),
                                      ("Estrato", "Genero_Colegio"), ("Estrato", "Departamento_Est"),

                                      ("Bilingue", "Computador"), ("Bilingue", "Calendario"),
                                      ("Bilingue", "Departamento_Est"), ("Bilingue", "Jornada"),
                                      ("Bilingue", "Genero_Colegio"), ("Bilingue", "Genero"),
                                      ("Bilingue", "Periodo"), ("Bilingue", "Estrato"),

                                      ("Genero_Colegio", "Jornada"), ("Bilingue", "Jornada"),
                                      ("Departamento_Est", "Jornada"), ("Puntaje", "Jornada"),
                                      ("Computador", "Jornada"), ("Genero", "Jornada"),
                                      ("Periodo", "Jornada"), ("Calendario", "Jornada"),

                                      ("Periodo", "Genero_Colegio"), ("Periodo", "Bilingue"),
                                      ("Periodo", "Estrato"), ("Periodo", "Genero"),
                                      ("Periodo", "Computador"), ("Periodo", "Jornada"),
                                      ("Periodo", "Departamento_Est"), ("Periodo", "Calendario"),

                                      ("Genero_Colegio", "Periodo"), ("Genero_Colegio", "Bilingue"),
                                      ("Genero_Colegio", "Estrato"), ("Genero_Colegio", "Genero"),
                                      ("Genero_Colegio", "Computador"), ("Genero_Colegio", "Jornada"),
                                      ("Genero_Colegio", "Departamento_Est"), ("Genero_Colegio", "Calendario"),

                                      ("Jornada", "Periodo"), ("Jornada", "Bilingue"),
                                      ("Jornada", "Estrato"), ("Jornada", "Genero"),
                                      ("Jornada", "Computador"), ("Jornada", "Genero_Colegio"),
                                      ("Jornada", "Departamento_Est"), ("Jornada", "Calendario"),

                                      ("Computador", "Periodo"), ("Computador", "Bilingue"),
                                      ("Computador", "Estrato"), ("Computador", "Genero"),
                                      ("Computador", "Jornada"), ("Computador", "Genero_Colegio"),
                                      ("Computador", "Departamento_Est"), ("Computador", "Calendario")
                                      })

#Periodo', 'Calendario', 'Bilingue', 'Departamento_Est', 'Jornada', 'Genero_Colegio', 'Genero', 'Estrato', 'Puntaje', 'Computador'
modeloK2 = BayesianNetwork()
edges = estimated_modelh.edges()
modeloK2.add_edges_from(edges)

##
graph = nx.DiGraph()
graph.add_nodes_from(modeloK2.nodes())
graph.add_edges_from(modeloK2.edges())
plt.figure(figsize = (5,5))
pos = {'Periodo': (0, 1), 'Calendario': (0, 0), 'Departamento_Est': (0, 2), 'Bilingue': (2, 2), 'Estrato': (3, 1),
       'Genero_Colegio': (1, 2), 'Puntaje': (1, 1), 'Genero': (1, 0), 'Jornada': (2, 1), 'Computador': (2, 0)}
nx.draw(graph, pos = pos ,with_labels = True, node_color = 'pink', node_size = 8000, font_size = 9, arrowsize = 20)

##
modeloK2.fit(data = muestras, estimator = MaximumLikelihoodEstimator)
ModK2 = VariableElimination(modeloK2)
##

emv = MaximumLikelihoodEstimator(model=modeloK2, data=muestras)
##
cpdem_r = emv.estimate_cpd(node="Computador")

######
reader = BIFReader("Proyecto Final/modeloPFinal.bif")

modelo = reader.get_model()

modelo.check_model()

# Infering the posterior probability
from pgmpy.inference import VariableElimination

infer = VariableElimination(modelo)
##
posterior_p = infer.query(["Puntaje"], evidence={'Periodo': '0', 'Calendario': '0', 'Bilingue': '0', 'Departamento_Est': '7',
                                                 'Jornada': '5', 'Genero_Colegio': '0', 'Genero': '0', 'Estrato':'5', 'Computador': '0'})


print(posterior_p)
valores1 = round(posterior_p.values[0],2)
valores2 = round(posterior_p.values[1],2)
valores3 = round(posterior_p.values[2],2)
valores4 = round(posterior_p.values[3],2)
##

valores = [valores1, valores2, valores3, valores4]
maximo = max(valores)
posicion = 0
datos = [ ]
for i in range(0, len(valores)):
    if valores[i] == maximo:
        maximo = valores[i]
        posicion = i

if posicion == 0:
    percentil = '0 y 25'
    minimo = 0
    maximob = 25
    datos = np.append(maximob, datos)
elif posicion == 1:
    percentil = '25 y 50'
    minimo = 25
    maximob = 50
    datos = np.append(maximob, datos)
elif posicion == 2:
    percentil = '50 y 75'
    minimo = 50
    maximob = 75
    datos = np.append(maximob, datos)
elif posicion == 3:
    percentil = '75 y 100'
    minimo = 75
    maximob = 100
    datos = np.append(maximob, datos)

data2 = pd.DataFrame({'Probabilidad': datos})
##
lineas0 = [0,0,0]
lineas25 = [25, 25, 25]
lineas50 = [50,50, 50]
lineas75 = [75,75,75]
lineas1 = [100,100,100]
valoresy = [-0.4, 0, 0.3]
data0 = pd.DataFrame({'lineas0': lineas0, 'valoresy': valoresy})
data25 = pd.DataFrame({'lineas25': lineas25, 'valoresy': valoresy})
data50 = pd.DataFrame({'lineas50': lineas50, 'valoresy': valoresy})
data75 = pd.DataFrame({'lineas75': lineas75, 'valoresy': valoresy})
data1 = pd.DataFrame({'lineas1': lineas1, 'valoresy': valoresy})
etiquetasx = ['0', '25', '50', '75', '100']

##
# Se crea la gráfica de barras
pio.renderers.default = "browser"
fig = go.Figure()
fig.update_layout(height=300, width=800)
#fig = px.bar(data2, x = 'Probabilidad', height=300, text_auto=True, orientation = 'h')
#fig.update_traces(marker_color='#A4D2BC')
fig.add_trace(go.Bar(x = [maximob - minimo], base = minimo,marker_color='#A4D2BC', orientation = 'h', showlegend = False))



fig.add_trace(go.Scatter(x = data0['lineas0'], y = data0['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 0, y = 0.4, text = '0', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data25['lineas25'], y = data25['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 25, y = 0.4, text = '25%', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data50['lineas50'], y = data50['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 50, y = 0.4, text = '50%', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data75['lineas75'], y = data75['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 75, y = 0.4, text = '75%', arrowhead = False, showarrow = False)
fig.add_trace(go.Scatter(x = data1['lineas1'], y = data1['valoresy'], mode = 'lines', line_color = '#728E9D', line_dash = 'dash', showlegend = False))
fig.add_annotation(x = 100, y = 0.4, text = '100%', arrowhead = False, showarrow = False)

if math.isnan(valores1) or math.isnan(valores2) or math.isnan(valores3) or math.isnan(valores4):
    fig.update_layout(width=900, bargap=0.8,
                      plot_bgcolor="rgba(255,255,255,255)",
                      title_text='No es posible calcular la probabilidad con los datos ingresados')
else:
    fig.update_layout(width=900, bargap=0.8,
                      plot_bgcolor="rgba(255,255,255,255)",
                      title_text='El estudiante se encuentra entre los percentiles ' + percentil + ' con una probabilidad de ' + str(maximo), title_x=0.5)

fig.update_xaxes(range=[-0.05, 100.05], showline=True, linewidth=1, linecolor='black', showticklabels=False, title = ' ')
fig.update_yaxes(range=[-0.4, 0.45], showline=True, linewidth=1, mirror=True, showticklabels=False, title = ' ')
fig.show()


###

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
