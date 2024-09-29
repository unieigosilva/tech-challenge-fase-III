# Manual de Utilização da API de Dados de Futebol

Este manual fornece instruções detalhadas sobre como configurar, executar e utilizar a API de Dados de Futebol, que permite a coleta e manipulação de dados das competições Brasileirão Série A e Copa do Brasil.

## Sumário

- [Manual de Utilização da API de Dados de Futebol](#manual-de-utilização-da-api-de-dados-de-futebol)
  - [Sumário](#sumário)
  - [Visão Geral](#visão-geral)
  - [Pré-requisitos](#pré-requisitos)
  - [Configuração do Ambiente](#configuração-do-ambiente)
    - [1. Clone o Repositório (opcional)](#1-clone-o-repositório-opcional)
    - [2. Crie um Ambiente Virtual](#2-crie-um-ambiente-virtual)
    - [3. Instale as Dependências](#3-instale-as-dependências)
    - [4. Estrutura de Arquivos](#4-estrutura-de-arquivos)
    - [5. Configuração das Credenciais AWS (Opcional)](#5-configuração-das-credenciais-aws-opcional)
  - [Execução da Aplicação](#execução-da-aplicação)
  - [Endpoints Disponíveis](#endpoints-disponíveis)
    - [1. Gerar CSV Filtrado (`/gerar-csv`)](#1-gerar-csv-filtrado-gerar-csv)
    - [2. Obter Dados Filtrados (`/dados-filtrados` e `/dados-filtrados.csv`)](#2-obter-dados-filtrados-dados-filtrados-e-dados-filtradoscsv)
    - [3. Enviar CSV para Bucket S3 (`/enviar-bucket`)](#3-enviar-csv-para-bucket-s3-enviar-bucket)
    - [4. Listar Colunas Disponíveis (`/colunas-disponiveis`)](#4-listar-colunas-disponíveis-colunas-disponiveis)
  - [Utilização do Swagger UI](#utilização-do-swagger-ui)
  - [Exemplos de Requisições](#exemplos-de-requisições)
    - [1. Gerar um CSV Filtrado para o Brasileirão](#1-gerar-um-csv-filtrado-para-o-brasileirão)
    - [2. Obter Dados Filtrados como Texto CSV](#2-obter-dados-filtrados-como-texto-csv)
    - [3. Baixar Dados Filtrados como Arquivo CSV](#3-baixar-dados-filtrados-como-arquivo-csv)
    - [4. Enviar o CSV para um Bucket S3](#4-enviar-o-csv-para-um-bucket-s3)
    - [5. Listar Colunas Disponíveis para a Copa do Brasil](#5-listar-colunas-disponíveis-para-a-copa-do-brasil)
  - [Considerações Finais](#considerações-finais)

---

## Visão Geral

A API de Dados de Futebol é uma aplicação desenvolvida em Python utilizando o framework FastAPI. Ela permite aos usuários:

- Carregar dados das competições Brasileirão Série A e Copa do Brasil a partir de arquivos CSV.
- Filtrar e manipular os dados com base em diversos parâmetros, como datas, times e estádios.
- Gerar arquivos CSV filtrados e disponibilizá-los para download ou enviar para um bucket AWS S3.
- Listar as colunas disponíveis para cada competição.

---

## Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado em seu ambiente:

- Python 3.8 ou superior.
- Pip (gerenciador de pacotes do Python).
- Git (opcional, para clonar o repositório).
- Credenciais válidas da AWS configuradas, caso deseje utilizar o recurso de upload para o S3.

---

## Configuração do Ambiente

### 1. Clone o Repositório (opcional)

Se o código estiver em um repositório Git, clone-o:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie um Ambiente Virtual

Crie um ambiente virtual para isolar as dependências:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- No Windows:

  ```bash
  venv\Scripts\activate
  ```

- No Linux/macOS:

  ```bash
  source venv/bin/activate
  ```

### 3. Instale as Dependências

Instale as bibliotecas necessárias:

```bash
pip install fastapi uvicorn pandas boto3
```

### 4. Estrutura de Arquivos

Certifique-se de que a estrutura de arquivos esteja conforme abaixo:

```
projeto/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── mundo_transfermarkt_competicoes_brasileirao_serie_a.csv
│   └── mundo_transfermarkt_competicoes_copa_brasil.csv
├── venv/
└── (outros arquivos)
```

- `main.py`: Código principal da aplicação.
- `config.py`: Configurações e constantes utilizadas na aplicação.
- `__init__.py`: Arquivo vazio que transforma o diretório `app` em um pacote Python.
- CSVs: Arquivos de dados das competições.

### 5. Configuração das Credenciais AWS (Opcional)

Para utilizar o endpoint de envio para o S3, configure suas credenciais AWS:

- Configure as variáveis de ambiente `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`.
- Ou configure o arquivo `~/.aws/credentials`.

---

## Execução da Aplicação

Execute a aplicação utilizando o Uvicorn:

```bash
uvicorn app.main:app --reload
```

- A opção `--reload` faz com que a aplicação seja recarregada automaticamente ao detectar mudanças no código.
- A aplicação estará disponível em `http://127.0.0.1:8000`.

---

## Endpoints Disponíveis

### 1. Gerar CSV Filtrado (`/gerar-csv`)

- **Método:** `POST`
- **Descrição:** Gera um arquivo CSV filtrado com base nos parâmetros fornecidos.
- **Parâmetros no Corpo da Requisição (JSON):**

  | Parâmetro       | Tipo             | Obrigatório | Descrição                                                  |
  |-----------------|------------------|-------------|------------------------------------------------------------|
  | `competicao`    | `string`         | Sim         | Competição (`brasileirao` ou `copa_brasil`).               |
  | `colunas_drop`  | `array[string]`  | Não         | Lista de colunas a serem removidas.                        |
  | `data_inicio`   | `string`         | Não         | Data inicial (`AAAA`, `MMAAAA`, `DDMMAAAA`).               |
  | `data_fim`      | `string`         | Não         | Data final (`AAAA`, `MMAAAA`, `DDMMAAAA`).                 |
  | `estadio`       | `string`         | Não         | Filtrar por estádio específico.                            |
  | `time_mandante` | `string`         | Não         | Filtrar por time mandante específico.                      |
  | `time_visitante`| `string`         | Não         | Filtrar por time visitante específico.                     |

- **Resposta:**

  ```json
  {
    "message": "CSV gerado para brasileirao!",
    "file_path": "app/dados_tratados_brasileirao.csv"
  }
  ```

### 2. Obter Dados Filtrados (`/dados-filtrados` e `/dados-filtrados.csv`)

- **Método:** `GET`
- **Descrição:** Retorna os dados filtrados em formato CSV como texto ou como arquivo para download.
- **URLs:**
  - `/dados-filtrados`: Retorna o CSV como texto.
  - `/dados-filtrados.csv`: Força o download do CSV como arquivo.
- **Parâmetros de Consulta:**

  Os mesmos parâmetros do endpoint `/gerar-csv`, mas passados como query parameters na URL.

- **Exemplo:**

  ```
  GET /dados-filtrados.csv?competicao=brasileirao&data_inicio=042004&data_fim=082004&estadio=Maracanã
  ```

- **Resposta:**

  - Como arquivo CSV para download ou texto CSV na resposta HTTP.

### 3. Enviar CSV para Bucket S3 (`/enviar-bucket`)

- **Método:** `POST`
- **Descrição:** Envia o arquivo CSV filtrado para o bucket S3 especificado.
- **Parâmetros no Corpo da Requisição (JSON):**

  | Parâmetro     | Tipo     | Obrigatório | Descrição                              |
  |---------------|----------|-------------|----------------------------------------|
  | `competicao`  | `string` | Sim         | Competição (`brasileirao` ou `copa_brasil`). |
  | `bucket_name` | `string` | Sim         | Nome do bucket S3 de destino.          |

- **Resposta:**

  ```json
  {
    "message": "Arquivo enviado para o bucket meu-bucket!"
  }
  ```

- **Observação:**
  - Antes de usar este endpoint, certifique-se de ter gerado o CSV utilizando o endpoint `/gerar-csv`.

### 4. Listar Colunas Disponíveis (`/colunas-disponiveis`)

- **Método:** `GET`
- **Descrição:** Retorna as colunas disponíveis para a competição selecionada.
- **Parâmetros de Consulta:**

  | Parâmetro    | Tipo     | Obrigatório | Descrição                              |
  |--------------|----------|-------------|----------------------------------------|
  | `competicao` | `string` | Sim         | Competição (`brasileirao` ou `copa_brasil`). |

- **Exemplo:**

  ```
  GET /colunas-disponiveis?competicao=brasileirao
  ```

- **Resposta:**

  ```json
  {
    "competicao": "brasileirao",
    "colunas_disponiveis": [
      "ano_campeonato",
      "data",
      "rodada",
      "estadio",
      "... (outras colunas)"
    ]
  }
  ```

---

## Utilização do Swagger UI

O Swagger UI é uma interface gráfica que permite testar e visualizar os endpoints da API de forma interativa.

- **Acesso:** `http://127.0.0.1:8000/docs`
- **Recursos:**
  - Visualizar a documentação de cada endpoint.
  - Testar requisições diretamente pelo navegador.
  - Visualizar os parâmetros e as respostas esperadas.

---

## Exemplos de Requisições

### 1. Gerar um CSV Filtrado para o Brasileirão

**Requisição:**

```bash
POST http://127.0.0.1:8000/gerar-csv
Content-Type: application/json

{
  "competicao": "brasileirao",
  "colunas_drop": ["arbitro", "publico"],
  "data_inicio": "2020",
  "data_fim": "2021",
  "estadio": "Maracanã",
  "time_mandante": "Flamengo",
  "time_visitante": "Vasco"
}
```

**Resposta:**

```json
{
  "message": "CSV gerado para brasileirao!",
  "file_path": "app/dados_tratados_brasileirao.csv"
}
```

### 2. Obter Dados Filtrados como Texto CSV

**Requisição:**

```bash
GET http://127.0.0.1:8000/dados-filtrados?competicao=brasileirao&data_inicio=2020&estadio=Maracanã
```

**Resposta:**

- Texto CSV com os dados filtrados.

### 3. Baixar Dados Filtrados como Arquivo CSV

**Requisição:**

```bash
GET http://127.0.0.1:8000/dados-filtrados.csv?competicao=brasileirao&data_inicio=2020&estadio=Maracanã
```

**Resposta:**

- Arquivo `dados_filtrados_brasileirao.csv` para download.

### 4. Enviar o CSV para um Bucket S3

**Requisição:**

```bash
POST http://127.0.0.1:8000/enviar-bucket
Content-Type: application/json

{
  "competicao": "brasileirao",
  "bucket_name": "meu-bucket"
}
```

**Resposta:**

```json
{
  "message": "Arquivo enviado para o bucket meu-bucket!"
}
```

### 5. Listar Colunas Disponíveis para a Copa do Brasil

**Requisição:**

```bash
GET http://127.0.0.1:8000/colunas-disponiveis?competicao=copa_brasil
```

**Resposta:**

```json
{
  "competicao": "copa_brasil",
  "colunas_disponiveis": [
    "ano_campeonato",
    "data",
    "horario",
    "fase",
    "... (outras colunas)"
  ]
}
```

---

## Considerações Finais

- **Formatos de Data Aceitos:**
  - `AAAA` (por exemplo, `2020`)
  - `MMAAAA` (por exemplo, `042020` para abril de 2020)
  - `DDMMAAAA` (por exemplo, `01042020` para 1º de abril de 2020)

- **Filtragem por Colunas:**
  - Utilize o endpoint `/colunas-disponiveis` para verificar as colunas disponíveis antes de fazer requisições que envolvam remoção de colunas (`colunas_drop`).

- **Filtragem por Valores Específicos:**
  - Para `estadio`, `time_mandante` e `time_visitante`, certifique-se de que os valores fornecidos correspondem exatamente aos presentes nos dados (case-sensitive).

- **Envio para o S3:**
  - Certifique-se de que suas credenciais AWS estão corretamente configuradas e que você tem permissão para escrever no bucket especificado.
  - O arquivo enviado terá o nome `{competicao}_dados_tratados.csv`.

- **Segurança:**
  - Esta API não implementa autenticação ou autorização. Se for expô-la publicamente, considere implementar medidas de segurança adequadas.

- **Logs e Monitoramento:**
  - Para ambientes de produção, é recomendável configurar logs e monitoramento para acompanhar o desempenho e possíveis erros da aplicação.

---

$$