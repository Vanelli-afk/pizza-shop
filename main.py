from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI() # precisa do app pras rotas funcionarem por isso ficam abaixo

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# "criar usando uvicorn e executar o main no terminal"
#  uvicorn main:app --reload

CryptContext