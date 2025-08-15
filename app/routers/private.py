from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.db.models import User

router = APIRouter(prefix="/private", tags=["private"])


@router.get("/me")
def read_me(current_user: Annotated[User, Depends(get_current_user)]):
	return {"id": current_user.id, "email": current_user.email, "is_active": current_user.is_active} 