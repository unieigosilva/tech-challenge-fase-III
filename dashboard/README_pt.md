
# Projeto Dashboard

## Visão Geral
Este projeto é uma aplicação de dashboard construída usando Python e Dash. Ele inclui diversos componentes para visualizar e prever dados relacionados ao campeonato Brasileirão. O projeto está organizado em diferentes módulos, incluindo processamento de dados, manipulação de modelos e a aplicação principal do dashboard.

## Estrutura do Projeto
Abaixo está uma visão geral da estrutura do projeto:

```
dashboard/
│
├── main.py                  # Arquivo principal para executar o dashboard
├── config.py                # Configurações do projeto
├── utils.py                 # Funções utilitárias para processamento de dados
├── __init__.py              # Arquivo de inicialização do pacote
├── requirements.txt         # Dependências Python do projeto
├── teste.ipynb              # Notebook Jupyter para testes e desenvolvimento
├── .env                     # Variáveis de ambiente
├── .gitignore               # Arquivo Git ignore
│
├── dash_app/                # Diretório contendo a aplicação Dash
│   ├── app.py               # Definição principal da aplicação Dash
│   ├── callbacks.py         # Callbacks para interatividade dinâmica
│   ├── componentes.py       # Componentes personalizados para o dashboard
│   ├── layout.py            # Estrutura de layout do dashboard
│   ├── __init__.py          # Arquivo de inicialização do módulo Dash
│   └── assets/
│       └── custom_style.css # CSS personalizado para o estilo do dashboard
│
├── data/                    # Diretório contendo os conjuntos de dados
│   ├── brasileirao.xlsx             # Dados do campeonato Brasileirão
│   ├── dados_normalizados.xlsx      # Dados normalizados para análise
│   └── tabela_times.xlsx            # Tabela de informações dos times
│
└── model/                   # Diretório contendo o modelo treinado e dados relacionados
    ├── modelo.pkl                      # Modelo de machine learning treinado
    └── mundo_transfermarkt_competicoes_brasileirao_serie_a.csv # Conjunto de dados adicional para previsões do modelo
```

## Começando

### Pré-requisitos
Para executar este projeto, é necessário ter o Python instalado juntamente com as seguintes dependências, que podem ser instaladas através do `requirements.txt`:

```sh
pip install -r requirements.txt
```

Certifique-se de configurar as variáveis de ambiente no arquivo `.env` conforme necessário.

### Executando o Dashboard
Para executar a aplicação do dashboard, execute o seguinte comando:

```sh
python main.py
```

Isso iniciará um servidor local onde você poderá visualizar e interagir com o dashboard em seu navegador.

## Dados
Os dados utilizados neste projeto incluem informações históricas sobre o campeonato Brasileirão, detalhes dos times e conjuntos de dados normalizados para análise. Estes arquivos estão localizados no diretório `data/` e são usados tanto para visualização quanto para previsões do modelo.

## Modelo
O modelo treinado (`modelo.pkl`) é utilizado para prever resultados relacionados ao campeonato Brasileirão. Ele está armazenado no diretório `model/`, juntamente com dados adicionais de suporte.

## Desenvolvimento
O projeto inclui um notebook Jupyter (`teste.ipynb`) para testes e prototipagem. Isto pode ser útil para experimentar novos recursos ou analisar dados antes de integrá-los ao dashboard principal.

## Estilo
A aparência visual do dashboard pode ser personalizada através do arquivo CSS localizado em `dash_app/assets/custom_style.css`.

## Licença
Este projeto é licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Agradecimentos
- Os dados utilizados neste projeto são provenientes de informações publicamente disponíveis sobre o campeonato Brasileirão.
- Agradecimentos especiais aos contribuidores e à comunidade de código aberto pelo suporte.

