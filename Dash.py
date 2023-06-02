# Alejandra Erazo
# Juliana Mendoza
# Proyecto Final

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pgmpy.models import BayesianNetwork, BayesianModel
from pgmpy.inference import VariableElimination
from pgmpy.estimators import MaximumLikelihoodEstimator, PC
from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import K2Score, BicScore
import math
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = "browser"
import psycopg2
from sqlalchemy import create_engine, text
import os
from pgmpy.readwrite import BIFReader
from statistics import mode

# VISUALIZACIONES ---------------------------------------------------------------------------------------------------------------------

# se importan los datos
engine=create_engine('postgresql://postgres:proyectofinal@proyectodb.colrzll4geas.us-east-1.rds.amazonaws.com:5432/proyectodb1')
datos = pd.read_sql(text("SELECT * FROM proyectodb1"), con=engine.connect())

# Visualización 1 y 2
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
fig_v1.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Saber 11 - 20194', title_x=0.5,
                     title_font_size=20, font=dict(size=16), bargap=0.3)
fig_v1.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v1.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))

fig_v2 = px.bar(x=d_x, y=despues)
fig_v2.update_traces(marker_color='#728E9D')
fig_v2.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Saber 11 - 20211', title_x=0.5, title_font_size=20,
                     font=dict(size=16), bargap=0.3)
fig_v2.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v2.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))

# Visualización 3
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


departamentos_nombre = ['AMAZONAS','ANTIOQUIA','ARAUCA','ATLANTICO','BOGOTA','BOLIVAR','BOYACA','CALDAS','CAQUETA',
                        'CASANARE','CAUCA', 'CESAR', 'CHOCO', 'CORDOBA','CUNDINAMARCA', 'GUAINIA','GUAVIARE', 'HUILA',
                        'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO','NORTE SANTANDER','PUTUMAYO', 'QUINDIO',
                        'RISARALDA', 'SAN ANDRES', 'SANTANDER', 'SUCRE','TOLIMA','VALLE', 'VAUPES', 'VICHADA']

datos_punt = {'Departamento': departamentos_nombre, 'Moda': moda_puntaje, "Cantidad": personas_moda}

moda_punt_dept = pd.DataFrame(datos_punt)
mejores_depts = moda_punt_dept.drop(moda_punt_dept[moda_punt_dept['Moda'] == 1].index)


fig_v3 = px.bar(mejores_depts, x='Cantidad', y='Departamento', orientation='h')
fig_v3.update_traces(marker_color='#A4D2BC')
fig_v3.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Personas que obtuvieron un puntaje entre el percentil 25 y 50', title_x=0.5, title_font_size=20, font=dict(size=16))
fig_v3.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))
fig_v3.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Departamento',tickfont=dict(size=15))

# Visualización 4 y 5
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
fig_v4.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Percentil del puntaje obtenido en el Saber 11 - Mujeres',
                     title_x=0.5, title_font_size=20, font=dict(size=16), bargap=0.3)
fig_v4.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v4.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))

fig_v5 = px.bar(x=d_x, y=hombres)
fig_v5.update_traces(marker_color='#728E9D')
fig_v5.update_layout(width=1000,plot_bgcolor="rgba(255,255,255,255)",title_text='Percentil del puntaje obtenido en el Saber 11 - Hombres',
                     title_x=0.5, title_font_size=20, font=dict(size=16), bargap=0.3)
fig_v5.update_xaxes( showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Percentil',tickfont=dict(size=15))
fig_v5.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, title_text='Frecuencia',tickfont=dict(size=15))


