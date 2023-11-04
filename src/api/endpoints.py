import fastapi

from .routes import user_router

router = fastapi.APIRouter()


router.include_router(router=user_router)
