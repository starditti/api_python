from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
	create_access_token,
	create_refresh_token,
	get_password_hash,
	verify_password,
	decode_refresh_token,
)
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import TokenPair, RefreshRequest
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Annotated[Session, Depends(get_db)]):
	existing = db.execute(select(User).where(User.email == user_in.email)).scalar_one_or_none()
	if existing:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
	user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.post("/login", response_model=TokenPair)
def login(
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
	db: Annotated[Session, Depends(get_db)],
):
	user: User | None = db.execute(select(User).where(User.email == form_data.username)).scalar_one_or_none()
	if user is None or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
	access_token = create_access_token(user.id)
	refresh_token = create_refresh_token(user.id)
	return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(payload: RefreshRequest):
	try:
		claims = decode_refresh_token(payload.refresh_token)
		subject = claims.get("sub")
		new_access = create_access_token(subject)
		new_refresh = create_refresh_token(subject)
		return TokenPair(access_token=new_access, refresh_token=new_refresh)
	except Exception:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido") 