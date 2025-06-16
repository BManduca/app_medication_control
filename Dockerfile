# Imagem oficial do Python como base
FROM python:3.12-slim

# definindo diretório de trabalho dentro do container
WORKDIR /app

# Ação de copiar o requirements.txt e instalar as dependências
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt --root-user-action=ignore

# Copiar todo o projeto para o container
COPY . .

# Evidenciando/Expondo a porta que o Flask vai executar
EXPOSE 5000

# criando variável de ambiente para evidenciar que a app esta em prod
ENV FLASK_ENV=production

# comando para rodar a app em Gunicorn (mais robusto que flask run)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "wsgi:app"]