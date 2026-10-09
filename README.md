# Pizza Shop

API REST desenvolvida com **Python (FastAPI)**, com rotas iniciais para cadastro de usuários e criação de pedidos. A persistência é feita com SQLAlchemy e o versionamento do esquema do banco é gerenciado pelo Alembic.

> **Status:** projeto em desenvolvimento. Algumas partes, especialmente o fluxo de login e a proteção das rotas, ainda precisam ser concluídas antes de qualquer uso em produção.

## Stack

- **Python** — linguagem principal
- **FastAPI** — criação das rotas HTTP e da API
- **SQLAlchemy** — mapeamento objeto-relacional (ORM)
- **SQLite** — banco configurado atualmente no projeto
- **Alembic** — migrações do esquema do banco de dados
- **Pydantic** — schemas e validação dos dados de entrada
- **Passlib + bcrypt** — hash de senha durante o cadastro
- **Uvicorn** — servidor ASGI para executar a aplicação
- **python-dotenv** — carregamento de variáveis de ambiente

## Funcionalidades presentes

- Cadastro de usuários com verificação de e-mail duplicado.
- Armazenamento de hash da senha no cadastro.
- Rotas iniciais relacionadas a autenticação e pedidos.
- Criação de pedidos associados a um ID de usuário.
- Modelos SQLAlchemy para usuários, pedidos e itens de pedido.
- Migração inicial das tabelas com Alembic.
- Documentação interativa dos endpoints fornecida pelo FastAPI.

## Estrutura do projeto

```text
python-api/
├── main.py                 # Cria a aplicação FastAPI e registra os routers
├── auth_routes.py           # Rotas de cadastro e login
├── order_routes.py          # Rotas relacionadas a pedidos
├── dependencies.py          # Dependência de sessão do banco
├── models.py                # Engine, modelos e tabelas SQLAlchemy
├── schemas.py               # Schemas Pydantic de entrada
├── requirements.txt         # Dependências Python
├── alembic.ini              # Configuração do Alembic
├── alembic/
│   ├── env.py
│   └── versions/             # Histórico de migrações
└── database/
    └── data.db               # Banco SQLite configurado no projeto
```

## Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/Vanelli-afk/pizza-shop.git
cd pizza-shop
```


### 2. Crie e ative um ambiente virtual

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Aplique as migrações

Execute a partir da raiz do projeto:

```bash
alembic upgrade head
```

A configuração atual do SQLAlchemy e do Alembic aponta para `database/data.db`, usando SQLite.

### 5. Inicie a API

```bash
uvicorn main:app --reload
```

Por padrão, a aplicação fica disponível em `http://127.0.0.1:8000`.

A documentação interativa pode ser acessada em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints existentes

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/auth/` | Retorna uma mensagem da rota inicial de autenticação. |
| `POST` | `/auth/create_profile` | Cadastra um usuário. O e-mail é verificado antes da criação e a senha é armazenada como hash. |
| `POST` | `/auth/login` | Rota de login criada, mas ainda incompleta; veja as limitações abaixo. |
| `GET` | `/orders/` | Retorna uma mensagem da rota de pedidos. |
| `POST` | `/orders/order` | Cria um pedido usando o `user_id` informado no corpo da requisição. |

### Exemplo: cadastrar um usuário

```bash
curl -X POST "http://127.0.0.1:8000/auth/create_profile" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ana Silva",
    "email": "ana@example.com",
    "password": "uma-senha-de-exemplo",
    "activated": true,
    "admin": false
  }'
```

O schema atual recebe `name`, `email`, `password`, `activated` e `admin`. O exemplo usa credenciais fictícias.

### Exemplo: criar um pedido

O endpoint recebe o ID de um usuário existente:

```bash
curl -X POST "http://127.0.0.1:8000/orders/order" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

No modelo atual, um novo pedido recebe `PENDING` como status e `0` como preço por padrão. O endpoint ainda não recebe itens ou preço no schema de entrada.

## Banco de dados e migrações

O projeto possui os seguintes modelos:

- **`User` (`users`)**: nome, e-mail, hash da senha, estado de ativação e indicador de administrador.
- **`Order` (`orders`)**: usuário associado, status e preço.
- **`OrderedItem` (`ordered_items`)**: quantidade, sabor, tamanho, preço unitário e pedido associado.

Para gerar uma migração após alterar os modelos, execute na raiz do projeto:

```bash
alembic revision --autogenerate -m "descreve a alteracao"
alembic upgrade head
```

Revise o arquivo de migração gerado antes de aplicá-lo. A configuração deve apontar para o banco que você realmente pretende atualizar.

## Limitações conhecidas

- **Banco de dados:** o código usa SQLite, não MySQL. A URL está definida em `models.py` e em `alembic.ini`.
- **Login:** o fluxo em `/auth/login` ainda não está funcional como autenticação completa. A consulta de usuário não é executada com `.first()`/`.one_or_none()`, a senha recebida não é verificada e `create_token()` retorna uma string de exemplo, não um JWT válido.
- **Proteção de rotas:** as rotas de pedidos não exigem nem validam token de autenticação no estado atual do código.
- **Itens de pedido:** existe um modelo para `OrderedItem`, mas ainda não há endpoints dedicados para gerenciar esses itens.

Essas limitações refletem o código atual do repositório e devem ser resolvidas antes de considerar a aplicação pronta para produção.
