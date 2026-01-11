from injector import inject
from dataclasses import dataclass
from internal.schema import UploadFileRequest, UploadFileResponse, UploadImageRequest
from internal.service import CosService
from pkg.response import Response


@inject
@dataclass
class UploadFileHandler:
    cos_service: CosService

    async def upload_file(self, request: UploadFileRequest):
        """上传文件"""
        upload_file = await self.cos_service.upload_file(request.file)
        return Response(
            message="文件上传成功",
            data=UploadFileResponse(
                id=upload_file.id,
                account_id=upload_file.account_id,
                name=upload_file.name,
                size=upload_file.size,
                ext=upload_file.extension,
                mime_type=upload_file.mime_type,
                create_at=int(upload_file.create_at.timestamp())
            )
        )

    async def upload_image(self, request: UploadImageRequest):
        upload_file = await self.cos_service.upload_file(request.file, True)
        image_url = await self.cos_service.get_file_url(upload_file.key)
        return Response(
            message="图片上传成功",
            data={
                "image_url": image_url
            }
        )
