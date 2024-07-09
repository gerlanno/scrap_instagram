from ast import Set
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

# Criando a engine do SQLAlchemy que se conecta a um banco de dados SQLite chamado "results.db"
engine = sqlalchemy.create_engine("sqlite:///scrap_insta.db")
# Criando uma classe base para a definição das classes de mapeamento ORM
Base = declarative_base()
# Criando uma classe Session configurada para ser ligada à engine
Session = sessionmaker(bind=engine)
# Criando uma instância de sessão para interagir com o banco de dados
session = Session()


# Classe mapeada que representa uma tabela no banco de dados
class InstagramUser(Base):
    # Nome da tabela no banco de dados.
    __tablename__ = "instagram_scrap"
    # Colunas da tabela com seus respectivos tipos e propriedades.
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    url_perfil = Column(String(100))
    telefone = Column(String(20))
    website = Column(String(100))
    email = Column(String(100))


    def __repr__(self):
        return f"<instagram_scrap(id={self.id}, Username='{self.username}', url_perfil='{self.url_perfil}', telefone='{self.telefone}', website='{self.website}', email='{self.email}')>"


def inserir_dados(lista):
    # Inserir a lista com dados no banco de dados.
    if not lista:
        print("Nada a processar!")
    else:

        try:
            session.add_all(lista)
            session.commit()
            print("Dados inseridos com sucesso!")
        except Exception as e:
            print(f"Erro! {e}")


def inicializar_bd():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Erro! {e}")


