from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserResponse
from models.Models import UserModel
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib import hash
from db.session import get_db
import jwt
from constants.const import JWT_SECRET

class UserService:
    @staticmethod
    async def add_user(db: Session, user: UserCreate) -> UserResponse:
        if await UserService.get_user_by_email(db, user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        new_user = UserModel(
            name=user.name,
            email=user.email,
            password=hash.bcrypt.hash(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    

    @staticmethod
    async def get_user(db: Session, user_id: int) -> UserResponse:
        return db.query(UserModel).filter(UserModel.id == user_id).first()
    
    @staticmethod
    async def get_user_by_email(db: Session, email: str):
        return db.query(UserModel).filter(UserModel.email == email).first()
    
    @staticmethod
    async def authenticate_user(db: Session, email: str, password: str):
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return user

    @staticmethod
    async def create_token(user: UserModel):
        user_obj = UserResponse(
            id=user.id,
            email=user.email,
            name=user.name
        )
        token = jwt.encode(user_obj.model_dump(), JWT_SECRET, algorithm="HS256")  
        return dict(access_token=token, token_type="bearer")     
    
    @staticmethod
    async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/users/authenticate")), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user = await UserService.get_user(db, payload.get("id"))
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return UserResponse.model_validate(user)
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")