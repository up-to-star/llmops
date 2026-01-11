from pydantic import BaseModel, Field, field_validator
from internal.entity.upload_file_entity import ALLOWED_FILE_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS
from fastapi import UploadFile, HTTPException, File
import os
import uuid
import time


class UploadFileRequest(BaseModel):
    file: UploadFile

    @field_validator("file")
    @classmethod
    def validate_file(cls, v):
        if not v:
            raise HTTPException(status_code=400, detail="文件不能为空")
        max_size = 15 * 1024 * 1024
        if v.size > max_size:
            raise HTTPException(status_code=400, detail="文件大小不能超过15MB")
        ext = v.filename.split(".")[-1].lower()
        if ext not in ALLOWED_FILE_EXTENSIONS:
            alowed_str = "/".join(ALLOWED_FILE_EXTENSIONS)
            raise HTTPException(
                status_code=400, detail=f"文件类型不支持，仅支持{alowed_str}")
        return v


class UploadImageRequest(BaseModel):
    file: UploadFile

    @field_validator("file")
    @classmethod
    def validate_file(cls, v):
        if not v:
            raise HTTPException(status_code=400, detail="文件不能为空")
        max_size = 15 * 1024 * 1024
        if v.size > max_size:
            raise HTTPException(status_code=400, detail="文件大小不能超过15MB")
        ext = v.filename.split(".")[-1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            alowed_str = "/".join(ALLOWED_IMAGE_EXTENSIONS)
            raise HTTPException(
                status_code=400, detail=f"图片类型不支持，仅支持{alowed_str}")
        return v


class UploadFileResponse(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="文件上传后的ID")
    account_id: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="文件上传后的账户ID")
    name: str = Field(default="", description="文件名称")
    size: int = Field(description="文件大小")
    extension: str = Field(default="", description="文件扩展名")
    mime_type: str = Field(default="", description="文件MIME类型")
    create_at: int = Field(default_factory=lambda: int(
        time.time()), description="文件上传时间")
