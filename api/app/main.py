from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from typing import List, Optional
from datetime import datetime
import pandas as pd
import boto3

# Importar as configurações
from app.config import CompeticaoEnum, CSV_FILES, COLUNAS_COMPETICOES

app = FastAPI(
    title="API de Dados de Futebol",
    description="API para coleta e manipulação de dados de competições de futebol: Brasileirão Série A e Copa do Brasil.",
    version="1.0.0"
)

# Função para carregar os dados a partir de arquivos CSV locais
def carregar_dados(competicao: CompeticaoEnum):
    if competicao not in CSV_FILES:
        raise HTTPException(status_code=400, detail="Competição não reconhecida.")
    csv_path = CSV_FILES[competicao]
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Arquivo CSV não encontrado para a competição '{competicao}'.")
    return df

# Função para filtrar dados
def filtrar_dados(df, params):
    # Remover colunas
    if params.colunas_drop:
        df = df.drop(columns=params.colunas_drop, errors='ignore')

    # Filtrar por valores específicos
    if params.estadio:
        df = df[df['estadio'] == params.estadio]

    if params.time_mandante:
        df = df[df['time_mandante'] == params.time_mandante]

    if params.time_visitante:
        df = df[df['time_visitante'] == params.time_visitante]

    # Filtrar por datas
    if params.data_inicio or params.data_fim:
        if 'data' not in df.columns:
            raise HTTPException(status_code=400, detail="Coluna 'data' não encontrada.")

        if 'horario' in df.columns:
            df['data_hora'] = pd.to_datetime(df['data'] + ' ' + df['horario'], errors='coerce', dayfirst=True)
        else:
            df['data_hora'] = pd.to_datetime(df['data'], errors='coerce', dayfirst=True)

        if params.data_inicio:
            df = df[df['data_hora'] >= params.data_inicio]

        if params.data_fim:
            df = df[df['data_hora'] <= params.data_fim]

    return df

# Função para converter datas
def converter_data(data_str):
    try:
        if len(data_str) == 4:
            return datetime.strptime(data_str, '%Y')
        elif len(data_str) == 6:
            return datetime.strptime(data_str, '%m%Y')
        elif len(data_str) == 8:
            return datetime.strptime(data_str, '%d%m%Y')
        else:
            return datetime.strptime(data_str, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Formato de data inválido: '{data_str}'.")

# Modelos Pydantic
class FilterParams(BaseModel):
    competicao: CompeticaoEnum = Field(..., description="Escolha a competição.")
    colunas_drop: Optional[List[str]] = Field(None, description="Colunas a serem removidas.")
    data_inicio: Optional[datetime] = Field(None, description="Data inicial.")
    data_fim: Optional[datetime] = Field(None, description="Data final.")
    estadio: Optional[str] = Field(None, description="Estádio.")
    time_mandante: Optional[str] = Field(None, description="Time mandante.")
    time_visitante: Optional[str] = Field(None, description="Time visitante.")

    @field_validator('data_inicio', 'data_fim', mode='before')
    def parse_data(cls, v):
        if v is None:
            return None
        return converter_data(v)

    @field_validator('colunas_drop')
    def validar_colunas_drop(cls, v, info: FieldValidationInfo):
        if v is None:
            return None
        competicao = info.data.get('competicao')
        if not competicao:
            raise ValueError("O campo 'competicao' é obrigatório.")
        colunas_validas = COLUNAS_COMPETICOES[competicao]
        colunas_invalidas = [col for col in v if col not in colunas_validas]
        if colunas_invalidas:
            raise ValueError(f"Colunas inválidas para '{competicao}': {colunas_invalidas}")
        return v

    @field_validator('estadio', 'time_mandante', 'time_visitante')
    def validar_coluna_existente(cls, v, info: FieldValidationInfo):
        if v is None:
            return None
        field_name = info.field_name
        competicao = info.data.get('competicao')
        if not competicao:
            raise ValueError("O campo 'competicao' é obrigatório.")
        if field_name not in COLUNAS_COMPETICOES[competicao]:
            raise ValueError(f"A coluna '{field_name}' não existe para '{competicao}'.")
        return v

class S3Params(BaseModel):
    competicao: CompeticaoEnum = Field(..., description="Escolha a competição.")
    bucket_name: str = Field(..., description="Nome do bucket S3.")

# Dependência para extrair parâmetros
def get_filter_params(
    request: Request,
    competicao: CompeticaoEnum = Query(...),
    colunas_drop: Optional[List[str]] = Query(None),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
    estadio: Optional[str] = Query(None),
    time_mandante: Optional[str] = Query(None),
    time_visitante: Optional[str] = Query(None)
) -> FilterParams:
    params = FilterParams(
        competicao=competicao,
        colunas_drop=colunas_drop,
        data_inicio=data_inicio,
        data_fim=data_fim,
        estadio=estadio,
        time_mandante=time_mandante,
        time_visitante=time_visitante
    )
    return params

# Endpoint para gerar CSV filtrado
@app.post("/gerar-csv", summary="Gerar CSV Filtrado")
def gerar_csv(params: FilterParams):
    df = carregar_dados(params.competicao)
    df_filtrado = filtrar_dados(df, params)
    file_path = f"app/dados_tratados_{params.competicao}.csv"
    df_filtrado.to_csv(file_path, index=False)
    return {"message": f"CSV gerado para {params.competicao}!", "file_path": file_path}

# Endpoint para obter dados filtrados
@app.get("/dados-filtrados{ext}", summary="Obter Dados Filtrados")
def dados_filtrados(
    ext: str = '',
    params: FilterParams = Depends(get_filter_params)
):
    df = carregar_dados(params.competicao)
    df_filtrado = filtrar_dados(df, params)
    csv_data = df_filtrado.to_csv(index=False)

    if ext == '.csv':
        filename = f'dados_filtrados_{params.competicao}.csv'
        return Response(
            content=csv_data,
            media_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    else:
        return Response(content=csv_data, media_type='text/plain')

# Endpoint para enviar o CSV para S3
@app.post("/enviar-bucket", summary="Enviar CSV para Bucket S3")
def enviar_bucket(params: S3Params):
    file_path = f"app/dados_tratados_{params.competicao}.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV não encontrado.")
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, params.bucket_name, f"{params.competicao}_dados_tratados.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar para o bucket: {e}")
    return {"message": f"Arquivo enviado para o bucket {params.bucket_name}!"}

# Endpoint para listar colunas disponíveis
@app.get("/colunas-disponiveis", summary="Listar Colunas Disponíveis")
def colunas_disponiveis(
    competicao: CompeticaoEnum = Query(...)
):
    colunas = COLUNAS_COMPETICOES.get(competicao)
    if not colunas:
        raise HTTPException(status_code=404, detail="Colunas não encontradas.")
    return {"competicao": competicao, "colunas_disponiveis": colunas}
