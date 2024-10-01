import dash
from dash import html, Output, Input, State
from utils import *
from config import *
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def register_callbacks(app):

    @app.callback(
        [
            Output('mandante-colocacao', 'children'),
            Output('mandante-valor-equipe', 'children'),
            # Output('mandante-idade-equipe', 'children'),
            Output('mandante-container', 'children'),
            Output('visitante-colocacao', 'children'),
            Output('visitante-valor-equipe', 'children'),
            # Output('visitante-idade-equipe', 'children'),
            Output('visitante-container', 'children'),
            Output('loading-mandante', 'children'),
            Output('loading-visitante', 'children'),
        ],
        Input('mandante-dropdown', 'value'),
        Input('visitante-dropdown', 'value'),
        State('mandante-container', 'children'),
        State('visitante-container', 'children'),
        
        State('mandante-colocacao', 'children'),
        State('mandante-valor-equipe', 'children'),
        State('visitante-colocacao', 'children'),
        State('visitante-valor-equipe', 'children'),
        State('loading-mandante', 'children'),
        State('loading-visitante', 'children'),
    )
    def get_icon(
        mandante, 
        visitante,
        mandante_img,
        visitante_img,
        mandante_colocacao,
        mandante_valor,
        visitante_colocacao,
        visitante_valor,
        loading_m,
        loading_v,
    ):

        trigger_id = dash.callback_context.triggered[0]['prop_id']

        not_found = html.I(className="fas fa-times fa-lg")

        if mandante:
            if 'mandante' in trigger_id:
                mandante_img = get_team_info(mandante)
                team_data = get_team_data(mandante, 'mandante')
                mandante_colocacao = team_data['colocacao']
                mandante_valor = locale.currency(team_data['valor'], grouping=True)
        else:
            mandante_img = not_found
            mandante_colocacao = '###'
            mandante_valor = '###'

        if visitante:
            if 'visitante' in trigger_id:
                visitante_img = get_team_info(visitante)
                team_data = get_team_data(visitante, 'visitante')
                visitante_colocacao = team_data['colocacao']
                visitante_valor = locale.currency(team_data['valor'], grouping=True)
        else:
            visitante_img = not_found
            visitante_colocacao = '###'
            visitante_valor = '###'

        return [
            mandante_colocacao,
            mandante_valor,
            mandante_img,
            visitante_colocacao,
            visitante_valor,
            visitante_img,
            loading_m,
            loading_v,
        ]
    
    @app.callback(
        [
            Output('possible-result', 'children'),
            Output('result-container', 'children'),
            Output('loading-predict', 'children'),
        ],
        Input('predict-button', 'n_clicks'),
        State('mandante-dropdown', 'value'),
        State('visitante-dropdown', 'value'),
        State('mandante-container', 'children'),
        State('visitante-container', 'children'),
        State('possible-result', 'children'),
        State('result-container', 'children'),
        State('loading-predict', 'children'),
    )
    def predict_match(
        n_clicks, 
        mandante, 
        visitante, 
        mandante_icon,
        visitante_icon,
        possible_result,
        result_container,
        loading
    ):
        trigger_id = dash.callback_context.triggered[0]['prop_id']

        if 'predict-button' in trigger_id:
            
            possible_result = html.Label(
                'Selecione os times para que a predição possa ser realizada.',
                className="d-flex justify-content-center mt-2",
            )

            result_container = [
                html.I(className="fas fa-futbol fa-lg"),
            ]

            if mandante and visitante:

                prediction = prediction_teams(mandante, visitante)

                possible_result = [
                    html.P(
                        f'Em um possivel jogo entre {mandante} X {visitante} o resultado possível é: {prediction}',
                        className="d-flex justify-content-center"
                    )
                ]

                if prediction == 'Empate':
                    result_container = html.I(className="fas fa-equals fa-lg")

                elif prediction == mandante:
                    result_container = mandante_icon

                elif prediction == visitante:
                    result_container = visitante_icon

                else:
                    result_container = html.I(className="fas fa-futbol fa-lg")

        return [
            possible_result,
            result_container,
            loading
        ]
