from pydantic import BaseModel, EmailStr
from datetime import datetime



class Farm(BaseModel):
    username: str
    address: str
    email: EmailStr

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    address: str
    email: EmailStr

    class Config:
        orm_mode = True

class Farmer(BaseModel):
    id: int
    contact: str
    address: str
    created_at: datetime
    email: str

    class Config:
        orm_mode = True



class Produce(BaseModel):
    farm_produce: str
    farm: str
    qty: int
    id: int
    farmer: Farmer


    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True