# FUNCIÓN DE DISCRETIZACIÓN -------------------------------------------------------------------------------------------------------
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
    departamentos = ['AMAZONAS', 'ANTIOQUIA', 'ARAUCA', 'ATLANTICO', 'BOGOTA', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETA',
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

    datos.extend([str(periodoD), str(calendarioD), str(jornadaD), str(bilingueD), str(genero_colD), str(genero_estD), str(departamentoD), str(estratoD), str(computadorD)])
    return datos

# IMPORTACIÓN DEL MODELO ----------------------------------------------------------------------------------------------------------
reader = BIFReader("Proyecto Final/modeloPFinal.bif")
modelo = reader.get_model()
modelo.check_model()
# Infering the posterior probability
infer = VariableElimination(modelo)

# DASH -------------------------------------------------------------------------------------------------------------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

ruta_imagen = "https://colnazareth.edu.co/images/icfes2.png"
imagen2 = "https://www.elcolombiano.com/documents/10157/0/580x365/0c0/0d0/none/11101/KIMT/image_content_28178409_20170304154639.jpg"

app.layout = html.Div(style={'overflowY': 'auto'},
    children=[
        html.H1(
            children=[
                "Resultados del Examen Saber 11",
                html.Img(
                    src=ruta_imagen,
                    style={
                        "position": "absolute",
                        "top": "0",
                        "left": "0",
                        "width": "150px",
                        "height": "150px"})],
            style={
                "color": "white",
                "backgroundColor": "#ADD4D9",
                "textAlign": "center",
                "padding": "50px",
                "position": "relative",
                "font-size": "55px"}),

        dcc.Tabs(
            id="tabs",
            value="inicio",
            children=[
            # Tab 1: Inicio
                dcc.Tab(style={'backgroundColor':'#FAFAF3', 'fontSize': '18px', "color": "#526771"},
                    label="Inicio",
                    value="inicio",
                    children=[
                        html.Div(
                            className="texto",
                            style={"flex": "1"},
                            children=[
                                html.Br(),
                                html.Br(),
                                html.H6("Las pruebas Saber 11 son de carácter obligarotio en Colombia para el ingreso a la "
                                        "educación superior. Estas pruebas permiten realizar un censo periódico de las "
                                        "competencias básicas de los estudiantes, con el propósito de definir estrategias que "
                                        "mejoren la calidad de la educación. ", style={"color": "#526771", 'fontSize': '18px'}),
                                html.H6("En este tablero interactivo los usuarios puedan acceder a información descriptiva "
                                        "sobre los resultados de las pruebas Saber 11 de los últimos años y generar predicciones "
                                        "del puntaje que se puede obtener teniendo en cuenta las siguientes variables: ",
                                        style={"color": "#526771", 'fontSize': '18px'}),
                                html.Div(
                                    style={'display': 'flex', 'justify-content': 'center'},
                                    children=[
                                        html.Div(
                                            style={'margin-right': '20px', 'align-self': 'flex-start', 'width': '50%'},
                                            children=[
                                                html.H6(
                                                    dcc.Markdown('''
                                                        * **Periodo:** Periodo de realización del examen.
                                                        * **Calendario:** Calendario académico.
                                                        * **Jornada:** Jornada de estudio.
                                                        * **Bilingue:** El colegio enseña sus asignaturas en 2 idiomas.
                                                        * **Genero del colegio:** El colegio es mixto, femenino o masculino.
                                                        * **Genero del estudiante:** Femenino o masculino.
                                                        * **Departamento:** Departamento de residencia.
                                                        * **Estrato:** Estrato social del estudiante.
                                                        * **Computador:** El estudiante cuenta con un computador propio.
                                                    '''), style={"color": "#526771",'fontSize': '16px'})]),
                                        html.Div(
                                            style={'display': 'flex', 'align-items': 'center', 'width': '50%',
                                                   'justify-content': 'center'},
                                            children=[
                                                html.Img(
                                                    src=imagen2,
                                                    style={"width": "300px", "height": "300px"})])
                                ])


                    ])]),

            # Tab 2: Visualizaciones
                dcc.Tab(style={'backgroundColor':'#FAFAF3', 'fontSize': '18px', "color": "#526771"},
                    label="Visualizaciones",
                    value="tab-2",
                    children=[
                        html.Div(children=[
                            html.Br(),
                            html.Div(html.H6('Resultados de las pruebas Saber 11 antes y después de la pandemia por COVID-19'),
                                     style={'backgroundColor': "#D8E7E7", "color": "#526771",
                                         'textAlign': 'center', 'fontSize': '18px'}),
                            html.Br(),
                            html.Div([
                                html.Div(children=[
                                    dcc.Graph(id='graph1', figure=fig_v1),], className='six columns'),
                                html.Div(children=[
                                    dcc.Graph(id='graph2', figure=fig_v2),], className='six columns')], className='row'),

                            html.Br(),
                            html.Div(html.H6('A continuación se presentan los departamentos con mejores resultados en la prueba Saber 11.'
                                             ' Se presenta la cantidad de estudiantes que obtuvieron un puntaje entre el percentil'
                                             ' 25 y 50 para estos departamentos.'),
                                     style={'backgroundColor': "#D8E7E7", "color": "#526771",
                                            'textAlign': 'center', 'fontSize': '18px'}),
                            html.Br(),
                            html.Div([
                                dcc.Graph(
                                    id='graph3',
                                    figure=fig_v3),], className='row'),

                            html.Br(),
                            html.Div(html.H6('Resultados de las pruebas Saber 11 según el Género del Estudiante'),
                                     style={'backgroundColor': "#D8E7E7", "color": "#526771",
                                         'textAlign': 'center', 'fontSize': '18px'}),
                            html.Br(),
                            html.Div([
                                html.Div(children=[
                                    dcc.Graph(id='graph4', figure=fig_v4),], className='six columns'),
                                html.Div(children=[
                                    dcc.Graph(id='graph5', figure=fig_v5),], className='six columns')], className='row'),

                        ])]),

            # Tab 3: Predicciones
                dcc.Tab(style={'backgroundColor':'#FAFAF3', 'fontSize': '18px', "color": "#526771"},
                    label="Predicciones",
                    value="tab-3",
                    children=[
                        html.Div([

                            html.Br(),
                            # Sección que indica la instrucción a seguir
                            html.Div(html.H6('Seleccione los valores de los parámetros para hacer la predicción'),
                                     style={'backgroundColor': "#D8E7E7", "color": "#526771",
                                            'textAlign': 'center', 'fontSize': '18px'}),
                            html.Br(),

                            # Listas desplegables
                            html.Div([
                            html.Div(html.H6("Periodo", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='periodo',
                                    options=[{'label': i, 'value': i} for i in ["20194", "20211"]])],
                                    style={'width': '35%', 'display': 'inline-block'}),

                            html.Div(html.H6("Calendario", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='calendario',
                                    options=[{'label': i, 'value': i} for i in ["A", "B", "OTRO"]])],
                                    style={'width': '35%', 'display': 'inline-block'}),

                            html.Div(html.H6("Jornada", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='jornada',
                                    options=[{'label': i, 'value': i} for i in ['COMPLETA', 'MAÑANA', 'NOCHE',
                                                                                'SABATINA', 'TARDE', 'UNICA']])],
                                    style={'width': '35%', 'display': 'inline-block'})],style={'columnCount': 3}),


                            html.Div([
                            html.Div(html.H6("Bilingue", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='bilingue',
                                    options=[{'label': i, 'value': i} for i in ["No", "Si"]])],
                                    style={'width': '35%', 'display': 'inline-block'}),

                            html.Div(html.H6("Género de Colegio", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='genero_col',
                                    options=[{'label': i, 'value': i} for i in ["FEMENINO", "MASCULINO", "MIXTO"]])],
                                    style={'width': '35%', 'display': 'inline-block'}),

                            html.Div(html.H6("Género del Estudiante", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='genero_est',
                                    options=[{'label': i, 'value': i} for i in ["F", "M"]])],
                                    style={'width': '35%', 'display': 'inline-block'})], style={'columnCount': 3}),


                            html.Div([
                            html.Div(html.H6("Departamento", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='departamento',
                                    options=[{'label': i, 'value': i} for i in ['AMAZONAS','ANTIOQUIA','ARAUCA','ATLANTICO',
                                                                                'BOGOTA','BOLIVAR','BOYACA','CALDAS','CAQUETA',
                                                                                'CASANARE','CAUCA', 'CESAR', 'CHOCO', 'CORDOBA',
                                                                                'CUNDINAMARCA', 'GUAINIA','GUAVIARE', 'HUILA',
                                                                                'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO',
                                                                                'NORTE SANTANDER','PUTUMAYO', 'QUINDIO',
                                                                                'RISARALDA', 'SAN ANDRES', 'SANTANDER', 'SUCRE',
                                                                                'TOLIMA','VALLE', 'VAUPES', 'VICHADA']])],
                                    style={'width': '35%', 'display': 'inline-block'}),

                            html.Div(html.H6("Estrato", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='estrato',
                                    options=[{'label': i, 'value': i} for i in ["Estrato 1", "Estrato 2", "Estrato 3",
                                                                                "Estrato 4", "Estrato 5","Estrato 6",
                                                                                "No sabe"]])],
                                    style={'width': '35%', 'display': 'inline-block'}),

                            html.Div(html.H6("Computador", style={"color": "#576DA6"})),
                            html.Div([
                                dcc.Dropdown(
                                    id='computador',
                                    options=[{'label': i, 'value': i} for i in ["No", "Si"]])],
                                style={'width': '35%', 'display': 'inline-block'})], style={'columnCount': 3}),


                            # Se crea el botón
                            html.Div([
                            html.Br(),
                            html.Br(),
                            html.Button('Realizar predicción', id='boton', n_clicks=0,
                                        style={'color': '#526771',
                                            'backgroundColor': '#D8E7E7',
                                            'fontSize': '18px'}),
                            dcc.Interval(id='interval', interval=500)]),

                            # Se crea la gráfica
                            html.Div([
                            html.Br(),
                            html.Br(),
                            dcc.Graph(id='graficaProb')])])])])])


