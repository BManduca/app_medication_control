# Deploy de Flask com banco PostgreSQL no Render

## ✅ 1. Requisitos do projeto

- Seu projeto já deve conter
  - run.py
  - app/ com **init**.py, models, etc.
  - config.py com as classes DevConfig e ProdConfig
  - .env (usado localmente, não será enviado para o Render)
  - requirements.txt
  - Procfile com:
    - web: gunicorn run:app

## ✅ 2. Subir o projeto no GitHub

- Certifique-se de que seu projeto está versionado com o Git e está em um repositório no Github

## ✅ 3. Criar o serviço no Render

1. Acessar: https://render.com
2. Clique em "New Web Service"
3. Escolha seu repositório no Github
4. Configure:

- Name: nome do seu app
- Runtime: Python
- Build Command: deixe em branco ou use:
  - pip install -r requirements.txt
- Start Command:
  - gunicorn run:app
- Environment: Python 3.11(ou versão que foi utilizada no projeto)

## ✅ 4. Criar um banco PostgreSQL no Render

1. Vá para o dashboard do Render
2. Clique em "New PostfreSQL"
3. Dê um nome, crie o banco
4. Copie a Database URL (será algo como):
   1. postgres://usuario:senha@host:5432/nomedobanco

## ✅ 5. Configurar variáveis de ambiente

- No painel da sua Web App:
  1. Vá em "Environment" > "Add Environment Variable"
  2. Adicione:
     |Key|Value|
     |---|---|
     |FLASK_ENV|production|
     |DATABASE_URL|cole aqui a URL do banco PostgreSQL gerado pelo Render|
     |SECRET_KEY|uma chave secreta segura(Pode ser gerado com o Python, se quiser)|

## ✅ 6. Habilitar deploy automático (opcional)

- Você pode ativar o "Auto Deploy" para que o Render atualize automaticamente quando fizer push no Github

## ✅ 7. Rodar as migrações no Render

- Você pode rodar os comandos de migração via SSH ou por Jobs no Render:

  - Opção 1: Acesse o shell (via deploy shell ou script temporário)

  ```
    flask db upgrade
  ```

  - Opção 2: Adicione temporariamente um script Python chamando migrate.py com:

  ```
    from app import create_app, db
    from flask_migrate import upgrade

    app = create_app()
    with app.app_context():
        upgrade()
  ```

  ***

  - 🧪 Como usar:
    1. Faça um push do arquivo migrate.py para o Github
    2. No render, vá na sua Web Service > "Manual Deploy" > "Add Job"
    3. Crie um Job com este comando:
       ```
        python migrate.py
       ```
    4. Rode o Job. O Render vai iniciar sua app, rodar as migrações e criar as tabelas
    5. Verifique no painel do PostgreSQL do Render que as tabelas foram criadas
    6. Depois que tudo estiver certo, o arquivo pode ser apagado
       1. Acessar o respositorio na sua maquina
       2. Excluir o arquivo
       3. Subir as alterações para o Github
       ```
        git rm migrate.py
        git commit -m "remove migrate script"
        git push origin main
       ```
