from fastapi import FastAPI
from app.routers import comentarios, proyectos, roles, tareas, usuarios
import os

app = FastAPI()

APP_NAME = os.getenv("APP_NAME", "gestion-proyectos-tareas-backend")


@app.get("/")
def root():
    return {
        "message": "API funcionando",
        "app_name": APP_NAME
    }


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)
app.include_router(comentarios.router)

#pepe
