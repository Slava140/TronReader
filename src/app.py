from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.database import get_db

app = FastAPI()

@app.get('/')
def ok(session: Session = Depends(get_db)):
    print(session.autoflush)
    return 'ok'
