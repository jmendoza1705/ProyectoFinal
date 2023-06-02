import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork, BayesianModel
from pgmpy.inference import VariableElimination
from pgmpy.estimators import MaximumLikelihoodEstimator, PC
from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import K2Score, BicScore
import math
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.readwrite import BIFWriter, BIFReader
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.io as pio
pio.renderers.default = "browser"
import psycopg2
from sqlalchemy import create_engine, text

#### Se cargan los datos
engine=create_engine('postgresql://postgres:proyectofinal@proyectodb.colrzll4geas.us-east-1.rds.amazonaws.com:5432/proyectodb1')
data = pd.read_sql(text("SELECT * FROM proyectodb1"), con=engine.connect())
names = data.columns.values
data = data.to_numpy()

# Se dividen los datos en conjuntos de entrenamiento y prueba
dataEntrenamiento = data[0:615000,:]
dataValidacion = data[615000:,:]
##
#Se definen las muestras con los datos de entrenamiento
muestras = pd.DataFrame(dataEntrenamiento, columns = names)

# Modelo K2
scoring_method = K2Score(data=muestras)
esth = HillClimbSearch(data=muestras)
estimated_modelh = esth.estimate(scoring_method=scoring_method, max_indegree=7, max_iter=int(1e4),
                        fixed_edges = {("Departamento_Est", "Genero_Colegio"),("Genero_Colegio", "Puntaje"),
                                       ("Genero", "Puntaje"), ("Estrato", "Jornada"),
                                       ("Estrato", "Bilingue"), ("Computador", "Puntaje"), ("Jornada", "Puntaje"),
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
                                      ("Computador", "Periodo"), ("Computador", "Estrato"),

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
                                      ("Estrato", "Periodo"), ("Computador", "Periodo"),
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
                                      ("Computador", "Departamento_Est"), ("Computador", "Calendario"),

                                      ("Calendario", "Periodo"), ("Calendario", "Bilingue"),
                                      ("Calendario", "Estrato"), ("Calendario", "Genero"),
                                      ("Calendario", "Jornada"), ("Calendario", "Genero_Colegio"),
                                      ("Calendario", "Departamento_Est"), ("Calendario", "Computador")
                                      })


modeloK2 = BayesianNetwork()
edges = estimated_modelh.edges()
modeloK2.add_edges_from(edges)
modeloK2.fit(data = muestras, estimator = MaximumLikelihoodEstimator)
modeloK2.check_model()

# Grafo
graph = nx.DiGraph()
graph.add_nodes_from(estimated_modelh.nodes())
graph.add_edges_from(estimated_modelh.edges())
plt.figure(figsize = (5,5))
pos = {'Periodo': (0, 1), 'Calendario': (0, 0), 'Departamento_Est': (0, 2), 'Bilingue': (2, 2), 'Estrato': (3, 1),
       'Genero_Colegio': (1, 2), 'Puntaje': (1, 1), 'Genero': (1, 0), 'Jornada': (2, 1), 'Computador': (2, 0)}
nx.draw(graph, pos = pos ,with_labels = True, node_color = 'pink', node_size = 8000, font_size = 9, arrowsize = 20)

## Archivo del modelo

writer = BIFWriter(modeloK2)
writer.write_bif(filename='modeloPFinal.bif')