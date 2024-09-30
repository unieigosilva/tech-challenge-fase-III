# Use uma imagem oficial do Python como base
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY . /app

# Instale as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r Docker/requirements.txt

# Exponha a porta 8000 para acessar a API
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
