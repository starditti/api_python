from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine
from app.routers import auth as auth_router
from app.routers import public as public_router
from app.routers import private as private_router


def create_app() -> FastAPI:
	app = FastAPI(title=settings.APP_NAME)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	# Crear tablas
	Base.metadata.create_all(bind=engine)

	# Incluir routers
	app.include_router(auth_router.router, prefix=settings.API_PREFIX)
	app.include_router(public_router.router, prefix=settings.API_PREFIX)
	app.include_router(private_router.router, prefix=settings.API_PREFIX)

	@app.get("/")
	def root():
		return {"name": settings.APP_NAME}

	return app


app = create_app() 