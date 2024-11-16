from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import User
from app.database.connection import get_db
from app.core.security import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el correo electrónico ya está registrado
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear nuevo usuario
    hashed_password = get_password_hash(user_data.password)
    user = User(name=user_data.name, email=user_data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/search", response_model=list[UserResponse])
def search_users(query: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.name.ilike(f"%{query}%")).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/auto-translate", response_model=UserResponse)
def toggle_auto_translate(user_id: int, auto_translate: bool, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.auto_translate = auto_translate
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}/profile", response_model=UserResponse)
def update_user_profile(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Actualizar los campos si están presentes en los datos de entrada
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.profile_picture is not None:
        user.profile_picture = str(user_data.profile_picture)
    if user_data.interests is not None:
        user.interests = user_data.interests
    if user_data.skills is not None:
        user.skills = user_data.skills
    if user_data.social_links is not None:
        user.social_links = user_data.social_links

    db.commit()
    db.refresh(user)
    return user