from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session

# dominio/auth/
auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id):
    token = f"token{id}"
    return token

@auth_router.get("/")
async def home():
    """
    This is the default authentication route.
    """
    return {"message": "You have accessed the default authentication route.",
            "autenticado": False}

@auth_router.post("/create_profile")
async def create_profile(user_schema: UserSchema, session: Session = Depends(get_session)):
    # usa a session pra fazer a busca, filtrando por emails iguais
    # .all() e em seguida if len(user) > 0 é uma opcao
    # ou o first() pra pegar o primeiro
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        # ja tem usuario com esse email
        raise HTTPException(status_code=400, detail="There is already a user with this email.")
    else:
        crypt_password = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, crypt_password, user_schema.activated, user_schema.admin)
        session.add(new_user)
        session.commit() # salva alterações do banco de dados
        return {"message": f"User successfully registered {user_schema.email}"}
    # ainda tem que fechar a sessao do db

    # Token JWT (Jason Web Token)
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == login_schema.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    else: # cria token de usuario
        access_token = create_token(user.id)
        return {"access_token": access_token,
                "token_type": "Bearer"}
    
        # JWT Bearer
        # Headers = {"Access-Token": "Bearer token"}