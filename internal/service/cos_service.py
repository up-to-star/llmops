from datetime import datetime
from injector import inject
from dataclasses import dataclass
from qcloud_cos import CosS3Client, CosConfig
import os
import dotenv
from fastapi import UploadFile
from internal.entity.upload_file_entity import ALLOWED_IMAGE_EXTENSIONS, ALLOWED_FILE_EXTENSIONS
from internal.exception import FailException
import uuid
from internal.model import UploadFile as UploadFileModel
from .upload_file_service import UploadFileService
import hashlib
from internal.lib.logger import get_module_logger, log_function_call

logger = get_module_logger(__name__)

dotenv.load_dotenv()


@inject
class CosService:
    '''腾讯云COS对象存储服务类'''

    def __init__(self, upload_file_service: UploadFileService):
        self.upload_file_service = upload_file_service
        self.client = self._get_client()
        self.bucket = self._get_bucket()

    @classmethod
    def _get_client(cls) -> CosS3Client:
        '''获取COS客户端'''
        config = CosConfig(
            Region=os.getenv("COS_REGION"),
            SecretId=os.getenv("COS_SECRET_ID"),
            SecretKey=os.getenv("COS_SECRET_KEY"),
            Token=None,
            Scheme=os.getenv("COS_SCHEME", "https"),
        )
        return CosS3Client(config)

    @classmethod
    def _get_bucket(cls) -> str:
        '''获取COS存储桶名称'''
        return os.getenv("COS_BUCKET")

    @log_function_call()
    async def upload_file(self, file: UploadFile, only_image: bool = False) -> UploadFileModel:
        '''上传文件到COS'''
        account_id = '550e8400-e29b-41d4-a716-446655440000'
        filename = file.filename
        extension = filename.rsplit(".", 1)[-1] if "." in filename else ""
        if extension.lower() not in (ALLOWED_IMAGE_EXTENSIONS + ALLOWED_FILE_EXTENSIONS):
            raise FailException(
                f"{filename}文件类型不支持，仅支持{ALLOWED_IMAGE_EXTENSIONS + ALLOWED_FILE_EXTENSIONS}")
        elif only_image and extension.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise FailException(
                f"{filename}图片类型不支持，仅支持{ALLOWED_IMAGE_EXTENSIONS}")
        random_filename = str(uuid.uuid4()) + "." + extension
        now = datetime.now()
        upload_filename = f"{now.year}/{now.month:02d}/{now.day:02d}/{random_filename}"
        file_content = file.file.read()
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Body=file_content,
                Key=upload_filename,
            )
            logger.info(f"文件 {filename} 上传到COS成功，路径为 {upload_filename}")
        except Exception as e:
            raise FailException(f"上传文件到COS失败: {e}, 请稍后重试")

        upload_file = await self.upload_file_service.create_upload_file(
            account_id=account_id,
            name=upload_filename,
            key=upload_filename,
            size=len(file_content),
            extension=extension,
            mime_type=file.content_type,
            hash=hashlib.sha3_256(file_content).hexdigest())
        return upload_file

    async def download_file(self, key: str, target_file_path: str):
        '''从COS下载文件'''
        try:
            response = self.client.download_file(
                Bucket=self.bucket,
                Key=key,
                DestFilePath=target_file_path,
            )
        except Exception as e:
            raise FailException(f"从COS下载文件失败: {e}, 请稍后重试")

    async def get_file_url(self, key: str) -> str:
        '''获取COS文件URL'''
        cos_domain = os.getenv("COS_DOMAIN")
        if not cos_domain:
            schema = os.getenv("COS_SCHEME", "https")
            region = os.getenv("COS_REGION")
            cos_domain = f"{schema}://{self.bucket}.cos.{region}.myqcloud.com"
        return f"{cos_domain}/{key}"
