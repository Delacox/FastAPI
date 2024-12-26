from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None  # Hacer que el campo id sea opcional
    username: str
    email: str