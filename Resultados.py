import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pgmpy.readwrite import BIFReader
import plotly.graph_objs as go
import plotly.io as pio
import math
import plotly.express as px
from pgmpy.inference import VariableElimination
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score

pio.renderers.default = "browser"
##
reader = BIFReader("Proyecto Final/modeloPFinal.bif")
modelo = reader.get_model()
modelo.check_model()

# Infering the posterior probability
infer = VariableElimination(modelo)
##
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
fig.add_trace(go.Bar(x = [maximob - minimo], base = minimo, marker_color='#A4D2BC', orientation = 'h', showlegend = False))
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


####
#Métricas de Desempeño

data = pd.read_csv('Proyecto Final/Datos Discretizados3.csv')
names = data.columns.values
data = data.to_numpy()
##
dataEntrenamiento = data[0:615000,:]
dataValidacion = data[615000:,:]
anotaciones = []
predicciones = []
for i in range(0, len(dataValidacion)):



    variables = [dataValidacion[i, 0], dataValidacion[i, 1], dataValidacion[i, 4], dataValidacion[i, 2],
                 dataValidacion[i, 5], dataValidacion[i, 6], dataValidacion[i, 3], dataValidacion[i, 7], dataValidacion[i, 9]]
    posterior_p = infer.query(["Puntaje"], evidence={'Periodo': str(variables[0]), 'Calendario': str(variables[1]),
                                                     'Jornada': str(variables[2]), 'Bilingue': str(variables[3]),
                                                     'Genero_Colegio': str(variables[4]), 'Genero': str(variables[5]),
                                                     'Departamento_Est': str(variables[6]), 'Estrato': str(variables[7]),
                                                     'Computador': str(variables[8])})
    probabilidades = posterior_p.values



    maximo = np.max(probabilidades)

    for j in range(0, len(probabilidades)):
        if probabilidades[0] != probabilidades[1] and probabilidades[1] != probabilidades[2] and probabilidades[2] != probabilidades[3]:
            if probabilidades[j] == maximo and ~np.isnan(probabilidades).any():
                posicion = j
                predicciones = np.append(predicciones, posicion)
                anotaciones = np.append(anotaciones, dataValidacion[i, 8])
        elif probabilidades[0] == probabilidades[1] and probabilidades[1] == probabilidades[2] and probabilidades[2] == probabilidades[3]:
            continue



########### Matriz de Confusión y Resultados Estadísticos ###########
matriz = confusion_matrix(anotaciones, predicciones)
cm_display = ConfusionMatrixDisplay(confusion_matrix = matriz, display_labels = ['0', '1','2', '3'])
cm_display.plot(cmap = 'PuRd', colorbar = True)
plt.title('Matriz de Confusión para Predicción de Enfermedad Cardiaca (EC) \n Modelo Proyecto 1 \n')
plt.ylabel('Anotaciones')
plt.xlabel('Predicciones')
plt.tight_layout()
plt.show()

precision = precision_score(anotaciones, predicciones, average = 'weighted')
cobertura = recall_score(anotaciones, predicciones, average = 'weighted')
f1 = f1_score(anotaciones, predicciones, average = 'weighted')
print('Precisión:', round(precision,2), '\nCobertura:', round(cobertura,2), '\nF1-Score:', round(f1,2))
