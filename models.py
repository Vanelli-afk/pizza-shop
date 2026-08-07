from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

# cria a conexao do seu banco
db = create_engine("sqlite:///database/data.db")

# cria a base do banco de dados
Base = declarative_base()

# cria as classes/tabelas do banco
# Usuarios
# Pedidos
# ItensPedido

class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    activated = Column("activated", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, activated=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.activated = activated
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"

    # ORDER_STATUS = (
    #     #(chave, valor)
    #     ("PENDING", "PENDING"),
    #     ("CANCELED", "CANCELED"),
    #     ("COMPLETED", "COMPLETED")
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    user = Column("user", ForeignKey("users.id"))
    price = Column("price", Float, nullable=False)
    # itens

    def __init__(self, user, status="PENDING", price=0):
        self.status = status
        self.user = user
        self.price = price

class OrderedItem(Base):
    __tablename__ = "ordered_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    taste = Column("taste", String)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, quantity, taste, size, unit_price, order):
        self.quantity = quantity
        self.taste = taste
        self.size = size
        self.unit_price = unit_price
        self.order = order

# executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)
"""
Atraves do alambic:
Para qualquer mudança ou criação de banco de dados
    Sempre tem que fazer a migração ('commit' do db)
            "alambic revision --autogenerate -m 'mensagem'"
    E depois fazer o upgrade ('push' do db)
            "alambic upgrade head"
"""