from fastapi import APIRouter
from src.schemas.message import Parameter
from src.services.parameters import get_parameters, update_parameters
from fastapi import  HTTPException

router = APIRouter()

@router.get("/parameters")
async def read_parameters():
    params = get_parameters()
    if not params:
        raise HTTPException(status_code=404, detail="Parameters not found")
    return params

@router.put("/parameters")
async def update_params(params: Parameter):
    update_parameters(params.dict())
    return {"message": "Parameters updated successfully"}

