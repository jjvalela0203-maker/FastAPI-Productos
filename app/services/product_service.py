from fastapi import HTTPException, UploadFile
from sqlmodel import Session
from app.models.products import Product
from app.schemas.product_schema import Productcreate, Productupdated
import boto3
import os


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

def subir_imagen_producto_service(producto_id: int, file: UploadFile, session: Session):
    # 1. Verificamos que el producto exista antes de subir nada a AWS
    producto = session.get(Product, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # 2. Subimos el archivo a S3
    file_name = f"productos/{producto_id}_{file.filename}"
    try:
        s3_client.upload_fileobj(
            file.file, 
            BUCKET_NAME, 
            file_name,
            ExtraArgs={"ContentType": file.content_type}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir imagen a AWS: {str(e)}")
    
    # 3. Construimos la URL pública y actualizamos la base de datos
    url_imagen = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    producto.url = url_imagen
    
    session.add(producto)
    session.commit()
    session.refresh(producto)
    
    return producto

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