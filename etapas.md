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
Se quiser, posso gerar os arquivos register_medication.html e view_history.html também. Deseja seguir com essas telas?
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
