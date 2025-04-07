from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import settings

engine = create_engine(settings.database_url_psycopg)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

sql_utc_now = text("timezone('utc', now())")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()