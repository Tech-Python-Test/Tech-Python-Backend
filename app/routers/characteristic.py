from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.characteristic import CharacteristicCreate, CharacteristicResponse, CharacteristicUpdate
from app.models.characteristics import Characteristic
from app.database.connection import get_db

router = APIRouter(
    prefix="/characteristic",
    tags=["characteristic"]
)

@router.post("/create", response_model=CharacteristicResponse)
def register_characteristic(characteristic_data: CharacteristicCreate, db: Session = Depends(get_db)):
    # Verificar duplicado
    existing_characteristic = db.query(Characteristic).filter(Characteristic.name == characteristic_data.name).first()
    if existing_characteristic:
        raise HTTPException(status_code=400, detail="Characteristic already registered")

    # Crear 
    characteristic = Characteristic(name=characteristic_data.name)
    db.add(characteristic)
    db.commit()
    db.refresh(characteristic)
    return characteristic


@router.get("/{characteristic_id}", response_model=CharacteristicResponse)
def get_characteristic(characteristic_id: int, db: Session = Depends(get_db)):
    characteristic = db.query(Characteristic).filter(Characteristic.id == characteristic_id).first()
    if not characteristic:
        raise HTTPException(status_code=404, detail="Characteristic not found")
    return characteristic


@router.put("/{characteristic_id}", response_model=CharacteristicResponse)
def update_characteristic(characteristic_id: int, characteristic_data: CharacteristicUpdate, db: Session = Depends(get_db)):
    characteristic = db.query(Characteristic).filter(Characteristic.id == characteristic_id).first()
    if not characteristic:
        raise HTTPException(status_code=404, detail="Characteristic not found")

    # Actualizar los campos si están presentes en los datos de entrada
    if characteristic_data.name is not None:
        characteristic.name = characteristic_data.name

    db.commit()
    db.refresh(characteristic)
    return characteristic
