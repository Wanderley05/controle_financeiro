# 💰 Finance Manager

Aplicação web de controle financeiro pessoal desenvolvida com **Python + Streamlit + SQLite**.

---

## 📋 Funcionalidades

- ✅ Cadastro e login de usuários com senha criptografada
- ✅ Registro de transações (receitas e despesas)
- ✅ Categorização por tipo: Alimentação, Transporte, Moradia, Lazer, Salário e Outros
- ✅ Dashboard com resumo de receitas, despesas e saldo
- ✅ Filtros por categoria e tipo de transação
- ✅ Gráfico de pizza com gastos por categoria
- ✅ Gráfico de linha com evolução financeira
- ✅ Exclusão de transações
- ✅ Log de ações do sistema

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| Streamlit | Interface web |
| SQLite | Banco de dados local |
| Pandas | Manipulação de dados |
| Plotly | Gráficos interativos |
| Bcrypt | Hash de senhas |

---

## 📁 Estrutura do Projeto

```
controle_financeiro/
│
├── app.py          # Interface principal (Streamlit)
├── database.py     # Funções de acesso ao banco de dados
├── auth.py         # Funções de autenticação (hash/verify)
├── requirements.txt
└── README.md
```

---

## ⚙️ Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/controle-financeiro.git
cd controle-financeiro
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode a aplicação

```bash
streamlit run app.py
```

Acesse em: [http://localhost:8501](http://localhost:8501)

---

## 📦 requirements.txt

```
streamlit
pandas
plotly
bcrypt
```

---

## 🗄️ Banco de Dados

O banco `financeiro.db` é criado automaticamente na primeira execução. Ele contém três tabelas:

- **usuarios** — armazena usuários e senhas (hash bcrypt)
- **transacoes** — armazena as transações de cada usuário
- **logs** — registra ações realizadas no sistema

> ⚠️ O arquivo `financeiro.db` não deve ser versionado. Adicione-o ao `.gitignore`.

---

## 🔒 Segurança

As senhas são armazenadas com hash **bcrypt** — nunca em texto puro.

---

## 📸 Preview

> Dashboard com métricas de receitas, despesas, saldo e gráficos por categoria.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar e modificar.