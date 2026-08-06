from fastapi import APIRouter, Depends
from models import User
from dependencies import get_session
from main import bcrypt_context

# dominio/auth/
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    This is the default authentication route.
    """
    return {"message": "You have accessed the default authentication route.",
            "autenticado": False}

@auth_router.post("/create_profile")
async def create_profile(email: str, password: str, name: str, session = Depends(get_session)):
    # usa a session pra fazer a busca, filtrando por emails iguais
    # .all() e em seguida if len(user) > 0 é uma opcao
    # ou o first() pra pegar o primeiro
    user = session.query(User).filter(User.email==email).first()
    if user:
        # ja tem usuario com esse email
        return {"message": "There is already a user with this email."}
    else:
        crypt_password = bcrypt_context.hash(password)
        new_user = User(name, email, crypt_password)
        session.add(new_user)
        session.commit() # salva alterações do banco de dados
        return {"message": "User successfully registered"}
    # ainda tem que fechar a sessao do db