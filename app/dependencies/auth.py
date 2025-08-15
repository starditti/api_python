from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.db.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
	token: Annotated[str, Depends(oauth2_scheme)],
	db: Annotated[Session, Depends(get_db)],
) -> User:
	try:
		payload = decode_access_token(token)
		user_id: str | None = payload.get("sub")
		if user_id is None:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
		user = db.get(User, int(user_id))
		if user is None or not user.is_active:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado o inactivo")
		return user
	except JWTError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido") 