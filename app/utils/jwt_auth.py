from typing import Optional
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from app.schemas import TokenData

SECRET_KEY = "093nestinvestca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88efrank"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire, 'accessed_time': str(datetime.now())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get('user_email')
        user_id = payload.get('user_id')
        role = payload.get('role')
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, user_email=user_email, role=role)
    except InvalidTokenError:
        raise credentials_exception

    return {
        'user_id': token_data.user_id,
        'user_email': token_data.user_email,
        'role': token_data.role
    }

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin access required'
        )
    return current_user
