# Usa uma imagem oficial do Python
FROM python:3.11-slim

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos para o container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "main.py"]
