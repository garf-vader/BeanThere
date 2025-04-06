# app/__init__.py
from fastapi import FastAPI
from app import crud

def create_app() -> FastAPI:
    app = FastAPI()

    # Include the router from crud.py
    app.include_router(crud.router)

    return app