from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.config.database import SessionLocal, User
from passlib.context import CryptContext
from src.dependencies import get_db
from src.models.user_auth import UserCreate, UserResponse
from src.utils.auth import create_access_token
from src.env.environment import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def checkIfUserExists(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

@router.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if checkIfUserExists(user.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.post("/login", response_model=UserResponse)
def login_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    user_db = checkIfUserExists(user.email, db)
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    if not pwd_context.verify(user.password, user_db.password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user_db.email}, expires_delta=access_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user_db.email,
            "name": user_db.name
        }
    }