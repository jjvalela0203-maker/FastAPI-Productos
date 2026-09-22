from typing import Optional
from pydantic import BaseModel

class Productcreate(BaseModel):
    nombre_del_producto: str
    precio: float
    cantidad: int
    categoria: str

class Productupdated(BaseModel):
    nombre_del_producto: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    categoria: Optional[str] = None