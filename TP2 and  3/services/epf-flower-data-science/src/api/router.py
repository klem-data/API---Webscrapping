"""API Router for Fast API."""
from fastapi import APIRouter
from src.api.routes import hello, data


router = APIRouter()

router.include_router(hello.router, tags=["Hello"])
