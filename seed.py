import sys
import datetime
from uuid import uuid4

sys.path.insert(0, "backend")

from database import SessionLocal, engine
from models.userModels import Users
from models.itemModels import Items
from models import userModels, listaModels
from security import bcrypt_context

userModels.Base.metadata.create_all(bind=engine)

db = SessionLocal()

USUARIOS = [
    {"username": "ana_silva",   "password": "ana123"},
    {"username": "joao_costa",  "password": "joao123"},
    {"username": "maria_souza", "password": "maria123"},
]

ITENS = {
    "ana_silva": [
        {"nome": "Arroz",          "quantidade": 3,   "preco": 22.90, "marca": "Tio João",   "categoria": "Alimentos",  "dias": 60},
        {"nome": "Feijão",         "quantidade": 2,   "preco": 9.50,  "marca": "Camil",      "categoria": "Alimentos",  "dias": 45},
        {"nome": "Macarrão",       "quantidade": 4,   "preco": 4.80,  "marca": "Barilla",    "categoria": "Alimentos",  "dias": 30},
        {"nome": "Óleo de Soja",   "quantidade": 2,   "preco": 7.90,  "marca": "Soya",       "categoria": "Alimentos",  "dias": 50},
        {"nome": "Açúcar",         "quantidade": 1,   "preco": 5.50,  "marca": "União",      "categoria": "Alimentos",  "dias": 40},
        {"nome": "Café",           "quantidade": 2,   "preco": 18.90, "marca": "Pilão",      "categoria": "Alimentos",  "dias": 20},
        {"nome": "Leite",          "quantidade": 6,   "preco": 5.20,  "marca": "Itambé",     "categoria": "Alimentos",  "dias": 15},
        {"nome": "Detergente",     "quantidade": 3,   "preco": 2.50,  "marca": "Ypê",        "categoria": "Limpeza",    "dias": 30},
        {"nome": "Sabão em Pó",    "quantidade": 1,   "preco": 14.90, "marca": "OMO",        "categoria": "Limpeza",    "dias": 45},
        {"nome": "Amaciante",      "quantidade": 1,   "preco": 11.90, "marca": "Comfort",    "categoria": "Limpeza",    "dias": 60},
        {"nome": "Shampoo",        "quantidade": 1,   "preco": 17.90, "marca": "Pantene",    "categoria": "Higiene",    "dias": 45},
        {"nome": "Papel Higiênico","quantidade": 8,   "preco": 19.90, "marca": "Neve",       "categoria": "Higiene",    "dias": 30},
    ],
    "joao_costa": [
        {"nome": "Arroz",          "quantidade": 5,   "preco": 21.50, "marca": "Namorado",   "categoria": "Alimentos",  "dias": 55},
        {"nome": "Feijão Preto",   "quantidade": 3,   "preco": 8.90,  "marca": "Camil",      "categoria": "Alimentos",  "dias": 40},
        {"nome": "Farinha",        "quantidade": 2,   "preco": 6.20,  "marca": "Dona Benta", "categoria": "Alimentos",  "dias": 35},
        {"nome": "Sal",            "quantidade": 1,   "preco": 2.90,  "marca": "Cisne",      "categoria": "Alimentos",  "dias": 90},
        {"nome": "Manteiga",       "quantidade": 2,   "preco": 12.50, "marca": "Aviação",    "categoria": "Alimentos",  "dias": 25},
        {"nome": "Ovos",           "quantidade": 12,  "preco": 14.90, "marca": "Mantiqueira","categoria": "Alimentos",  "dias": 15},
        {"nome": "Pão de Forma",   "quantidade": 2,   "preco": 8.90,  "marca": "Wickbold",   "categoria": "Alimentos",  "dias": 7},
        {"nome": "Desinfetante",   "quantidade": 2,   "preco": 4.90,  "marca": "Pinho Sol",  "categoria": "Limpeza",    "dias": 30},
        {"nome": "Esponja",        "quantidade": 5,   "preco": 1.50,  "marca": "Scotch-Brite","categoria": "Limpeza",   "dias": 20},
        {"nome": "Sabonete",       "quantidade": 4,   "preco": 2.80,  "marca": "Lux",        "categoria": "Higiene",    "dias": 30},
        {"nome": "Creme Dental",   "quantidade": 2,   "preco": 5.90,  "marca": "Colgate",    "categoria": "Higiene",    "dias": 45},
        {"nome": "Desodorante",    "quantidade": 1,   "preco": 14.90, "marca": "Rexona",     "categoria": "Higiene",    "dias": 30},
        {"nome": "Papel Toalha",   "quantidade": 4,   "preco": 9.90,  "marca": "Snob",       "categoria": "Limpeza",    "dias": 25},
    ],
    "maria_souza": [
        {"nome": "Arroz Integral", "quantidade": 2,   "preco": 12.90, "marca": "Camil",      "categoria": "Alimentos",  "dias": 50},
        {"nome": "Granola",        "quantidade": 1,   "preco": 24.90, "marca": "Quaker",     "categoria": "Alimentos",  "dias": 30},
        {"nome": "Azeite",         "quantidade": 1,   "preco": 34.90, "marca": "Gallo",      "categoria": "Alimentos",  "dias": 60},
        {"nome": "Iogurte",        "quantidade": 6,   "preco": 4.50,  "marca": "Danone",     "categoria": "Alimentos",  "dias": 10},
        {"nome": "Queijo",         "quantidade": 1,   "preco": 22.90, "marca": "Polenghi",   "categoria": "Alimentos",  "dias": 14},
        {"nome": "Presunto",       "quantidade": 1,   "preco": 15.90, "marca": "Sadia",      "categoria": "Alimentos",  "dias": 10},
        {"nome": "Achocolatado",   "quantidade": 2,   "preco": 9.90,  "marca": "Nescau",     "categoria": "Alimentos",  "dias": 20},
        {"nome": "Amaciante",      "quantidade": 2,   "preco": 13.90, "marca": "Downy",      "categoria": "Limpeza",    "dias": 40},
        {"nome": "Água Sanitária", "quantidade": 2,   "preco": 3.90,  "marca": "Qboa",       "categoria": "Limpeza",    "dias": 30},
        {"nome": "Condicionador",  "quantidade": 1,   "preco": 19.90, "marca": "Elsève",     "categoria": "Higiene",    "dias": 45},
        {"nome": "Hidratante",     "quantidade": 1,   "preco": 22.90, "marca": "Nivea",      "categoria": "Higiene",    "dias": 60},
        {"nome": "Fio Dental",     "quantidade": 2,   "preco": 4.90,  "marca": "Oral-B",     "categoria": "Higiene",    "dias": 30},
        {"nome": "Café Cápsula",   "quantidade": 10,  "preco": 2.90,  "marca": "Nespresso",  "categoria": "Alimentos",  "dias": 15},
        {"nome": "Vinho",          "quantidade": 2,   "preco": 49.90, "marca": "Salton",     "categoria": "Bebidas",    "dias": 30},
    ],
}

try:
    for u in USUARIOS:
        existente = db.query(Users).filter(Users.username == u["username"]).first()
        if existente:
            print(f"Usuário {u['username']} já existe, pulando...")
            continue

        usuario = Users(
            username=u["username"],
            hashed_pass=bcrypt_context.hash(u["password"]),
            uuid=str(uuid4()),
        )
        db.add(usuario)
        db.flush()

        for i in ITENS[u["username"]]:
            add_data = datetime.date.today() - datetime.timedelta(days=i["dias"])
            item = Items(
                owner_id=usuario.user_id,
                nome=i["nome"],
                quantidade=i["quantidade"],
                preco=i["preco"],
                marca=i["marca"],
                categoria=i["categoria"],
                total_add=i["quantidade"],
                add_data=add_data,
                ativo=True,
            )
            db.add(item)

        print(f"Criado: {u['username']} com {len(ITENS[u['username']])} itens")

    db.commit()
    print("\nBanco populado com sucesso!")

except Exception as e:
    db.rollback()
    print(f"Erro: {e}")
    raise

finally:
    db.close()
