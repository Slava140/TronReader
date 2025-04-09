import pytest

from src.config import settings
from src.database import SessionLocal, Base, engine
from src.models import RequestM


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

@pytest.fixture
def tron_address():
    return 'TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ'


@pytest.fixture(scope='function')
def add_requests(db_session, tron_address):
    for _ in range(4):
        db_session.add(RequestM(tron_address=tron_address))
        db_session.commit()


@pytest.fixture(scope='function')
def empty_requests(db_session):
    all_requests = db_session.query(RequestM)
    for r in all_requests:
        db_session.delete(r)
        db_session.commit()