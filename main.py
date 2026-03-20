from fastapi import FastAPI
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
