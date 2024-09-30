# config.py

from enum import Enum

# Definir um Enum para as competições
class CompeticaoEnum(str, Enum):
    brasileirao = "brasileirao"
    copa_brasil = "copa_brasil"

# Caminhos para os arquivos CSV das competições
CSV_FILES = {
    CompeticaoEnum.brasileirao: "Dados/mundo_transfermarkt_competicoes_brasileirao_serie_a.csv",
    CompeticaoEnum.copa_brasil: "Dados/mundo_transfermarkt_competicoes_copa_brasil.csv"
}

# Nomes das colunas para cada competição
COLUNAS_COMPETICOES = {
    CompeticaoEnum.brasileirao: [
        "ano_campeonato",
        "data",
        "rodada",
        "estadio",
        "arbitro",
        "publico",
        "publico_max",
        "time_mandante",
        "time_visitante",
        "tecnico_mandante",
        "tecnico_visitante",
        "colocacao_mandante",
        "colocacao_visitante",
        "valor_equipe_titular_mandante",
        "valor_equipe_titular_visitante",
        "idade_media_titular_mandante",
        "idade_media_titular_visitante",
        "gols_mandante",
        "gols_visitante",
        "gols_1_tempo_mandante",
        "gols_1_tempo_visitante",
        "escanteios_mandante",
        "escanteios_visitante",
        "faltas_mandante",
        "faltas_visitante",
        "chutes_bola_parada_mandante",
        "chutes_bola_parada_visitante",
        "defesas_mandante",
        "defesas_visitante",
        "impedimentos_mandante",
        "impedimentos_visitante",
        "chutes_mandante",
        "chutes_visitante",
        "chutes_fora_mandante",
        "chutes_fora_visitante"
    ],
    CompeticaoEnum.copa_brasil: [
        "ano_campeonato",
        "data",
        "horario",
        "fase",
        "tipo_fase",
        "estadio",
        "arbitro",
        "publico",
        "publico_max",
        "time_mandante",
        "time_visitante",
        "tecnico_mandante",
        "tecnico_visitante",
        "valor_equipe_titular_mandante",
        "valor_equipe_titular_visitante",
        "idade_media_titular_mandante",
        "idade_media_titular_visitante",
        "gols_mandante",
        "gols_visitante",
        "gols_1_tempo_mandante",
        "gols_1_tempo_visitante",
        "penalti",
        "gols_penalti_mandante",
        "gols_penalti_visitante",
        "escanteios_mandante",
        "escanteios_visitante",
        "faltas_mandante",
        "faltas_visitante",
        "chutes_bola_parada_mandante",
        "chutes_bola_parada_visitante",
        "defesas_mandante",
        "defesas_visitante",
        "impedimentos_mandante",
        "impedimentos_visitante",
        "chutes_mandante",
        "chutes_visitante",
        "chutes_fora_mandante",
        "chutes_fora_visitante"
    ]
}

# Criar um Enum com todas as colunas
AllColumnsEnum = Enum(
    'AllColumnsEnum',
    {col: col for cols in COLUNAS_COMPETICOES.values() for col in cols}
)
