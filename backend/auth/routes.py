from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from database import get_session
from models import User
from auth.schemas import UserCreate, UserLogin, Token
from auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=Token)
def signup(data: UserCreate, session: Session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.email == data.email)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        email=data.email, 
        password_hash=hash_password(data.password),
        full_name=data.full_name
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    token = create_access_token({"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
