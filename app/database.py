from sqlmodel import create_engine, Session
import os

Database_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1140918021@localhost:5432/Productos_DB")

engine = create_engine(Database_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session