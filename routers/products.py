from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["Products"],
                   responses={404: {"message": "No encontrado"}})

products_list = ["Producto 1", "Producto 2", "Producto 3"]

@router.get("/")
async def products():
    return products_list
            

@router.get("/{id}")
async def product(id: int):
    return products_list[id]