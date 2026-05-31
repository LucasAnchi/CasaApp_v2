# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é este projeto

API REST para gerenciamento de itens domésticos (estoque/lista de compras), com autenticação JWT por usuário. Cada usuário tem seus próprios itens com nome, quantidade, preço, marca, categoria e estado ativo/inativo.

## Como rodar

```bash
# A partir de backend/
export SECRET_KEY="sua_chave_secreta_aqui"
cd backend
uvicorn main:app --reload
```

Requer MySQL rodando em `localhost:3306` com banco `casaApp` criado. A variável `SECRET_KEY` é obrigatória — a aplicação não sobe sem ela.

## Como rodar os testes manuais

A pasta `teste/` contém scripts manuais (não pytest). Para rodar:
```bash
cd teste
python main_teste.py
```

Não há testes automatizados ainda. Ao escrever testes, usar `pytest` com fixtures que importam os módulos de `backend/` diretamente — **não duplicar** os arquivos de `backend/` na pasta `teste/`.

## Arquitetura

### Camadas

```
backend/
├── main.py           # entry point — registra routers, cria tabelas
├── database.py       # engine MySQL, SessionLocal, get_db()
├── security.py       # SECRET_KEY, ALGORITHM, bcrypt_context, oauth2_bearer
├── models/
│   ├── userModels.py # ORM: tabela users (user_id, username, hashed_pass, uuid)
│   ├── itemModels.py # ORM: tabela items (item_id, owner_id FK, nome, quantidade, preco, marca, categoria, ativo)
│   └── schemas.py    # Pydantic: UserAdd, UserUpdate, UserResponse, ItemAdd, ItemUpdate, ItemResponse, Token
├── routers/          # só fazem parsing HTTP e delegam para services
├── services/
│   ├── auth_service.py   # login_for_access_token, authenticate_user, create_access_token
│   ├── user_service.py   # create_user, get_current_user (JWT decode), update_user, delete_user
│   └── item_service.py   # create_item, update_item, delete_item, deactivate_item
└── routers/
    ├── auth_routers.py   # POST /auth/token
    ├── user_routers.py   # GET/POST/DELETE /users/me, POST /users/
    ├── items_routers.py  # POST /items/add, POST /items/update, DELETE /items/delete
    └── views_routers.py  # templates Jinja2 — atualmente comentado em main.py
```

### Fluxo de autenticação

1. `POST /auth/token` → `auth_service.authenticate_user` verifica bcrypt → `create_access_token` retorna JWT com `sub=username` e `id=user_id`
2. Qualquer rota protegida usa `Depends(get_current_user)` de `user_service.py`, que decodifica o JWT e retorna o objeto `Users` do banco

### Relação entre modelos

`Users` 1→N `Items` via `Items.owner_id = users.user_id`. O relacionamento SQLAlchemy está em `userModels.py` como `relationship("Items", backref="user")`.

## Pendências conhecidas

- Frontend (`frontend/templates/`, `frontend/static/`) existe mas `views_routers` está desativado e Jinja2 não está configurado em `main.py`
