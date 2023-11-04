from fastapi import (status, Depends, APIRouter)
from fastapi.security import OAuth2PasswordBearer

from conf import settings
from src import schemas
from src.crud import UserCrudRepository
from src.api.dependencies.repository import get_repository
from utils.exceptions.http import exc_400
from src.auth.token import create_token


__all__ = ("router",)


router = APIRouter(prefix="/register", tags=["login"])


@router.post(
    '',
    name='user:register_user',
    response_model=schemas.UserRegisterSchemaOut,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    payload: schemas.UserRegisterSchemaIn,
    user_repo: UserCrudRepository = Depends(get_repository(repo_type=UserCrudRepository)),
):

    # user = await user_repo.register_user(instance=payload)

    # access_token = create_token(data={"id": user.id}, exp=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # refresh_token = create_token(data={"id": user.id}, exp=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    return await user_repo.register_user(instance=payload)
