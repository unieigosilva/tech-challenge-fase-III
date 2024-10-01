import pickle
import pandas as pd

def get_base(dados):
    data = pd.read_excel(f'./dashboard/data/{dados}.xlsx')

    return data

def get_model():
    with open('./dashboard/model/modelo.pkl', 'rb') as arquivo:
        model = pickle.load(arquivo)

    return model

model = get_model()
dados_normalizados = get_base('dados_normalizados')
tabela_times = get_base('tabela_times')

tabela_times = {
    row['time_mandante']: row['time_mandante_id']
    for _, row in tabela_times.iterrows()
}

teams = [
    'RB Bragantino', 'Cuiabá-MT', 
    'Fortaleza', 'CSA', 'Cruzeiro', 
    'Fluminense', 'Coritiba FC', 
    'Athletico-PR', 'Goiás', 
    'Atlético-MG', 'Figueirense FC', 
    'Ceará SC', 'São Paulo', 'Grêmio', 
    'EC Bahia', 'Santa Cruz', 
    'Criciúma EC', 'Atlético-GO', 
    'Portuguesa', 'Paraná', 
    'Internacional', 'Guarani', 
    'Paysandu SC', 'Ponte Preta', 
    'América-MG', 'Santos', 
    'Santo André', 'Juventude', 
    'Ipatinga FC', 'Palmeiras', 
    'Flamengo', 'Botafogo', 
    'América-RN', 'Santos FC', 
    'EC Vitória', 'Avaí FC', 
    'Sport Recife', 'Vasco da Gama', 
    'Corinthians', 'Chapecoense', 
    'Atlético-PR', 'Náutico', 
    'Goiás EC', 'Joinville-SC', 
    'Barueri', 'Brasiliense-DF', 
    'São Caetano'
]