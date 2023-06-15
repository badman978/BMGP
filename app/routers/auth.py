from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from .. import schemas, models, utils, oauth2, responses

router=APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=responses.Token)
def login_farmer(login_credentials:OAuth2PasswordRequestForm= Depends(), db:Session = Depends(get_db), ):

    farm = db.query(models.Farms).filter(models.Farms.username == login_credentials.username).first()

    if not farm:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
    if not utils.authentication(login_credentials.password, farm.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
    access_token = oauth2.create_access_token(data = {"farm_username": farm.username})

    return {"access_token": access_token, "token_type":"bearer"}



 