import dash_bootstrap_components as dbc
from dash import Dash
from dash_app.layout import *
from .callbacks import register_callbacks

external_stylesheets = [
    __name__, 
    dbc.themes.CERULEAN,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = layout()

register_callbacks(app)