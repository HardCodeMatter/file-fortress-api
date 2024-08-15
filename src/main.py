import uvicorn
from fastapi import FastAPI

from config import settings
from auth.router import router as auth_router

app: FastAPI = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)

app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
