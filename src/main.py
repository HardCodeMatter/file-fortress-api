import uvicorn
from fastapi import FastAPI

from config import settings


app: FastAPI = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
