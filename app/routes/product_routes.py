from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.product_schema import Productcreate, Productupdated
from app.models.products import Product
from app.services import product_service

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=Product)
def create_product(product: Productcreate, session: Session = Depends(get_session)):
    return product_service.create_product(product, session)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    return product_service.get_product_by_id(product_id, session)

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_data: Productupdated, session: Session = Depends(get_session)):
    return product_service.update_product(product_id, product_data, session)

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    return product_service.delete_product(product_id, session)