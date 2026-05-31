from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from services.user_service import create_user, update_user, delete_user
from services.user_service import get_current_user
from models.schemas import UserAdd, UserResponse, UserUpdate
from models.userModels import Users

router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/")
async def add_user(user: UserAdd, db: db_dependency):
    return await create_user(db, user)


@router.get("/me", response_model=UserResponse)
async def get_me(user: Annotated[Users, Depends(get_current_user)]):
    return user


@router.post("/me")
async def updateMe(
    new_user: UserUpdate,
    db: db_dependency,
    current_user: Annotated[Users, Depends(get_current_user)],
):
    return await update_user(db, current_user.user_id, new_user)


@router.delete("/me")
async def deleteMe(
    db: db_dependency, current_user: Annotated[Users, Depends(get_current_user)]
):
    return await delete_user(db, current_user.user_id)
