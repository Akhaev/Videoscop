from minio import Minio
from minio.error import S3Error
from datetime import timedelta
from config import MinioConfig
from application import interfaces
from exceptions import AlreadyExistsFileError, NotFoundFileError


class FileStorage(interfaces.GetFileUploadLink, interfaces.GetFileUnloadLink):
    def __init__(self, client: Minio, config: MinioConfig) -> None:
        self.client = client
        self.config = config
        
    async def get_upload_link(self, file_type: interfaces.Tag.video | interfaces.Tag.heat_map, filename: str) -> str:
        try:
            self.client.stat_object(file_type, filename)
            raise AlreadyExistsFileError(filename)
        except S3Error as e:
            if e.code != "NoSuchKey":
                raise e
        
        url = self.client.presigned_put_object(
            file_type, filename, expires=timedelta(hours=self.config.expiration_days),
        )
        return url
    
    async def get_unload_link(self, file_type: interfaces.Tag.video | interfaces.Tag.heat_map, filename: str) -> str:
        try:
            self.client.stat_object(file_type, filename)
        except S3Error as e:
            if e.code == "NoSuchKey":
                raise NotFoundFileError(filename)
            raise e
        
        url = self.client.presigned_get_object(
            file_type, filename, expires=timedelta(hours=self.config.expiration_days),
        )
        return url
