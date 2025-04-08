import pytest

from src.config import settings
from src.database import SessionLocal, Base, engine


@pytest.fixture(scope="function", autouse=True)
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    assert settings.MODE == 'TEST'
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
