from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData, User

# Secret key and algorithm settings
SECRET_KEY = "YOUR_SECRET_KEY"  # Use a strong key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.repository.get_user_by_username(username)
        if not user:
            return None
        if not User.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.repository.get_user_by_username(token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
    async def get_current_active_user(self, current_user: User = Depends(get_current_user)):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user