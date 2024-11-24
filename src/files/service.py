from io import BytesIO

from fastapi import UploadFile, File, HTTPException, APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import generate_hash
from aws.client import s3_client
from service import BaseService
from database import get_async_session


class FileService(BaseService):
    async def upload_file(self, file: UploadFile) -> None:
        try:
            random_hash = generate_hash()

            return await s3_client.upload_file(file, random_hash)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def download_file(self, storage_key: str, filename: str):
        try:
            file_content = await s3_client.download_file(storage_key)

            return StreamingResponse(
                BytesIO(file_content),
                media_type='application/force-download',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


router = APIRouter(prefix='/files')
@router.post('/upload')
async def upload_file_to_aws(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    return await FileService(session).upload_file(
        file=file,
    )

@router.get('/download')
async def download_file(hash_key: str = None, filename: str = None, session: AsyncSession = Depends(get_async_session)):
    return await FileService(session).download_file(
        hash_key=hash_key,
        filename=filename,
    )
