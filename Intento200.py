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
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.io as pio
pio.renderers.default = "browser"

####
data = pd.read_csv('Proyecto Final/Datos Discretizados2.csv')
data = data.drop("Bilingue", axis = 1)
data = data.drop("Computador", axis = 1)
names = data.columns.values
data = data.to_numpy()
##
dataEntrenamiento = data[0:615000,:]
dataValidacion = data[615000:,:]

##
#Se definen las muestras con los datos de entrenamiento
muestras = pd.DataFrame(dataEntrenamiento, columns = names)

##
scoring_method = K2Score(data=muestras)
esth = HillClimbSearch(data=muestras)
estimated_modelh = esth.estimate(scoring_method=scoring_method, max_indegree=7, max_iter=int(1e4),
                        fixed_edges = {("Departamento_Est", "Genero_Colegio"),("Genero_Colegio", "Puntaje"),
                                       ("Genero", "Puntaje"), ("Estrato", "Jornada"),
                                       ("Jornada", "Puntaje"), ("Calendario", "Puntaje"), ("Periodo", "Puntaje")},

                        black_list = {("Genero_Colegio", "Departamento_Est"),
                                      ("Estrato", "Departamento_Est"), ("Puntaje", "Departamento_Est"),
                                       ("Genero", "Departamento_Est"),
                                      ("Periodo", "Departamento_Est"), ("Jornada", "Departamento_Est"),
                                      ("Calendario", "Departamento_Est"),

                                      ("Departamento_Est", "Genero"),("Departamento_Est", "Puntaje"),
                                       ("Departamento_Est", "Jornada"),
                                      ("Departamento_Est", "Calendario"),
                                      ("Departamento_Est", "Periodo"), ("Departamento_Est", "Estrato"),

                                      ("Genero_Colegio", "Estrato"),
                                      ("Departamento_Est", "Estrato"), ("Puntaje", "Estrato"),
                                       ("Genero", "Estrato"),
                                      ("Periodo", "Estrato"), ("Jornada", "Estrato"),
                                      ("Calendario", "Estrato"),

                                      ("Genero_Colegio", "Genero"),
                                      ("Estrato", "Genero"), ("Puntaje", "Genero"),
                                       ("Departamento_Est", "Genero"),
                                      ("Periodo", "Genero"), ("Jornada", "Genero"),
                                      ("Calendario", "Genero"),

                                      ("Genero_Colegio", "Periodo"),
                                      ("Estrato", "Periodo"), ("Puntaje", "Periodo"),
                                      ("Genero", "Periodo"),
                                      ("Departamento_Est", "Periodo"), ("Jornada", "Periodo"),
                                      ("Calendario", "Periodo"),

                                      ("Genero", "Calendario"),
                                      ("Genero", "Departamento_Est"), ("Genero", "Jornada"),
                                      ("Genero", "Genero_Colegio"),
                                      ("Genero", "Periodo"), ("Genero", "Estrato"),

                                      ("Estrato", "Calendario"), ("Estrato", "Periodo"),
                                      ("Estrato", "Puntaje"), ("Estrato", "Genero"),
                                      ("Estrato", "Genero_Colegio"), ("Estrato", "Departamento_Est"),

                                      ("Genero_Colegio", "Jornada"),
                                      ("Departamento_Est", "Jornada"), ("Puntaje", "Jornada"),
                                      ("Computador", "Jornada"), ("Genero", "Jornada"),
                                      ("Periodo", "Jornada"), ("Calendario", "Jornada"),

                                      ("Periodo", "Genero_Colegio"),
                                      ("Periodo", "Estrato"), ("Periodo", "Genero"), ("Periodo", "Jornada"),
                                      ("Periodo", "Departamento_Est"), ("Periodo", "Calendario"),

                                      ("Genero_Colegio", "Periodo"),
                                      ("Genero_Colegio", "Estrato"), ("Genero_Colegio", "Genero"),
                                       ("Genero_Colegio", "Jornada"),
                                      ("Genero_Colegio", "Departamento_Est"), ("Genero_Colegio", "Calendario"),

                                      ("Jornada", "Periodo"),
                                      ("Jornada", "Estrato"), ("Jornada", "Genero"),
                                       ("Jornada", "Genero_Colegio"),
                                      ("Jornada", "Departamento_Est"), ("Jornada", "Calendario"),

                                      })

#Periodo', 'Calendario', 'Bilingue', 'Departamento_Est', 'Jornada', 'Genero_Colegio', 'Genero', 'Estrato', 'Puntaje', 'Computador'
modeloK2 = BayesianNetwork()
edges = estimated_modelh.edges()
modeloK2.add_edges_from(edges)

##
graph = nx.DiGraph()
graph.add_nodes_from(estimated_modelh.nodes())
graph.add_edges_from(estimated_modelh.edges())
plt.figure(figsize = (5,5))
pos = {'Jornada': (2, 2), 'Calendario': (0, 0), 'Departamento_Est': (0, 2), 'Estrato': (3, 1),
       'Genero_Colegio': (1, 2), 'Puntaje': (1, 1), 'Genero': (1, 0), 'Periodo': (2, 1), 'Computador': (2, 0)}
nx.draw(graph, pos = pos ,with_labels = True, node_color = 'pink', node_size = 8000, font_size = 9, arrowsize = 20)

##
modeloK2.fit(data = muestras, estimator = MaximumLikelihoodEstimator)
ModK2 = VariableElimination(modeloK2)
##

emv = MaximumLikelihoodEstimator(model=modeloK2, data=muestras)
##
cpdem_r = emv.estimate_cpd(node="Puntaje")