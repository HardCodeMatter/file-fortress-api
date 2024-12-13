from datetime import datetime
from io import BytesIO

from fastapi import UploadFile, status, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, Select, desc, asc

from .schemas import FileQueryParams, OrderBy
from .utils import generate_hash
from .models import File
from aws.client import s3_client
from auth.models import User
from service import BaseService


class FileService(BaseService):
    async def upload_file(
        self,
        access_code: str,
        expiration_date: datetime,
        is_public: bool,
        upload_file: UploadFile,
        current_user: User
    ) -> File:
        try:
            storage_key: str = generate_hash()

            stmt: Select[File] = select(File).filter(File.storage_key == storage_key)
            file: File = (
                await self.session.execute(stmt)
            ).scalars().first()

            if file:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'File with this storage key is already exist.',
                )

            custom_expiration_date: datetime = expiration_date.replace(tzinfo=None) if expiration_date else None

            file = File(
                name=upload_file.filename,
                size=upload_file.size,
                content_type=upload_file.content_type,
                storage_key=storage_key,
                uploader_id=current_user.id,
                access_code=access_code,
                expiration_date=custom_expiration_date,
                is_public=is_public
            )

            await s3_client.upload_file(upload_file, storage_key)

            self.session.add(file)
            await self.session.commit()
            await self.session.refresh(file)

            return file
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def download_file(self, storage_key: str, filename: str | None):
        if not storage_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Storage key is unknown.',
            )

        try:
            stmt: Select[File] = select(File).filter(File.storage_key == storage_key)
            file: File = (
                await self.session.execute(stmt)
            ).scalars().first()

            if not file:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'File with this storage key is not found.',
                )

            file_content = await s3_client.download_file(storage_key)
            custom_filename: str = f'{filename}.{file.content_type.split("/")[1]}'

            print(file.is_public, file.access_code)

            return StreamingResponse(
                BytesIO(file_content),
                media_type='application/force-download',
                headers={'Content-Disposition': f'attachment; filename={custom_filename if filename is not None else file.name}'}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_file_by_id(self, id: str) -> File:
        stmt: Select[File] = select(File).filter(File.id == id)
        file: File = (
            await self.session.execute(stmt)
        ).scalars().first()

        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'File with ID \'{id}\' was not found.',
            )

        return file

    async def get_files_by_name(self, params: FileQueryParams, name: str, skip: int = 0, limit: int = 10) -> list[File]:
        order_by_mapping = {
            OrderBy.name: File.name,
            OrderBy.size: File.size,
            OrderBy.is_public: File.is_public,
            OrderBy.created_at: File.created_at
        }

        order_by_column = order_by_mapping[params.order_by]

        if order_by_column is None:
            raise HTTPException(
                status_code=400,
                detail=f'Invalid order_by field: {order_by_column}.',
            )
        print('\n\nORDER TO SORT!!!!!!!!: ', bool(params.descending), isinstance(params.descending, bool), '\n')

        stmt: Select[File] = (
            select(File)
            .filter(File.name.icontains(name))
            .order_by(desc(order_by_column) if bool(params.descending) else asc(order_by_column))
            .offset(skip)
            .limit(limit)
        )
        files: list[File] = (
            await self.session.execute(stmt)
        ).scalars().all()

        if not files:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Files were not found.',
            )

        return files

    async def get_files_by_current_user(self, current_user: User) -> list[File]:
        stmt: Select[list[File]] = (
            select(File)
            .filter(File.uploader_id == current_user.id)
            .order_by(File.created_at.desc())
        )
        files: list[File] = (
            await self.session.execute(stmt)
        ).scalars().all()

        if not files:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Files were not found.',
            )

        return files
