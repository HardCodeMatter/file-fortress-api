from contextlib import asynccontextmanager

from fastapi import UploadFile
from aiobotocore.session import get_session
import aiobotocore

from config import settings


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
        bucket_region: str,
    ) -> None:
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
        }
        self.bucket_name = bucket_name
        self.bucket_region = bucket_region
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    async def upload_file(self, file: UploadFile, storage_key: str) -> None:
        async with self.get_client() as client:
            file_content = await file.read()

            await client.put_object(
                Bucket=self.bucket_name,
                Key=storage_key,
                Body=file_content,
                ContentType=file.content_type,
            )

            return {
                'file_url': f'https://s3.{self.bucket_region}.amazonaws.com/{self.bucket_name}/{storage_key}',
            }

    async def download_file(self, storage_key: str):
        async with self.get_client() as client:
            response = await client.get_object(
                Bucket=self.bucket_name,
                Key=storage_key,
            )

            async with response['Body'] as stream:
                return await stream.read()


s3_client: S3Client = S3Client(
    access_key=settings.AWS_ACCESS_KEY,
    secret_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.AWS_S3_ENDPOINT,
    bucket_name=settings.AWS_BUCKET_NAME,
    bucket_region=settings.AWS_BUCKET_REGION,
)
