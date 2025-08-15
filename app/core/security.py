from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
	return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return password_context.verify(plain_password, hashed_password)


def _create_token(*, data: dict[str, Any], expires_delta: timedelta, secret: str) -> str:
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + expires_delta
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, secret, algorithm=settings.ALGORITHM)
	return encoded_jwt


def create_access_token(subject: str | int, additional_claims: Optional[dict[str, Any]] = None) -> str:
	claims: dict[str, Any] = {"sub": str(subject)}
	if additional_claims:
		claims.update(additional_claims)
	return _create_token(
		data=claims,
		expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
		secret=settings.SECRET_KEY,
	)


def create_refresh_token(subject: str | int) -> str:
	claims: dict[str, Any] = {"sub": str(subject), "type": "refresh"}
	return _create_token(
		data=claims,
		expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
		secret=settings.REFRESH_SECRET_KEY,
	)


def decode_access_token(token: str) -> dict[str, Any]:
	return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def decode_refresh_token(token: str) -> dict[str, Any]:
	payload = jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
	if payload.get("type") != "refresh":
		raise JWTError("Invalid token type")
	return payload 