from typing import Optional
from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    __tablename__ = "productos" 
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_del_producto: str = Field(index=True)
    precio: float
    cantidad: int
    categoria: str = Field(index=True)