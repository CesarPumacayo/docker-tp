import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import SessionLocal

app = FastAPI()

# Orígenes permitidos para CORS. En Render, configurar la variable de
# entorno FRONTEND_URL con la URL pública del frontend en Vercel
# (ej: https://docker-tp.vercel.app), separando varias con comas si hace falta.
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