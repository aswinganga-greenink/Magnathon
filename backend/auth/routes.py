from fastapi import APIRouter, HTTPException
from auth.schemas import UserCreate, UserLogin, Token
from auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# TEMP in-memory store (replace with DB)
_fake_users = {}

@router.post("/signup", response_model=Token)
def signup(data: UserCreate):
    if data.email in _fake_users:
        raise HTTPException(status_code=400, detail="User already exists")

    _fake_users[data.email] = {
        "email": data.email,
        "password": hash_password(data.password),
        "id": data.email,  # replace with real ID later
    }

    token = create_access_token({"sub": data.email})
    return {"access_token": token}


@router.post("/login", response_model=Token)
def login(data: UserLogin):
    user = _fake_users.get(data.email)
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": data.email})
    return {"access_token": token}
