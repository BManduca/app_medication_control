# Projeto - Aplicação Web para Gerenciamento de Medicamento 💊

- Sistema Web para gerenciar medicamentos de forma simples e segura, com login de usuários, cadastro, edição e exclusão de registros.

---

## 🚀 Tecnologias Utilizadas

### 🧠 Back-end

- **Python** - Linguagem principal
- **Flask** - Microframework web
- **Flask-Login** - Autenticação de usuários
- **Flask-WTF** - Formulários com validação
- **Flask-BCrypt** - Criptografia de senhas
- **Flask-SQLAlchemy** - ORM para banco de dados
- **WTForms** - Formulários e validação
- **python-dotenv** – Variáveis de ambiente (.env)

### 💾 Banco de Dados

- **SQLite** – Banco leve e embutido (pode ser substituído por outros via SQLAlchemy)

### 🎨 Front-end

- **HTML + Jinja2** - Templates dinâmicos
- **Tailwind CSS** - Estilização moderna, responsiva e com componentes reutilizáveis
- **Lucide Icons** – Ícones elegantes para UI

### 🛠️ Ferramentas de Suporte

- **Git + GitHub** – Versionamento e colaboração
- **Docker** – Containerização da aplicação
- **Render** – Deploy com Gunicorn + Nginx
- **requirements.txt** - Lista de dependências
- **venv** / **.env.dev / .env.prod** – Configurações seguras

## 🧪 Funcionalidades

- ✅ **Cadastro e login de usuários** (tradicional e Google OAuth)
- ✅ **Criptografia de senhas** com Bcrypt
- ✅ **Cadastro, edição, exclusão e listagem de medicamentos**
- ✅ **Sistema de lembretes de medicamentos por horário e frequência**
- ✅ **Histórico de uso com filtros por período**
- ✅ **Exportação de histórico (CSV)**
- ✅ **Validações e mensagens de erro personalizadas**
- ✅ **Layout moderno e responsivo (Tailwind CSS)**
- ✅ **Testes automatizados (unitários, integração e autenticação)**
- ✅ **Deploy com Docker**

---

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```
git clone https://github.com/BManduca/app_medication_control.git
cd app_medication_control
```

### 2. Criar e ativar um ambiente virtual

```
# não é necessários os ()
python -m venv (nome_do_seu_ambiente)

# Windows
nome_do_seu_ambiente\Scripts\activate

# Linux/MacOS
source nome_do_seu_ambiente/bin/activate
```

### 3. Instalando as dependências

```
pip3 install -r requirements.txt
```

### 4. Crie o banco de dados local
* Com o ambiente virtual ativado, instale todas as dependências
* execute o comando: python3 create_db.py
* Isso criará todas as tabelas definidas em app/models.py no banco de dados configurado (como SQLite por padrão)

```
python3 create_db.py
```

### 5. Rodar o servidor

```
python3 app.py
# acessar aplicação: http://localhost:5000
```

**🔐 Para login via Google, crie um projeto no [Google Cloud Console](https://console.cloud.google.com), ative o OAuth 2.0 e adicione as credenciais nos arquivos `.env`**

### 6. Rodando com Docker (opcional)

```
docker build -t app_medication_control
docker run -p 5000:5000 app_medication_control
# acesse: http://localhost:5000
```

## 📁 Estrutura do Projeto

```
app/
├── auth/                  # Rotas de autenticação
├── models/                # Modelos SQLAlchemy
├── templates/             # Templates HTML (Jinja2)
├── static/                # Arquivos estáticos (Tailwind, ícones)
├── forms/                 # Formulários Flask-WTF
├── routes/                # Rotas de medicamentos, lembretes, histórico
├── utils/                 # Funções auxiliares
├── tests/                 # Testes automatizados (pytest)
```

---

## 👨🏻‍💻 Autor

[![LinkedIn](https://img.shields.io/badge/LinkedIn--blue?style=social&logo=linkedin)](https://www.linkedin.com/in/brunnomanduca/)  
**Brunno Manduca** – Desenvolvedor Web, buscando resolver problemas do dia a dia com soluções práticas e reais.

---

## 📝 Licença

Este projeto está licenciado sob a **Licença MIT** – sinta-se à vontade para usar, estudar e contribuir!

---
