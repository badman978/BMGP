from typing import Optional
from pydantic import BaseModel, EmailStr


# Schemas
class Produce(BaseModel):
    farm_produce: str
    qty: str
    on_sale: bool = False


class Farms(BaseModel):
    username: str
    password: str
    email: EmailStr
    address: str
    contact: str


class Login(BaseModel):
    username: str
    password: str

# response models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
