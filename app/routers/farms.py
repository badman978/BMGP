from ..database import  get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, responses, schemas, utils, oauth2





#
#

router = APIRouter(
    prefix= "/farms",
    tags=['Farms']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=responses.Farm)
def create_farmer(farm:schemas.Farms, db: Session = Depends(get_db)):
    farm.password=utils.hash(farm.password)
    new_farm = models.Farms(**farm.dict())
    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm

@router.get("/", response_model=List[responses.Farm])
def get_farms(db: Session = Depends(get_db)):
    
    farms=db.query(models.Farms).all()
    return  farms


@router.get("/{id}", response_model=responses.Farm)
def get_farm(id : int, db: Session=Depends(get_db)):
    farm = db.query(models.Farms).filter(models.Farms.id == id).first()
    
    if not farm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produce does not exist")

    return farm


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(id:int, db:Session=Depends(get_db), user:str = Depends(oauth2.get_current_farm)):
    query = db.query(models.Farms).filter(models.Farms.id == id)
    farm = query.first()
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"farm with id({id}) does not exist")
    if farm.username != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perfrom requested action")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", response_model=responses.Farm)
def update_farm(id:int, updated_farm: schemas.Farms, db: Session = Depends(get_db), user:str = Depends(oauth2.get_current_farm)):
    query = db.query(models.Farms).filter(models.Farms.id == id)
    farm = query.first()
    if farm == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produce with id({id}) does not exist")
    if farm.username != user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perfrom requested action")
    
    query.update(updated_farm.dict(), synchronize_session=False)
    db.commit()
    return {"data":query.first()}