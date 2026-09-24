from sqlalchemy import create_engine
from sqlmodel import Session
import os

Database_URL = os.getenv("DATABASE_URL")

if not Database_URL:
    raise ValueError("Falta la variable de entorno DATABASE_URL")

engine = create_engine(Database_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session