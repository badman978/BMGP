from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..database import  get_db
from .. import models, responses, schemas, utils, oauth2
#


router = APIRouter(
    prefix= "/users",
    tags=['Users']
)



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=responses.User)
def create_user(user:schemas.Users, db: Session = Depends(get_db)):
    user.password=utils.hash(user.password)
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{username}", response_model=responses.User)
def get_farm(username: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User does not exist")

    return user


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, db: Session = Depends(get_db), farm_username:str = Depends(oauth2.get_current_farm)):
    query = db.query(models.Users).filter(models.Users.username == username)
    user = query.first()
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"farm with id({id}) does not exist")
    if user.username != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perfrom requested action")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)