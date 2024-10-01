import os
import requests
import pandas as pd
import pickle
from config import *
from dash import html
from dotenv import load_dotenv
load_dotenv()

def calculate_rolling_performance(df, team_column, result_column, rolling_window=5):
    # Create a copy to avoid modifying the original data
    performance = df[[team_column, result_column]].copy()
    performance['is_win'] = performance[result_column].apply(lambda x: 1 if x == 1 else 0)
    
    # Group by team and calculate rolling win rate
    rolling_performance = performance.groupby(team_column)['is_win'].rolling(window=rolling_window, min_periods=1).mean().reset_index(0, drop=True)
    
    return rolling_performance

def get_team_info(team_name):

    # Cabeçalho com a chave de API
    headers = {
        'X-Auth-Token': os.environ.get("PI_FOOTBALL_KEY")
    }

    # URL do endpoint de times para uma competição (por exemplo, Brasileirão Série A)
    url = "https://api.football-data.org/v4/competitions/BSA/teams"

    # Fazer a requisição
    response = requests.get(url, headers=headers)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        
        data = response.json()
        teams = data['teams']
        filtered_team = [team for team in teams if team_name.lower() in team['name'].lower()]
        
        if filtered_team:
            return html.Img(
                id='result-img',
                src=filtered_team[0]['crest'],
                className='img-fluid d-flex justify-content-center result-img',
            )
        
    else:
        print(f"Erro: {response.status_code}")
        print(response)
    
    return html.Label(
        'Não foi possivel encontrar uma imagem para esse time',
        className="d-flex justify-content-center",
    )

def get_team_data(team, type):

    team_id = tabela_times[team]

    team_data = dados_normalizados[dados_normalizados[f'time_{type}_id'] == team_id]

    item_maior_index = team_data.loc[team_data.index.max()]

    print(item_maior_index)
    
    return {
        'team_id': team_id,
        'colocacao':item_maior_index[f'colocacao_{type}'], 
        'valor':item_maior_index[f'valor_equipe_titular_{type}']
    }

def prediction_teams(mandante, visitante):

    mandante_data = get_team_data(mandante, 'mandante')
    visitante_data = get_team_data(visitante, 'visitante')

    data = {
        "ano_campeonato": [2024], #ID Time Mandante
        "time_mandante_id": [mandante_data['team_id']], 
        "time_visitante_id": [visitante_data['team_id']], 
        "colocacao_mandante": [mandante_data['colocacao']], 
        "colocacao_visitante":[visitante_data['colocacao']], 
        "valor_equipe_titular_mandante": [mandante_data['valor']], 
        "valor_equipe_titular_visitante": [visitante_data['valor']], 
    }

    # Creating a DataFrame for the São Paulo x Corinthians match
    match_data = pd.DataFrame(data)

    # Making a prediction using the trained model
    match_prediction = model.predict(match_data)

    # Mapping the prediction to the result
    result_map = {1: mandante, 0: 'Empate', 2: visitante}
    predicted_result = result_map[match_prediction[0]]

    return predicted_result