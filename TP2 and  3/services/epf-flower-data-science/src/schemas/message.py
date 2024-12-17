from src.schemas.camelcase import CamelCase
from pydantic import BaseModel


class MessageResponse(CamelCase):
    message: str

class Parameter(BaseModel):
    n_estimators: int
    criterion: str

__all__ = ['Parameter', 'MessageResponse']
