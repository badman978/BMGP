
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, responses, schemas
from app import oauth2


#
#
router = APIRouter(
    prefix="/produce",
    tags=['Produce']
)

#8:48 

@router.get("/", response_model=List[responses.Produce])
def get_all_products(db: Session = Depends(get_db), limit: int = 5, search: Optional[str] = ''):
    produce = db.query(models.Produce).filter(models.Produce.farm_produce.contains(search)).limit(limit).all()
    return produce


# 8:28
@router.get("/farm", response_model=List[responses.Produce])
def get_all_products(db: Session = Depends(get_db), user: str =Depends(oauth2.get_current_farm)):
    print(user.username)
    produce = db.query(models.Produce).filter(models.Produce.farm == user.username)
    return produce


@router.get("/{id}", response_model=responses.Produce)
def get_produce(id : int, db: Session=Depends(get_db)):
    produce = db.query(models.Produce).filter(models.Produce.id == id).first()

    if not produce:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produce with id({id}) does not exist")

    return produce


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[responses.Produce])
def add_produce(produce: schemas.Produce, db: Session = Depends(get_db), farm_username:str = Depends(oauth2.get_current_farm)):
    
    
    new_produce = models.Produce(farm= farm_username.username, **produce.dict())

    db.add(new_produce)
    db.commit()
    db.refresh(new_produce)

    return { new_produce}


@router.put("/{id}", response_model=responses.Produce)
def update_produce(id:int, updated_prod: schemas.Produce, db:Session=Depends(get_db), user:str = Depends(oauth2.get_current_farm)):
    query = db.query(models.Produce).filter(models.Produce.id == id)
    produce = query.first()
    if produce == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produce with id({id}) does not exist")
    if produce.farm != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perfrom requested action")
    
    query.update(updated_prod.dict(), synchronize_session=False)
    
    db.commit()
    return query.first()



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produce(id:int, db: Session=Depends(get_db), user:str = Depends(oauth2.get_current_farm)):
    query = db.query(models.Produce).filter(models.Produce.id == id)
    produce = query.first()
    if produce == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"farm with id({id}) does not exist")
    
    if produce.farm != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perfrom requested action")
    
    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
