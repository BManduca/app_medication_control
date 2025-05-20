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

### 💾 Banco de Dados

- **SQLite** - Banco de dados leve e embutido

### 🎨 Front-end

- **HTML + Jinja2** - Templates dinâmicos
- **Tailwind CSS** - Estilização moderna e responsiva

### 🛠️ Ferramentas de Suporte

- **Git / GitHub** - Versionamento e colaboração
- **venv** - Ambiente virtual Python
- **requirements.txt** - Lista de dependências

## 🧪 Funcionalidades

- ✅ **Registro e login de usuários**
- ✅ **Criptografia de senhas**
- ✅ **Autenticação de sessões com Flask-Login**
- ✅ **Cadastro, edição e remoção de medicamentos**
- ✅ **Listagem de medicamentos**
- ✅ **Layout responsivo com Tailwind CSS**

---

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

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

### 4. Criando o banco de dados

```
python3 create_db.py
```

### 5. Rodar o servidor

```
python3 app.py
# acessar aplicação: http://localhost:5000
```

---

## 📝 Licença

**Este projeto está sob a licença MIT. Sinta-se livre para usar, estudar e contribuir.**

---

## Autor

### [Linkedin Brunno Manduca](https://www.linkedin.com/in/brunnomanduca/)
