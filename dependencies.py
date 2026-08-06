from models import db
from sqlalchemy.orm import sessionmaker

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # pois session é um generator, retorna o valor mas n encerra
    finally: # executa independente se o try deu certo ou errado
        session.close() # fecha quando encerrar função