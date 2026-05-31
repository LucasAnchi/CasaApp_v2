# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este projeto

API REST para gerenciamento de itens domésticos (estoque e lista de compras), com autenticação JWT por usuário. Cada usuário tem seu próprio estoque de itens e uma lista de compras independente com sugestão automática de quantidade baseada no histórico de consumo.

## Como rodar

```bash
# Na raiz do projeto, crie o venv e instale as dependências
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Configure as variáveis de ambiente (copie e edite)
cp .env.example .env

# Rode a partir de backend/
cd backend
../.venv/bin/uvicorn main:app --reload
```

Requer MySQL rodando em `localhost:3306` com banco `casaApp` criado. As variáveis `SECRET_KEY` e `DATABASE_URL` são obrigatórias — a aplicação não sobe sem elas.

## Popular o banco

```bash
# Na raiz do projeto
.venv/bin/python seed.py
```

Cria 3 usuários (`ana_silva/ana123`, `joao_costa/joao123`, `maria_souza/maria123`) com 12–14 itens cada, com datas retroativas para o cálculo de quantidade ótima funcionar.

## Arquitetura

### Camadas

```
backend/
├── main.py            # entry point — registra routers, cria tabelas
├── database.py        # engine MySQL, SessionLocal, Base (DeclarativeBase), get_db()
├── config.py          # carrega .env com python-dotenv, exporta SECRET_KEY, DATABASE_URL, ALGORITHM
├── security.py        # bcrypt_context, oauth2_bearer (importa config.py)
├── models/
│   ├── userModels.py  # ORM: tabela users
│   ├── itemModels.py  # ORM: tabela items
│   ├── listaModels.py # ORM: tabela lista_compras
│   └── schemas.py     # Pydantic: todos os schemas de request/response
├── services/
│   ├── auth_service.py   # login_for_access_token, authenticate_user, create_access_token
│   ├── user_service.py   # create_user, get_current_user (JWT decode), update_user, delete_user
│   ├── item_service.py   # get_items, create_item, update_item, delete_item, deactivate_item
│   └── lista_service.py  # getLista, addItemLista, popularLista, updateItemLista, deleteItemLista, limparLista
└── routers/
    ├── auth_routers.py   # POST /auth/token
    ├── user_routers.py   # GET/POST/DELETE /users/me, POST /users/
    ├── items_routers.py  # GET /items/, POST /items/, PUT /items/{id}, PATCH /items/{id}/deactivate, DELETE /items/{id}
    ├── lista_routers.py  # GET /lista/, POST /lista/, POST /lista/popular, PUT /lista/{id}, DELETE /lista/{id}, DELETE /lista/limpar
    └── views_routers.py  # templates Jinja2 — desativado em main.py
```

### Models usam SQLAlchemy 2.0

Todos os campos usam `Mapped[tipo] = mapped_column(...)` para que o Pylance infira os tipos corretamente. Evitar voltar para o estilo `Column(Tipo)` sem anotação.

### Fluxo de autenticação

1. `POST /auth/token` → `auth_service.authenticate_user` verifica bcrypt → `create_access_token` retorna JWT com `sub=username` e `id=user_id` (expira em 20 min)
2. Rotas protegidas usam `Depends(get_current_user)` de `user_service.py`, que decodifica o JWT e retorna o objeto `Users` do banco

### Lista de compras

A tabela `lista_compras` é independente do estoque. `POST /lista/popular` auto-popula a lista com itens ativos do estoque usando `getOptimalQuantidade`, que calcula `total_add / meses_desde_primeiro_add`. Itens já presentes na lista não são duplicados.

### Relação entre modelos

`Users` 1→N `Items` via `Items.owner_id`. `Users` 1→N `ListaCompras` via `ListaCompras.owner_id`. Relacionamento declarado em `userModels.py` com `relationship("Items", backref="user")`.

## Pendências conhecidas

- Frontend (`frontend/templates/`, `frontend/static/`) existe mas `views_routers` está desativado e Jinja2 não está configurado em `main.py`
