from fastapi import APIRouter
from .routes import parameters
from fastapi.responses import RedirectResponse
from src.api.routes import hello
from src.api.routes import data
from .routes import authentication

router = APIRouter()

@router.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

router.include_router(hello.router, tags=["Hello"])
router.include_router(data.router, prefix="/data", tags=["Dataset"])
router.include_router(parameters.router, tags=["parameters"])
router.include_router(authentication.router, tags=["authentication"])
