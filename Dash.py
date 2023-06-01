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
                        html.Div("Contenido de la pestaña 2")]),

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
                                                                                'BOGOTÁ','BOLIVAR','BOYACA','CALDAS','CAQUETA',
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

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=9878, host = "0.0.0.0")


