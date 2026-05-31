from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.schemas import UserAdd, UserUpdate, UserResponse
from models.userModels import Users
from models.itemModels import Items
from uuid import uuid4
from security import bcrypt_context, oauth2_bearer, SECRET_KEY, ALGORITHM
from database import get_db
from typing import Annotated
from fastapi import Depends
from jose import jwt, JWTError
from starlette import status


async def create_user(db: Session, create_user_request: UserAdd):
    existing_user = (
        db.query(Users).filter(Users.username == create_user_request.username).first()
    )

    if existing_user:
        raise HTTPException(400, "Usuário já existe")
    create_user_model = Users(
        username=create_user_request.username,
        hashed_pass=bcrypt_context.hash(create_user_request.password),
        uuid=str(uuid4()),
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "Usuário criado com sucesso"}


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível autenticar o usuário",
            )

        user = db.query(Users).filter(Users.user_id == user_id).first()

        if not user:
            raise HTTPException(401, "Usuário inválido")

        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível autenticar o usuário",
        )


async def update_user(db: Session, user_id: int, new_user: UserUpdate):
    user = db.query(Users).filter(Users.user_id == user_id).first()

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    if new_user.username is not None:
        existing_user = (
            db.query(Users).filter(Users.username == new_user.username).first()
        )

        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(400, "Username já existe")

        user.username = new_user.username

    if new_user.password is not None:
        user.hashed_pass = bcrypt_context.hash(new_user.password)

    db.commit()
    db.refresh(user)

    return UserResponse.model_validate(user)


async def delete_user(
    db: Session,
    user_id: int,
):
    user = db.query(Users).filter(Users.user_id == user_id).first()

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    db.delete(user)
    db.commit()

    return {"Usuário deletado"}
