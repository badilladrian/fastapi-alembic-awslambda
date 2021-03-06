from typing import Generator
from sqlalchemy.orm import Session

from app.schemas import token as schemas
from app.models import users as models
from app.cruds import users as cruds


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.core.config import settings
from app.core.db.session import SessionLocal, SessionGlobal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_HOST}/login/access-token")


def get_db_local() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_db_global() -> Generator:
    try:
        db = SessionGlobal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db_local), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials",
        )
    user = cruds.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user),) -> models.User:
    if not cruds.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: models.User = Depends(get_current_user),) -> models.User:
    if not cruds.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return current_user
