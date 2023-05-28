import numpy as np
import pandas as pd
##
data = pd.read_csv('Proyecto Final/data.csv')
data2 = pd.read_csv('Proyecto Final/data.csv')
data = data.dropna()
data = data.to_numpy()

##
# Discretización Periodo
# 20194: 0, 20211:1
for i in range(0, len(data)):
    if data[i, 0] == 20194:
        data[i, 0] = 0
    else:
        data[i, 0] = 1

##
# Discretización Calendario
# A: 0, B:1
for i in range(0, len(data)):
    if data[i, 1] == "A":
        data[i, 1] = 0
    else:
        data[i, 1] = 1

##
# Discretización Caracter
# 'ACADÉMICO': 0, 'TÉCNICO':1, 'TÉCNICO/ACADÉMICO': 2, 'NO APLICA':3
for i in range(0, len(data)):
    if data[i, 2] == 'ACADÉMICO':
        data[i, 2] = 0
    elif data[i, 2] == "TÉCNICO":
        data[i, 2] = 1
    elif data[i, 2] == "TÉCNICO/ACADÉMICO":
        data[i, 2] = 2
    else:
        data[i, 2] = 3

##
#Discretización Departamentos
#{'AMAZONAS': 0, 'ANTIOQUIA': 1, 'ARAUCA': 2, 'ATLANTICO': 3, 'BOGOTÁ': 4, 'BOLIVAR': 5, 'BOYACA': 6, 'CALDAS': 7,
#'CAQUETA': 8, 'CASANARE': 9, 'CAUCA': 10, 'CESAR': 11, 'CHOCO': 12, 'CORDOBA': 13, 'CUNDINAMARCA': 14, 'GUAINIA': 15,
#'GUAVIARE': 16, 'HUILA': 17, 'LA GUAJIRA': 18, 'MAGDALENA': 19, 'META': 20, 'NARIÑO': 21, 'NORTE SANTANDER': 22,
#'PUTUMAYO': 23, 'QUINDIO': 24, 'RISARALDA': 25, 'SAN ANDRES': 26, 'SANTANDER': 27, 'SUCRE': 28, 'TOLIMA': 29,
#'VALLE': 30, 'VAUPES': 31, 'VICHADA': 32}

deptos = data[:,3]
departamentos = []

for i in range(0, len(deptos)):
    if deptos[i] not in departamentos:
        departamentos.append(deptos[i])
departamentos.sort()

for i in range(0, len(departamentos)):
    for j in range(0 ,len(deptos)):
        if data[j,3] == departamentos[i]:
            data[j,3] = i

##
#Discretización Jornada
#'COMPLETA': 0, 'MAÑANA': 1, 'NOCHE': 2, 'SABATINA': 3, 'TARDE': 4, 'UNICA': 5
jornadas = ['COMPLETA', 'MAÑANA', 'NOCHE', 'SABATINA', 'TARDE', 'UNICA']

for i in range(0, len(jornadas)):
    for j in range(0 ,len(data)):
        if data[j,4] == jornadas[i]:
            data[j,4] = i

##
#Discretización Genero Colegio
##
#Discretización Puntajes
#0-125 = 0
#126-250 = 1
#251-375 = 2
#376-500 = 3

for i in range (0, len(data)):
    if data[i,-1] <= 125:
        data[i,-1] = 0

    elif data[i,-1] > 125 and data[i,-1] <= 250:
        data[i,-1] = 1

    elif data[i,-1] > 250 and data[i,-1] <= 375:
        data[i,-1] = 2

    elif data[i,-1] > 375 and data[i,-1] <= 500:
        data[i,-1] = 3