# API FastAPI con JWT (Access + Refresh) y MySQL

## Requisitos
- Python 3.10+
- MySQL Server (crea una BD, ej. `fastapi_db`)

## Configuración
1. Crea un entorno virtual e instala dependencias:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. Crea un archivo `.env` en `api/` (mismo nivel que `requirements.txt`) con valores como:
   ```env
   APP_NAME=FastAPI JWT API
   API_PREFIX=/api
   SECRET_KEY=tu-secret
   REFRESH_SECRET_KEY=tu-refresh-secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_MINUTES=10080
   DATABASE_URL=mysql+pymysql://user:password@localhost:3306/fastapi_db
   ```

## Inicialización de DB
Las tablas se crean automáticamente al iniciar la app (SQLAlchemy `Base.metadata.create_all`).
Asegúrate de que la BD existe y las credenciales son correctas.

## Ejecutar servidor
Desde el directorio `api/`:
```bash
PYTHONPATH=$(pwd) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- Público:
  - `GET /api/public/ping`
- Auth:
  - `POST /api/auth/register` (body JSON: `{ "email": "a@b.com", "password": "pwd" }`)
  - `POST /api/auth/login` (form `application/x-www-form-urlencoded`: `username`, `password`)
  - `POST /api/auth/refresh` (body JSON: `{ "refresh_token": "..." }`)
- Privado (requiere `Authorization: Bearer <access_token>`):
  - `GET /api/private/me`

## Notas
- El `tokenUrl` del flujo OAuth2 es `/api/auth/login`.
- El `refresh_token` se verifica con una clave diferente a la del access token. 