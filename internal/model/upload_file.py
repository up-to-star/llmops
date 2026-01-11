
import uuid
from tortoise import fields
from tortoise.models import Model


class UploadFile(Model):
    id = fields.UUIDField(pk=True, description="文件上传后的ID",
                          default_factory=uuid.uuid4)
    account_id = fields.UUIDField(description="文件上传后的账户ID",
                                  default_factory=uuid.uuid4)
    name = fields.CharField(max_length=255, description="文件名称", default="")
    key = fields.CharField(max_length=500, description="文件在COS中的键", default="")
    size = fields.IntField(description="文件大小")
    extension = fields.CharField(max_length=50, description="文件扩展名", default="")
    mime_type = fields.CharField(max_length=100, description="文件MIME类型", default="")
    hash = fields.CharField(max_length=64, description="文件哈希值", default="")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")
    create_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
