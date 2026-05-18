from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session

from app.core.config import settings
from app.models.base import Base
from app.models import Account, Category, Transaction

engine = create_engine(         #connection manager to the db (not query running)
    settings.DATABASE_URL,
    echo=settings.DEBUG     #SQLAlchemy prints SQL queries in terminal (SQL logs)
)

SessionLocal = sessionmaker( #database sessions
    autocommit=False,   #Changes are NOT saved automatically (manual commit)
    autoflush=False,    #Prevents automatic DB syncing unexpectedly
    bind=engine
)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()