🔧 Stack Tecnológica

Back-end
• Python 3.x
• Flask (framework web)
• Flask-SQLAlchemy (ORM para banco de dados)
• Flask-Migrate (migrações de banco de dados)
• Flask-Login (autenticação)
• Flask-WTF (validação de formulários)

Front-end
• HTML5, Jinja2 (templating engine do Flask)
• Tailwind CSS (estilização moderna)
• Alpine.js (opcional para interatividade leve)

Banco de Dados
• SQLite (local e simples) ou PostgreSQL (produção)

Extras
• Docker (opcional para deploy)
• Gunicorn + Nginx (produção)
• pytest ou unittest (testes)

⸻

🧱 Etapas do Projeto

⸻

🟩 Etapa 1: Configuração Inicial do Projeto
• Estrutura básica do projeto Flask
• Criação de ambiente virtual
• Instalação das dependências principais
• Arquitetura de pastas (MVC)

⸻

🟨 Etapa 2: Modelagem do Banco de Dados
• Modelo User com autenticação
• Modelo Medicamento
• Nome
• Dosagem
• Frequência
• Horário
• Data de início e fim
• Modelo Registro para controle de uso

⸻

🟦 Etapa 3: Sistema de Autenticação
• Tela de login, logout, registro
• Proteção de rotas
• Hash de senha
⸻

🟧 Etapa 4: CRUD de Medicamentos
• Listagem
• Adição
• Edição
• Remoção
• Formulários com Flask-WTF

⸻

🟫 Etapa 5: Lembretes e Controle de Uso
• Registrar uso do medicamento
• Histórico de tomadas
• Filtros por período

⸻

🟥 Etapa 6: Layout com Tailwind CSS
• Aplicação de layout responsivo
• Componentes reutilizáveis (cards, navbar, forms)
• Estética clean

⸻

🟪 Etapa 7: Testes e Validação
• Testes unitários de rotas e modelos
• Validação de formulários
• Proteção contra erros comuns

⸻

🟨 Etapa 8: Deploy
• Dockerização do app
• Deploy no Render, Railway ou VPS (com Gunicorn + Nginx)

⸻

Extra: 🌟 Branding e Identidade Visual — Bônus em andamento
	•	✅ Logo personalizada criada (SVG + PNG)
	•	✅ Ilustrações aplicadas no home.html
	•	🔜 favicon.ico, e talvez página sobre/contato para SEO


progresso de revisão: 

- app/templates/partials => _buttons.html, _flash_messages.html, _form_field.html
- app/templates => base.html, dashboard.html, home.html
- app => forms.py

---

etapa de tests

🧪 1️⃣ Testes Unitários de Rotas e Modelos

Começaremos a criar um conjunto básico de testes para:
	•	Autenticação (login, logout, registro)
	•	CRUD de medicamentos
	•	Modelos principais (User, Medication, MedicationRegister)

👉 Ferramenta recomendada: pytest com Flask
👉 Estrutura típica:
```
/tests
  test_auth.py
  test_medications.py
  test_models.py
```

📦 Primeiros passos:
	•	Crie um diretório chamado tests no seu projeto.
	•	Adicione um arquivo conftest.py para fixtures globais.
	•	Crie testes simples de 200 OK e redirecionamentos para as rotas principais.
	•	Crie testes básicos de criação e leitura dos modelos.


✍️ 2️⃣ Validação de Formulários

Já usamos o Flask-WTF para os formulários! Agora vamos revisar:
	•	Verificar se campos obrigatórios estão sendo validados (já temos!)
	•	Adicionar feedback visual no formulário em caso de erro (mensagens de erro abaixo do campo)
	•	Verificar campos como:
	•	Nome do medicamento (não pode ser vazio!)
	•	Dosagem (obrigatório!)
	•	Frequência (opcional ou obrigatório?)
	•	Datas coerentes (data de início não pode ser depois da data de fim)

🛡️ 3️⃣ Proteção contra Erros Comuns

Alguns pontos essenciais:

✅ Uso de CSRF nos formulários ({{ form.hidden_tag() }} já está incluído no Flask-WTF).
✅ Proteger rotas sensíveis (já feito com @login_required).
✅ Mensagens de erro claras no login e registro (ex.: “Usuário ou senha incorretos”).
✅ Redirecionamentos adequados para evitar acesso não autorizado.


---


### Etapa de testes

🪛 1️⃣ Executar os testes para ver se está tudo funcionando

