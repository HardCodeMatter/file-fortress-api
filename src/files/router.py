from datetime import datetime

from fastapi import APIRouter, UploadFile, File as FastAPIFile, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .schemas import FileRead
from .service import FileService
from auth.utils import get_current_active_user
from auth.models import User


router: APIRouter = APIRouter(
    prefix='/files',
    tags=['Files']
)


@router.post('/upload')
async def upload_file_to_aws(
    file: UploadFile = FastAPIFile(...),
    access_code: str = Body(None),
    expiration_date: datetime = Body(None),
    is_public: bool = Body(False),
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> FileRead:
    return await FileService(session).upload_file(
        access_code,
        expiration_date,
        is_public,
        upload_file=file,
        current_user=current_user,
    )

@router.get('/download')
async def download_file(
    storage_key: str = None,
    filename: str | None = None,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    return await FileService(session).download_file(
        storage_key=storage_key,
        filename=filename,
    )
