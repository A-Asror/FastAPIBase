from uuid import UUID

from fastapi import (APIRouter, Depends, Request, status)

from src.api.dependencies.repository import get_repository
from src import schemas
from src.crud import UserCrudRepository
from .login.register import router as login_router

router = APIRouter(prefix="/user", tags=["user"])
router.add_route(path="/", endpoint=login_router)


@router.get(
    '',
    name='user:retrieve_user',
    response_model=schemas.UserRetrieveSchemaOut,
    status_code=status.HTTP_200_OK
)
async def retrieve_user(
        uuid: UUID,
        request: Request,
        user_repo: UserCrudRepository = Depends(get_repository(repo_type=UserCrudRepository))
):
    return await user_repo.retrieve_user(uuid=uuid)


@router.patch(
    '',
    name='user:update_user',
    response_model=schemas.UserUpdateSchemaOut,
    status_code=status.HTTP_200_OK
)
async def update_user(
        user_id: UUID,
        payload: schemas.UserUpdateSchemaIn,
        user_repo: UserCrudRepository = Depends(get_repository(repo_type=UserCrudRepository))
):
    return await user_repo.update_user_by_id(uuid=user_id, payload=payload)


@router.patch(
    '/unique',
    name='user:update_user_unique_fields',
    response_model=schemas.UserUpdateSchemaOut,
    status_code=status.HTTP_200_OK
)
async def update_user_unique_fields(
        user_id: UUID,
        payload: schemas.UserUpdateUniqueFieldsSchemaIn,
        user_repo: UserCrudRepository = Depends(get_repository(repo_type=UserCrudRepository))
):
    return await user_repo.update_user_unique_fields_by_id(uuid=user_id, payload=payload)

# @router.delete('', name='transport:delete_cargo', status_code=status.HTTP_200_OK)
# async def create_cargo(
#     pk: int,
#     cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository)),
# ):
#     return await cargo_repo.delete_by_id(cargo_id=pk)
#
#

#
# @router.get(
#     '/{cargo_id}',
#     response_model=schemas.CargoInfoOutSchema,
#     response_model_exclude={'transports': {"__all__": {'location_lat', 'location_lng'}}},
#     status_code=status.HTTP_200_OK
# )
# async def read_cargo_many(
#     cargo_id: int,
#     cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository))
# ):
#     cargo = await cargo_repo.read_by_id(cargo_id=cargo_id)
#     transports = await cargo_repo.read_all_transports()
#
#     response = schemas.CargoInfoOutSchema(
#         id=cargo.id,
#         pick_up_post_code=cargo.pick_up_post_code,
#         delivery_post_code=cargo.delivery_post_code,
#         weight=cargo.weight,
#         description=cargo.description,
#         transports=transports
#     )
#     response.distance(lat=cargo.pick_up_lat, lng=cargo.pick_up_lng)
#     return response
#
#
# @router.get(
#     '/filter/',
#     response_model=list[schemas.CargoFilterByRadiusWeightOutSchema],
#     response_model_exclude={'transports': {"__all__": {'location_lat', 'location_lng'}}},
#     status_code=status.HTTP_200_OK
# )
# async def read_cargo_filter(
#     query: schemas.CargoInQueryParamsSchema = Depends(),
#     cargo_repo: CargoCRUDRepository = Depends(get_repository(repo_type=CargoCRUDRepository))
# ):
#
#     return await cargo_repo.filter_by_radius_and_weight(radius=query.radius, weight=query.weight, page=query.page)
