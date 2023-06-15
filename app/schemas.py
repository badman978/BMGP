from typing import Optional
from pydantic import BaseModel, EmailStr


# Schemas
class Base(BaseModel):
    username: str
    password: str
    email: EmailStr 

class Produce(BaseModel):
    farm_produce: str
    qty: str
    on_sale: bool = False

class Farms(Base):
    address: str
    contact: str

class Users(Base):
    contact: str
    address: str

class Login(BaseModel):
    username: str
    password: str

# response models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
