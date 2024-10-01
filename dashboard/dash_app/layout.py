from dash import html
import dash_bootstrap_components as dbc
from config import *
from utils import *
from .componentes import *

def layout():
    return dbc.Container([
    html.H1(
        [
            'Predição Brasileirão 2024',
        ],
        className="d-flex justify-content-center"
    ),
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
                    card_team_choice('mandante'),
                    xs=12, 
                    md=4,
                ),
                dbc.Col(
                    result_area(),
                    xs=12, 
                    md=4,
                    class_name="justify-content-center"
                ),
                dbc.Col(
                    card_team_choice('visitante'),
                    xs=12, 
                    md=4,
                ),
            ]),
        ]
    )
], fluid=True)