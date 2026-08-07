from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    activated: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

    # Essencialmente padroniza o usuario como objeto pra organizar e
    # facilitar validacoes enquanto trabalha com os parametros

class OrderSchema(BaseModel):
    user_id: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True