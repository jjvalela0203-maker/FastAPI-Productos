from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel

app = FastAPI()
class Producto(BaseModel):
    id: int
    nombre_del_producto: str
    precio: float
    cantidad: int
    categoria: str

productos = [
    {
        "id": 101,
        "nombre_del_producto": "Cafetera Expresso",
        "precio": 120.50,
        "cantidad": 15,
        "categoria": "Electrodomésticos"
    },
    {
        "id": 102,
        "nombre_del_producto": "Cafetera Expreso",
        "precio": 115.00,
        "cantidad": 8,
        "categoria": "Electrodomesticos" 
    },
    {
        "id": 103,
        "nombre_del_producto": "Máquina de Café Espresso",
        "precio": 150.99,
        "cantidad": 5,
        "categoria": "Electrodomésticos"
    },
    {
        "id": 104,
        "nombre_del_producto": "Cafetera expres",
        "precio": 89.90,
        "cantidad": 22,
        "categoria": "Cocina"
    },
    {
        "id": 105,
        "nombre_del_producto": "Nevera Samsung",
        "precio": 899.99,
        "cantidad": 3,
        "categoria": "Electrodomésticos"
    },
    {
        "id": 106,
        "nombre_del_producto": "Tablet Samsung Galaxy Tab S7",
        "precio": 499.99,
        "cantidad": 10,
        "categoria": "Electrónica"
    }
]

def limpiar_texto(texto:str):
    texto_limpio = texto.translate(str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU"))
    return texto_limpio.lower()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de productos",
            "version": "1.0.0",
            "total_productos": len(productos)}
    
@app.get("/productos")
def obtener_productos():
    return productos

@app.post("/productos")
def agregar_producto(producto: Producto):
    productos.append(producto)
    return {"mensaje": "Producto agregado exitosamente", "producto": producto}

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto_actualizado: Producto):
    for i, producto in enumerate(productos):
        if producto["id"] == producto_id:
            productos[i] = producto_actualizado
            return {"mensaje": "Producto actualizado exitosamente", "producto": producto_actualizado}
    return {"mensaje": "Producto no encontrado"}

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    for i, producto in enumerate(productos):
        if producto["id"] == producto_id:
            productos.pop(i)
            return {"mensaje": "Producto eliminado exitosamente"}
    return {"mensaje": "Producto no encontrado"}


@app.get("/buscar")
def buscar_productos(
    q: str = Query(..., description="Término a buscar"), 
    limite: int = Query(10, description="Cantidad máxima de resultados a mostrar")
):
    # Pasamos la búsqueda del usuario por la misma función limpiadora
    busqueda_limpia = limpiar_texto(q)
    resultado = []
    
    for producto in productos:
        nombre_limpio = limpiar_texto(producto["nombre_del_producto"])
        categoria_limpia = limpiar_texto(producto["categoria"])
        
        # Evaluamos si el texto está en el nombre O en la categoría
        if busqueda_limpia in nombre_limpio or busqueda_limpia in categoria_limpia:
            resultado.append(producto)
            
    if resultado:
        # resultado[:limite] recorta la lista hasta el número indicado
        return {
            "busqueda_original": q,
            "total_encontrados": len(resultado),
            "mostrando": min(len(resultado), limite),
            "coincidencias": resultado[:limite]
        }
        
    return {"mensaje": "No se encontró nada que contenga ese texto"}