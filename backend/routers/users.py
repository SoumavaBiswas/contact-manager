from fastapi import APIRouter, Depends, status, security, HTTPException
from schemas.users import UserResponse, UserCreate
from sqlalchemy.orm import Session
from services.users import UserService
from db.session import get_db

userApp = APIRouter()

@userApp.post('/api/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def add_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    
    return await UserService.add_user(db, user)
    
@userApp.post('/api/users/authenticate')
async def generate_token(form_data: security.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = await UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return await UserService.create_token(user)

@userApp.get('/api/users/me')
async def get_current_user(user: UserResponse = Depends(UserService.get_current_user)):
    return user