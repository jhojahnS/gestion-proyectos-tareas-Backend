import os
from sqlmodel import SQLModel
from fastapi import FastAPI
from app.db.session import engine
from app.routers import comentarios, proyectos, roles, tareas, usuarios


app = FastAPI()

APP_NAME = os.getenv("APP_NAME", "gestion-proyectos-tareas-backend")


@app.on_event("startup")
def init_db():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    return {
        "message": "API funcionando",
        "app_name": APP_NAME,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(proyectos.router)
app.include_router(tareas.router)
app.include_router(comentarios.router)
