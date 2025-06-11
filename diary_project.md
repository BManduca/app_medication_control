# Anotações

- Estrutura:
  1. criação do db em **init**.py
  2. definição das Class User, medication... em models.py
  3. Importação models para que o Flask-Migrate veja os models em **init**.py
     <br/><br/>
     ![](./diary_assets/definition_class_User_and_import_models_FlaskMigrate.png)

## Configurando TailwindCSS para o projeto

1. Inicializar o Node.js no projeto

```
npm init -y
```

2. Instale o Tailwind e dependências

```
npm install -D tailwindcss@3 postcss auto-prefixer
npx tailwindcss init
```

3. Crie a estrutura do diretório(como preferir):

```
mkdir -p app/static/css
touch app/static/css/tailwind.css
```

4. Edite o arquivo tailwind.config.js

```
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

5. Edite app/static/css/tailwind.css

```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

6. Crie ou edite o arquivo postcss.config.js

```
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

7. Compilar o Tailwind

```
npx tailwindcss -i ./app/static/css/tailwind.css -o ./app/static/css/output.css --watch
```

## Gerando e Aplicando script de migração

1. Definindo FLASK_APP

```
export FLASK_APP=run.py
```

2. Inicializando o banco

```
flask db init
```

3. Gerando script de migração

```
flask db migrate -m "Aplicar sua mensagem aqui"
```

4. Aplicar a migração ao banco de dados

```
flask db upgrade
```

## Etapa de testes

### 📁 1️⃣ Criação da Estrutura de Testes
* Criado a pasta de tests na raiz do projeto
```
mkdir tests
```

* Acessar a pasta tests e criar os arquivos iniciais:
```
touch tests/conftest.py tests/test_auth.py tests/test_medications.py tests/test_models.py
```

### 🔧 2️⃣ Configuração de Fixtures Globais (conftest.py)
* No arquivo tests/conftest.py, foi criado:
  * Um app de teste do Flask
  * Um banco de dados temporário (SQLite em memória)
  * Uma fisture de cliete de teste (Flask test client)

  * **Obs.:** É necessário atualizar o arquivo __init__.py
  ```
    from datetime import datetime, timezone
    import os
    from dotenv import load_dotenv
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_login import LoginManager
    from config import DevConfig, ProdConfig

    load_dotenv()

    # criando instancias "vazias" para o banco de dados, migração e autenticação
    db = SQLAlchemy()
    migrate = Migrate()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Redirecionamento se não estiver logado
    login_manager.login_message = 'Você precisa estar logado para acessar esta página!'
    login_manager.login_message_category = 'warning' # categoria do flash

    # função é responsável por criar e configurar a aplicação Flask, com banco de dados, 
    # autenticação, rotas e configurações gerais
    def create_app(testing=False):
        app = Flask(__name__)

        # carregando configurações do arquivo config.py | define se é dev ou prod
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'production':
            app.config.from_object(ProdConfig)
        else:
            app.config.from_object(DevConfig)

        # se testing=True, sobrescreve as configs para testes
        if testing:
            app.config.update({
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "WTF_CSRF_ENABLED": False,  # Desativa CSRF para testes
            })

        # Inicializa extensões com a aplicação
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)

        # carrega dos modelos definidos em app/models.py no momento em que o app é criado
        from app import models

        from app.routes.auth_routes import auth_bp
        from app.routes.dashboard_routes import dashboard_bp
        from app.routes.medication_routes import medication_bp
        from app.routes.main_routes import main

        app.register_blueprint(auth_bp) # Rotas de autenticação
        app.register_blueprint(dashboard_bp) # Rota protegia: /dashboard
        app.register_blueprint(medication_bp) # Rotas dos medicamentos
        app.register_blueprint(main) # Rota principal: /

        @app.context_processor
        def inject_now():
            return {'now': datetime.now(timezone.utc)}

        return app

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
  ```

### 🧪 3️⃣ Testes Básicos de Autenticação (test_auth.py)
  * Testes para login e logout
  
### 💊 4️⃣ Testes Básicos de CRUD de Medicamentos (test_medications.py)
  * Testes para acessar a página aonde lista os medicamentos
  * Teste para acessar a página para adicionar um medicamento
  * Teste para adicionar um medicamento

### 🧬 5️⃣ Testes Básicos de Modelos (test_models.py)
  * Necessário implementar a simulação da criação de usuário
  * Necessário implementar a simulação de login do usuário

### Criar o arquivo pytest.ini
  * para armazenar configurações para execução do teste.

### Para execução do teste
  * pyhton3 -m pytest