No terminal, no diretório raiz do projeto, execute:
```
python3 -m pytest
```

•	Isso vai rodar todos os testes encontrados em tests/.
•	Se aparecerem erros ou falhas, é hora de corrigir ou ajustar o que for necessário!

🏗️ 2️⃣ Ampliar a cobertura dos testes

Agora que temos as “bases” testadas, podemos:

✅ Testar casos de sucesso e falha.
✅ Testar validações de formulários (ex.: campos obrigatórios, limites de tamanho).
✅ Testar fluxos de autenticação protegidos (login obrigatório, redirecionamentos).
✅ Testar permissões (ex.: um usuário tentando acessar dados de outro).

💡 Exemplos para expandir:
	•	Testar o login com senha errada.
	•	Testar o cadastro de medicamentos sem campos obrigatórios (esperar erro!).
	•	Testar tentativa de acessar /dashboard sem login (esperar redirecionamento!).
	•	Testar limite de tamanho (name muito longo, por exemplo).

⸻

🔒 3️⃣ Proteção contra erros comuns

Inclua testes que forcem:
	•	Falhas de banco (ex.: violação de chave estrangeira).
	•	Falhas de formulário (ex.: dados inválidos).
	•	Falhas de autenticação (login obrigatório).

Isso garante robustez ao seu app!

⸻

🧪 4️⃣ Rodar os testes sempre!
	•	Antes de subir para produção.
	•	Antes de cada mudança grande no código.
	•	Se usar git, configure um hook (pre-push) para rodar pytest automaticamente!

⸻

🚀 5️⃣ Avançar para deploy e monitoração

Com tudo testado e validado, podemos:
	•	Deploy (hospedar em um serviço como Railway, Render, etc.).
	•	Incluir logs no app para monitorar erros em produção.
	•	Adotar ferramentas de CI/CD (ex.: GitHub Actions para rodar testes automaticamente em push/pull request).

---

🚀 Passo 1: Repositório GitHub

✅ Tenha o seu projeto em um repositório GitHub (público ou privado).
✅ O Render se conecta direto ao GitHub para deploys automáticos.

⸻

🚀 Passo 2: Prepare o seu projeto
1.	requirements.txt atualizado
•	Gere ou atualize:
	```
	pip freeze > requirements.txt
	```
	•	Confirme que todas as dependências estão listadas.

2.	Procfile (opcional, mas ajuda)
•	Render reconhece Procfile como no Heroku.
•	Crie um arquivo Procfile na raiz do projeto:
	```
	web: gunicorn app:app
	```
	(onde app é o nome do seu arquivo Python que cria a aplicação Flask, e app é a instância do Flask).

3.	Banco de dados (se necessário)
•	Se usar Postgres (ou outro), já configure a string de conexão no .env ou no Render.

⸻

🚀 Passo 3: Conta no Render
	1.	Acesse Render.com.
	2.	Crie uma conta ou faça login.

⸻

🚀 Passo 4: Crie o serviço web
	1.	No Dashboard do Render, clique em “New Web Service”.
	2.	Conecte o seu repositório GitHub e selecione o projeto.
	3.	Configure:
	•	Environment: Python 3.12 (ou a versão que você usa).
	•	Build Command: pip install -r requirements.txt
	•	Start Command: gunicorn app:app
(ajuste o caminho para o seu arquivo principal se necessário).
	•	Region: escolha a mais próxima de seus usuários.
	4.	Adicione as variáveis de ambiente necessárias (como DATABASE_URL, FLASK_ENV=production, etc.) na aba Environment.

⸻

🚀 Passo 5: Deploy automático e monitoramento
	•	O Render vai fazer o deploy automaticamente.
	•	Cada push no GitHub dispara um deploy novo.
	•	O painel do Render mostra logs em tempo real (para debug).
	•	É possível escalar o serviço (RAM/CPU) com 1 clique.

⸻

🚀 Banco de dados no Render

Se você usar Postgres (por exemplo), Render já fornece um serviço de banco de dados gerenciado:

✅ Vá em “Databases” > “New Database” e crie um novo banco.
✅ Pegue a string de conexão e configure no .env ou nas variáveis do serviço.

⸻

🚀 Checklist final de produção

✅ Use FLASK_ENV=production ou DEBUG=0.
✅ Use um servidor WSGI como gunicorn (não o Flask dev server).
✅ Configure variáveis secretas (SECRET_KEY, etc.).
✅ Verifique CORS e HTTPS.