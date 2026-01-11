from injector import inject
from dataclasses import dataclass
from internal.model import UploadFile as UploadFileModel


@inject
@dataclass
class UploadFileService:
    '''上传文件记录服务'''

    async def create_upload_file(self, **kwargs) -> UploadFileModel:
        '''创建上传文件记录'''
        upload_file = UploadFileModel(**kwargs)
        await upload_file.save()
        return upload_file
