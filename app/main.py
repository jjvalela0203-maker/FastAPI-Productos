from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routes import product_routes

app = FastAPI(title="API de Inventario")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(product_routes.router)