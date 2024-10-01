from dash import html, dcc
import dash_bootstrap_components as dbc
from config import *

def card_team_choice(type:str):

    return dbc.Card(
        dbc.CardBody(
            [
                html.H2(
                    f'Time {type.title()}',
                    className="d-flex justify-content-center"
                ),
                dcc.Dropdown(
                    options=teams,
                    placeholder="Escolha um time...",
                    id=f'{type}-dropdown',
                ),
                html.H4(
                    "Média de colocações",
                    className="d-flex justify-content-center",
                ),
                html.Label(
                    "###",
                    id=f"{type}-colocacao",
                    className="mb-1 d-flex justify-content-center info",
                ),
                html.H4(
                    "Valor Médio Equipe",
                    className="d-flex justify-content-center",
                ),
                html.Label(
                    "###",
                    id=f"{type}-valor-equipe",
                    className="mb-1 d-flex justify-content-center info",
                ),
                # html.H4(
                #     "Idade Média Equipe",
                #     className="d-flex justify-content-center",
                # ),
                # html.Label(
                #     "###",
                #     id=f"{type}-idade-equipe",
                #     className="mb-1 d-flex justify-content-center info",
                # ),
                html.Div(
                    [
                        html.I(className="fas fa-times fa-lg")
                    ],
                    id=f"{type}-container",
                    className="m-5 d-flex justify-content-center"
                ),
                dcc.Loading(
                    id=f"loading-{type}",
                    children=[html.Div([html.Div(id="loading-predict-output")])],
                    type="circle",
                ),
            ]
        ),
        color="dark",
        # style={"width": "18rem"},
    )

def result_area():
    return [
        html.H2(
            'Possivel Resultado',
            className="d-flex justify-content-center",
        ),
        dbc.Button(
            'Realizar Predição',
            id="predict-button",
            className="w-100"
        ),
        html.Div(
            [],
            id="possible-result",
            className="m-5 d-flex justify-content-center"
        ),
        dcc.Loading(
            id="loading-predict",
            children=[html.Div([html.Div(id="loading-predict-output")])],
            type="circle",
        ),
        html.Div(
            [
                html.I(className="fas fa-futbol fa-lg")
            ],
            id=f"result-container",
            className="m-5 d-flex justify-content-center"
        ),
    ]