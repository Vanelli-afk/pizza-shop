from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Order
from dependencies import get_session
from schemas import OrderSchema

# dominio/order
order_router = APIRouter(prefix="/orders", tags=["orders"])

# funcao executada sempre que recebe uma requisicao get no endpoint /order/
# funcao assincrona -> nao interrompe sistema com muitas req simultaneas
@order_router.get("/")
async def orders():
    """
    This is the default order route. Every order route needs authentication.
    """
    return {"message": "You have accessed the orders route."}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order created succesfully. Order ID: {new_order.id}"}