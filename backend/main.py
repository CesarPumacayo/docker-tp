import os

import sentry_sdk
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import SessionLocal

# Inicializar Sentry ANTES de crear la app, usando el DSN desde una
# variable de entorno (se configura en Render como SENTRY_DSN).
sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        send_default_pii=True,
        traces_sample_rate=1.0,
    )

app = FastAPI()

# Orígenes permitidos para CORS. En Render, configurar la variable de
# entorno FRONTEND_URL con la URL pública del frontend en Vercel.
origenes_permitidos = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:5500",
]

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origenes_permitidos.extend(
        origen.strip() for origen in frontend_url.split(",")
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"mensaje": "Backend FastAPI funcionando"}


@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    db = SessionLocal()

    try:
        resultado = db.execute(
            text("SELECT id, nombre FROM usuarios WHERE id = :id"),
            {"id": usuario_id}
        ).mappings().first()

        if resultado is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "id": resultado["id"],
            "nombre": resultado["nombre"]
        }

    finally:
        db.close()


@app.get("/sentry-debug")
async def trigger_error():
    # Endpoint que rompe a propósito, para demostrar en el video
    # que Sentry captura el error en tiempo real.
    division_por_cero = 1 / 0
    return division_por_cero