from fastapi import FastAPI, Query, HTTPException
import pandas as pd
from io import BytesIO
import boto3
import os

app = FastAPI()

# Caminhos para os arquivos CSV locais
BRASILEIRAO_PATH = 'app/mundo_transfermarkt_competicoes_brasileirao_serie_a.csv'
COPA_BRASIL_PATH = 'app/mundo_transfermarkt_competicoes_copa_brasil.csv'

# Função para carregar os dados a partir de arquivos CSV locais
def carregar_dados(competicao):
    if competicao == "brasileirao":
        return pd.read_csv(BRASILEIRAO_PATH)
    elif competicao == "copa_brasil":
        return pd.read_csv(COPA_BRASIL_PATH)
    else:
        raise HTTPException(status_code=400, detail="Competição não reconhecida. Escolha 'brasileirao' ou 'copa_brasil'.")

# Função para filtrar dados por colunas e datas
def filtrar_dados(df, colunas_drop=None, data_inicio=None, data_fim=None):
    # Filtrar por datas, se fornecido
    if data_inicio and data_fim:
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        df = df[(df['data'] >= pd.to_datetime(data_inicio)) & (df['data'] <= pd.to_datetime(data_fim))]

    # Remover colunas, se fornecido
    if colunas_drop:
        df = df.drop(columns=colunas_drop, errors='ignore')

    return df

# Endpoint para gerar CSV filtrado
@app.post("/gerar-csv")
def gerar_csv(competicao: str, colunas_drop: list = Query(None), data_inicio: str = None, data_fim: str = None):
    df = carregar_dados(competicao)

    # Filtrar os dados
    df_filtrado = filtrar_dados(df, colunas_drop, data_inicio, data_fim)

    # Salvar como CSV
    file_path = f"app/dados_tratados_{competicao}.csv"
    df_filtrado.to_csv(file_path, index=False)
    
    return {"message": f"CSV gerado com sucesso para {competicao}!", "file_path": file_path}

# Endpoint para baixar o CSV gerado
@app.get("/download-csv")
def download_csv(competicao: str):
    file_path = f"app/dados_tratados_{competicao}.csv"
    
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado. Gere o CSV primeiro.")

# Endpoint para enviar o CSV para S3
@app.post("/enviar-bucket")
def enviar_bucket(competicao: str, bucket_name: str):
    file_path = f"app/dados_tratados_{competicao}.csv"
    
    try:
        s3_client = boto3.client('s3')
        with open(file_path, "rb") as file:
            s3_client.upload_fileobj(file, bucket_name, f"{competicao}_dados_tratados.csv")
        return {"message": f"Arquivo enviado com sucesso para o bucket {bucket_name}!"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado. Gere o CSV primeiro.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar o arquivo para o bucket: {e}")

# Endpoint para retornar dados filtrados diretamente via GET
@app.get("/dados-filtrados")
def dados_filtrados(competicao: str, colunas_drop: list = Query(None), data_inicio: str = None, data_fim: str = None):
    df = carregar_dados(competicao)

    # Filtrar os dados
    df_filtrado = filtrar_dados(df, colunas_drop, data_inicio, data_fim)

    # Retornar os dados como JSON
    return df_filtrado.to_dict(orient="records")
