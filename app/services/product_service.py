from fastapi import HTTPException
from sqlmodel import Session
from app.models.products import Product
from app.schemas.product_schema import Productcreate, Productupdated

def create_product(product: Productcreate, session: Session):
    
    if product.cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa")
    
    if product.precio < 0:
        raise HTTPException(status_code=400, detail="El precio no puede ser negativo")
    
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def get_product_by_id(product_id: int, session: Session):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

def update_product(product_id: int, product_data: Productupdated, session: Session):
    db_product = get_product_by_id(product_id, session)
    
    if product_data.cantidad is not None and product_data.cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa")
    
    if product_data.precio is not None and product_data.precio < 0:
        raise HTTPException(status_code=400, detail="El precio no puede ser negativo")
    
    new_data = product_data.model_dump(exclude_unset=True)
    
    for key, value in new_data.items():
        setattr(db_product, key, value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def delete_product(product_id: int, session: Session):
    db_product = get_product_by_id(product_id, session)
    session.delete(db_product)
    session.commit()
    return {"mensaje": "Producto eliminado exitosamente"}