# Función de Callback
@app.callback(
    Output('graficaProb', "figure"),
    [Input('boton', "n_clicks")],
    [State('periodo', 'value'),
     State('calendario', 'value'),
     State('jornada', 'value'),
     State('bilingue', 'value'),
     State('genero_col', 'value'),
     State('genero_est', 'value'),
     State('departamento', 'value'),
     State('estrato', 'value'),
     State('computador', 'value')],prevent_initial_call=True, suppress_callback_exceptions=True)

def update_figure(n_clicks, periodo, calendario, jornada, bilingue, genero_col, genero_est, departamento, estrato, computador):
    variables = Discretizacion(periodo, calendario, jornada, bilingue, genero_col, genero_est, departamento, estrato,
                               computador)

    periodo = variables[0]
    calendario = variables[1]
    jornada = variables[2]
    bilingue = variables[3]
    genero_col = variables[4]
    genero_est = variables[5]
    departamento = variables[6]
    estrato = variables[7]
    computador = variables[8]

    posterior_p = infer.query(["Puntaje"], evidence={'Periodo': periodo, 'Calendario': calendario,
                                                     'Jornada': jornada, 'Bilingue': bilingue,
                                                     'Genero_Colegio': genero_col, 'Genero': genero_est,
                                                     'Departamento_Est': departamento, 'Estrato':estrato,
                                                     'Computador': computador})

    valores1 = round(posterior_p.values[0], 2)
    valores2 = round(posterior_p.values[1], 2)
    valores3 = round(posterior_p.values[2], 2)
    valores4 = round(posterior_p.values[3], 2)

    valores = [valores1, valores2, valores3, valores4]
    maximo = max(valores)
    posicion = 0
    datos = []
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

    lineas0 = [0, 0, 0]
    lineas25 = [25, 25, 25]
    lineas50 = [50, 50, 50]
    lineas75 = [75, 75, 75]
    lineas1 = [100, 100, 100]
    valoresy = [-0.4, 0, 0.3]
    data0 = pd.DataFrame({'lineas0': lineas0, 'valoresy': valoresy})
    data25 = pd.DataFrame({'lineas25': lineas25, 'valoresy': valoresy})
    data50 = pd.DataFrame({'lineas50': lineas50, 'valoresy': valoresy})
    data75 = pd.DataFrame({'lineas75': lineas75, 'valoresy': valoresy})
    data1 = pd.DataFrame({'lineas1': lineas1, 'valoresy': valoresy})
    etiquetasx = ['0', '25', '50', '75', '100']

    # Se crea la gráfica de barras
    pio.renderers.default = "browser"
    fig = go.Figure()
    fig.update_layout(height=300, width=800)
    fig.add_trace(go.Bar(x=[maximob - minimo], base=minimo, marker_color='#A4D2BC', orientation='h', showlegend=False))
    fig.add_trace(
        go.Scatter(x=data0['lineas0'], y=data0['valoresy'], mode='lines', line_color='#728E9D', line_dash='dash',
                   showlegend=False))
    fig.add_annotation(x=0, y=0.4, text='0', arrowhead=False, showarrow=False)
    fig.add_trace(
        go.Scatter(x=data25['lineas25'], y=data25['valoresy'], mode='lines', line_color='#728E9D', line_dash='dash',
                   showlegend=False))
    fig.add_annotation(x=25, y=0.4, text='25%', arrowhead=False, showarrow=False)
    fig.add_trace(
        go.Scatter(x=data50['lineas50'], y=data50['valoresy'], mode='lines', line_color='#728E9D', line_dash='dash',
                   showlegend=False))
    fig.add_annotation(x=50, y=0.4, text='50%', arrowhead=False, showarrow=False)
    fig.add_trace(
        go.Scatter(x=data75['lineas75'], y=data75['valoresy'], mode='lines', line_color='#728E9D', line_dash='dash',
                   showlegend=False))
    fig.add_annotation(x=75, y=0.4, text='75%', arrowhead=False, showarrow=False)
    fig.add_trace(
        go.Scatter(x=data1['lineas1'], y=data1['valoresy'], mode='lines', line_color='#728E9D', line_dash='dash',
                   showlegend=False))
    fig.add_annotation(x=100, y=0.4, text='100%', arrowhead=False, showarrow=False)

    if math.isnan(valores1) or math.isnan(valores2) or math.isnan(valores3) or math.isnan(valores4):
        fig.update_layout(width=900, bargap=0.8,
                          plot_bgcolor="rgba(255,255,255,255)",
                          title_text='No es posible calcular la probabilidad con los datos ingresados')
    else:
        fig.update_layout(width=900, bargap=0.8,
                          plot_bgcolor="rgba(255,255,255,255)",
                          title_text='El estudiante se encuentra entre los percentiles ' + percentil + ' con una probabilidad de ' + str(
                              maximo), title_x=0.5)

    fig.update_xaxes(range=[-0.05, 100.05], showline=True, linewidth=1, linecolor='black', showticklabels=False,
                     title=' ')
    fig.update_yaxes(range=[-0.4, 0.45], showline=True, linewidth=1, mirror=True, showticklabels=False, title=' ')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=9878, host = "0.0.0.0")


