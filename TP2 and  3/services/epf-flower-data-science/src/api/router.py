"""API Router for Fast API."""
from fastapi import APIRouter

from src.api.routes import hello, documentation

router = APIRouter()

router.include_router(hello.router, tags=["Hello"])
router.include_router(documentation.router, tags=["doc"])