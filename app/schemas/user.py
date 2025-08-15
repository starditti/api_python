from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	email: EmailStr

	class Config:
		from_attributes = True


class UserCreate(UserBase):
	password: str


class UserRead(UserBase):
	id: int
	is_active: bool
	created_at: datetime 