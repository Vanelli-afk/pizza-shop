from fastapi import APIRouter

# dominio/order
order_router = APIRouter(prefix="/order", tags=["order"])

# funcao executada sempre que recebe uma requisicao get no endpoint /order/
# funcao assincrona -> nao interrompe sistema com muitas req simultaneas
@order_router.get("/")
async def orders():
    """
    This is the default order route. Every order route needs authentication.
    """
    return {"message": "You have accessed the orders route."}