from fastapi import FastAPI, HTTPException, Depends, status
from routers import auth_routers
from routers import user_routers
from routers import views_routers
from routers import items_routers
from routers import lista_routers
from models import userModels, listaModels
from database import engine, get_db
from services.user_service import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()
app.include_router(auth_routers.router)
app.include_router(user_routers.router)
app.include_router(items_routers.router)
# app.include_router(views_routers.router)
app.include_router(lista_routers.router)

userModels.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/login", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Falha na autenticação")
    return {"Login": True}


@app.get("/")
def root():
    return {"message": "API ON"}
