# CasaApp

API REST para gerenciamento de itens domésticos — **estoque** e **lista de compras** — com autenticação JWT por usuário.

Cada usuário tem seu próprio estoque de itens e uma lista de compras independente, com **sugestão automática de quantidade** baseada no histórico de consumo.

## Tecnologias

- **FastAPI** — framework web
- **SQLAlchemy 2.0** — ORM (com `Mapped` / `mapped_column`)
- **MySQL** — banco de dados (via `pymysql`)
- **JWT** (`python-jose`) — autenticação
- **bcrypt** (`passlib`) — hash de senhas
- **Pydantic** — validação de schemas

## Pré-requisitos

- Python 3.10+
- MySQL rodando em `localhost:3306` com o banco `casaApp` criado:

```sql
CREATE DATABASE casaApp;
```

## Instalação

```bash
# Na raiz do projeto, crie o venv e instale as dependências
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com sua SECRET_KEY e DATABASE_URL
```

As variáveis `SECRET_KEY` e `DATABASE_URL` são **obrigatórias** — a aplicação não sobe sem elas.

### Variáveis de ambiente (`.env`)

```env
SECRET_KEY=troque_por_uma_chave_segura
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/casaApp
ALGORITHM=HS256
```

## Como rodar

```bash
cd backend
../.venv/bin/uvicorn main:app --reload
```

A API sobe em `http://localhost:8000`. A documentação interativa (Swagger) fica em `http://localhost:8000/docs`.

## Popular o banco (seed)

```bash
# Na raiz do projeto
.venv/bin/python seed.py
```

Cria 3 usuários de exemplo, cada um com 12–14 itens e datas retroativas (para o cálculo de quantidade ótima funcionar):

| Usuário       | Senha     |
|---------------|-----------|
| `ana_silva`   | `ana123`  |
| `joao_costa`  | `joao123` |
| `maria_souza` | `maria123`|

## Autenticação

1. `POST /auth/token` — envia `username` e `password` (form-data) e recebe um JWT.
2. As rotas protegidas exigem o header `Authorization: Bearer <token>`.

O token expira em **20 minutos** e carrega `sub=username` e `id=user_id`.

## Endpoints

### Auth
| Método | Rota          | Descrição                         |
|--------|---------------|-----------------------------------|
| POST   | `/auth/token` | Login e emissão do JWT            |

### Usuários
| Método | Rota         | Descrição                          |
|--------|--------------|------------------------------------|
| POST   | `/users/`    | Cria um novo usuário               |
| GET    | `/users/me`  | Dados do usuário autenticado       |
| POST   | `/users/me`  | Atualiza o usuário autenticado     |
| DELETE | `/users/me`  | Remove o usuário autenticado       |

### Estoque (items) — requer autenticação
| Método | Rota                       | Descrição                    |
|--------|----------------------------|------------------------------|
| GET    | `/items/`                  | Lista os itens do estoque    |
| POST   | `/items/`                  | Cria um item                 |
| PUT    | `/items/{id}`              | Atualiza um item             |
| PATCH  | `/items/{id}/deactivate`   | Desativa um item             |
| DELETE | `/items/{id}`              | Remove um item               |

### Lista de compras — requer autenticação
| Método | Rota              | Descrição                                            |
|--------|-------------------|------------------------------------------------------|
| GET    | `/lista/`         | Retorna a lista de compras                           |
| POST   | `/lista/`         | Adiciona um item à lista                             |
| POST   | `/lista/popular`  | Auto-popula a lista com itens ativos do estoque      |
| PUT    | `/lista/{id}`     | Atualiza um item da lista                            |
| DELETE | `/lista/{id}`     | Remove um item da lista                              |
| DELETE | `/lista/limpar`   | Esvazia a lista de compras                           |

## Arquitetura

O backend é organizado em camadas (`models` → `schemas` → `services` → `routers`):

```
backend/
├── main.py            # entry point — registra routers, cria tabelas
├── database.py        # engine MySQL, SessionLocal, Base, get_db()
├── config.py          # carrega .env (SECRET_KEY, DATABASE_URL, ALGORITHM)
├── security.py        # bcrypt_context, oauth2_bearer
├── models/
│   ├── userModels.py  # ORM: tabela users
│   ├── itemModels.py  # ORM: tabela items
│   ├── listaModels.py # ORM: tabela lista_compras
│   └── schemas.py     # Pydantic: schemas de request/response
├── services/          # regras de negócio (auth, user, item, lista)
└── routers/           # endpoints HTTP
```

### Lista de compras inteligente

A tabela `lista_compras` é independente do estoque. `POST /lista/popular` auto-popula a lista com os itens ativos do estoque usando `getOptimalQuantidade`, que calcula:

```
quantidade sugerida = total adicionado / meses desde o primeiro registro
```

Itens já presentes na lista não são duplicados.

## Pendências conhecidas

- O frontend (`frontend/templates/`, `frontend/static/`) existe, mas `views_routers` está desativado e o Jinja2 não está configurado em `main.py`.
