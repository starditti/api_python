from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_ignore_empty=True)

	APP_NAME: str = Field(default='FastAPI JWT API')
	API_PREFIX: str = Field(default='/api')

	# JWT
	SECRET_KEY: str = Field(default='change-this-in-prod')
	REFRESH_SECRET_KEY: str = Field(default='change-this-refresh-in-prod')
	ALGORITHM: str = Field(default='HS256')
	ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15)
	REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 7)  # 7 días

	# Database (MySQL por defecto)
	DATABASE_URL: str = Field(
		default='mysql+pymysql://user:password@localhost:3306/fastapi_db'
	)


settings = Settings() 