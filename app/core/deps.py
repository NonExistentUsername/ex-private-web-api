from typing import Generator, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
import core.config as config
from core.auth import oauth2_scheme
from models.user import User
from jose import jwt, JWTError

from app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id: Optional[int] = None
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        else:
            user_id = int(user_id)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
