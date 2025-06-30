from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Importamos nuestra configuración centralizada
from app.core.config import settings

# Usamos la URL de la base de datos desde la configuración
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# El resto del archivo permanece igual...
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()