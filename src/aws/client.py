from contextlib import asynccontextmanager

from fastapi import UploadFile
from aiobotocore.session import get_session

from config import settings


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ) -> None:
        self.config = {
            'aws_access_key': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    async def upload_file(self, file: UploadFile) -> None:
        async with self.get_client() as client:
            async with open(file, 'rb') as file:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file.filename,
                    Body=file,
                )


s3_client: S3Client = S3Client(
    access_key=settings.AWS_ACCESS_KEY,
    secret_key=settings.AWS_SECRET_KEY,
    endpoint_url=settings.AWS_ENDPOINT_URL,
    bucket_name=settings.AWS_BUCKET_NAME,
)
