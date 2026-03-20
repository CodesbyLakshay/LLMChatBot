import jwt
from jwt.exceptions import PyJWTError
from fastapi import Depends, HTTPException , status
from datetime import datetime, timedelta , timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .config import settings
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from .database import get_async_session
from .models.user import User

pwd_context = PasswordHash.recommended()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRES_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return access_token

def verify_access_token(token: str , credentials_exception):
    try:
       payload =  jwt.decode(token , SECRET_KEY, algorithms=ALGORITHM)
       user_id : str = payload.get("user_id")
       if user_id is None:
         raise credentials_exception
       return int(user_id)
    except PyJWTError:
        raise credentials_exception

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_access_token(token, credentials_exception)
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    return user
