from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import  jwt
from datetime import datetime, timedelta
from typing import Optional
import asyncio

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

# In-memory database simulation
fake_db = {
    "users": []
}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: EmailStr
    disabled: Optional[bool] = False

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(username: str):
    for user in fake_db['users']:
        if user['username'] == username:
            return UserInDB(**user)
    return None

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/register")
async def register(user: UserCreate):
    if await get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data['hashed_password'] = hashed_password
    del user_data['password']
    fake_db['users'].append(user_data)
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
async def login(username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = await create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = await create_refresh_token(data={"sub": user.username}, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    user = next((u for u in fake_db['users'] if u['email'] == request.email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"message": "Password reset email sent"}  # In practice, send an actual email.

@app.post("/change-password")
async def change_password(username: str, password_data: PasswordChange):
    user = await authenticate_user(username, password_data.old_password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid old password")
    user.hashed_password = get_password_hash(password_data.new_password)
    return {"message": "Password changed successfully"}

@app.post("/reset-password")
async def reset_password(email: str, new_password: str):
    user = next((u for u in fake_db['users'] if u['email'] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user['hashed_password'] = get_password_hash(new_password)
    return {"message": "Password reset successfully"}
