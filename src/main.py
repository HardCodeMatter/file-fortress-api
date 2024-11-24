import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from auth.router import router as auth_router
from files.service import router as file_router

app: FastAPI = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)

origins = [
    'http://127.0.0.1:5500',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(file_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
