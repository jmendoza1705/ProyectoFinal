import pandas as pd
import statistics
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import psycopg2
from sqlalchemy import create_engine, text
from statistics import mode
import geopandas
import pyproj
from urllib.request import urlopen
import json
##
# se importan los datos

engine=create_engine('postgresql://postgres:proyectofinal@proyectodb.colrzll4geas.us-east-1.rds.amazonaws.com:5432/proyectodb1')
datos = pd.read_sql(text("SELECT * FROM proyectodb1"), con=engine.connect())


## Visualización 1 y 2
punt_antes_mayor50, punt_antes_menor50, punt_despues_mayor50, punt_despues_menor50 = 0,0,0,0
for i in range (len(datos["Periodo"])):
    if datos["Periodo"][i] == 0:
        if datos["Puntaje"][i] == 0 or datos["Puntaje"][i] == 1:
            punt_antes_menor50 += 1
        elif datos["Puntaje"][i] == 2 or datos["Puntaje"][i] == 3:
            punt_antes_mayor50 += 1
    if datos["Periodo"][i] == 1:
        if datos["Puntaje"][i] == 0 or datos["Puntaje"][i] == 1:
            punt_despues_menor50 += 1
        elif datos["Puntaje"][i] == 2 or datos["Puntaje"][i] == 3:
            punt_despues_mayor50 += 1


d_x = ["Menor al 50%", "Mayor al 50%"]
antes = [punt_antes_menor50, punt_antes_mayor50]
despues = [punt_despues_menor50, punt_despues_mayor50]


fig_v1 = px.bar(x=d_x, y=antes)
fig_v1.update_traces(marker_color='#ADD4D9')
fig_v1.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Saber 11 - 20194', title_x=0.5, title_font_size=20, font=dict(size=16))
fig_v1.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v1.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))
fig_v1.show()

fig_v2 = px.bar(x=d_x, y=despues)
fig_v2.update_traces(marker_color='#A4D2BC')
fig_v2.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Saber 11 - 20211', title_x=0.5, title_font_size=20, font=dict(size=16))
fig_v2.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v2.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))
fig_v2.show()

## Visualización 3 -- quiero el percentil que mas se dio en cada departamento

departamentos = []
for departamento in datos['Departamento_Est'].unique():
    departamentos.append(departamento)
departamentos = sorted(departamentos)

departamentos_punt = []
for dept in departamentos:
    puntajes = datos.loc[datos['Departamento_Est'] == dept, 'Puntaje'].tolist()
    departamentos_punt.append(puntajes)

moda_puntaje = []
personas_moda = []
for i in range(len(departamentos_punt)):
    moda = mode(departamentos_punt[i])
    moda_puntaje.append(moda)
    count = departamentos_punt[i].count(moda)
    personas_moda.append(count)


departamentos_nombre = ['AMAZONAS','ANTIOQUIA','ARAUCA','ATLANTICO','SANTAFE DE BOGOTA D.C','BOLIVAR','BOYACA','CALDAS','CAQUETA',
                        'CASANARE','CAUCA', 'CESAR', 'CHOCO', 'CORDOBA','CUNDINAMARCA', 'GUAINIA','GUAVIARE', 'HUILA',
                        'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO','NORTE SANTANDER','PUTUMAYO', 'QUINDIO',
                        'RISARALDA', 'SAN ANDRES', 'SANTANDER', 'SUCRE','TOLIMA','VALLE', 'VAUPES', 'VICHADA']

datos_punt = {'Departamento': departamentos_nombre, 'Moda': moda_puntaje, "Cantidad": personas_moda}

moda_punt_dept = pd.DataFrame(datos_punt)
mejores_depts = moda_punt_dept.drop(moda_punt_dept[moda_punt_dept['Moda'] == 1].index)


fig_v3 = px.bar(mejores_depts, x='Cantidad', y='Departamento', orientation='h')
fig_v3.update_traces(marker_color='#A4D2BC')
fig_v3.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Personas que obtuvieron un puntaje entre el percentil 50 y 75.', title_x=0.5, title_font_size=20, font=dict(size=16))
fig_v3.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))
fig_v3.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Departamento',tickfont=dict(size=15))
fig_v3.show()

## Visualización 4

# 0 mujer
punt_mujer_50, punt_mujer_mas, punt_hombre_50, punt_hombre_mas = 0,0,0,0
for i in range (len(datos["Genero"])):
    if datos["Genero"][i] == 0:
        if datos["Puntaje"][i] == 0 or datos["Puntaje"][i] == 1:
            punt_mujer_50 += 1
        elif datos["Puntaje"][i] == 2 or datos["Puntaje"][i] == 3:
            punt_mujer_mas += 1
    if datos["Genero"][i] == 1:
        if datos["Puntaje"][i] == 0 or datos["Puntaje"][i] == 1:
            punt_hombre_50 += 1
        elif datos["Puntaje"][i] == 2 or datos["Puntaje"][i] == 3:
            punt_hombre_mas += 1

d_x = ["Menor al 50%", "Mayor al 50%"]
mujeres = [punt_mujer_50, punt_mujer_mas]
hombres = [punt_hombre_50, punt_hombre_mas]


fig_v4 = px.bar(x=d_x, y=mujeres)
fig_v4.update_traces(marker_color='#ADD4D9')
fig_v4.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Percentil del puntaje obtenido en el Saber 11 - Mujeres', title_x=0.5, title_font_size=20, font=dict(size=16))
fig_v4.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v4.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))
fig_v4.show()

fig_v5 = px.bar(x=d_x, y=hombres)
fig_v5.update_traces(marker_color='#526771')
fig_v5.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Percentil del puntaje obtenido en el Saber 11 - Hombres', title_x=0.5, title_font_size=20, font=dict(size=16))
fig_v5.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v5.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))
fig_v5.show()
