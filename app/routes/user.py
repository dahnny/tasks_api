from fastapi import APIRouter, HTTPException,status
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = next(get_db())):
    user.password = hash_password(user.password)
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    db_user = User(
        email=user.email,
        password=user.password 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user