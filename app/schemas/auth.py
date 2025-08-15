from pydantic import BaseModel


class TokenPair(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"


class RefreshRequest(BaseModel):
	refresh_token: str 