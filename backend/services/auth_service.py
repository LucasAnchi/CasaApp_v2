from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models.userModels import Users
from jose import jwt
from security import bcrypt_context, SECRET_KEY, ALGORITHM


async def login_for_access_token(username: str, password: str, db: Session):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível autenticar o usuário",
        )

    token = create_access_token(user.username, user.user_id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_pass):
        return None

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
