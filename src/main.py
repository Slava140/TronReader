import uvicorn

from app import app
from src.config import settings

if __name__ == '__main__':
    uvicorn.run(app=app, host=settings.APP_HOST, port=settings.APP_PORT)