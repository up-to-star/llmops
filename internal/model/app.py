from tortoise.models import Model
from tortoise import fields
import uuid

class App(Model):
    """AI应用基础模型类"""
    id = fields.UUIDField(
        pk=True, default_factory=uuid.uuid4, description="应用ID")
    account_id = fields.UUIDField(nullable=False, description="账号ID")
    name = fields.CharField(max_length=255, default="",
                            nullable=False, description="应用名称")
    description = fields.TextField(
        default="", nullable=False, description="应用描述")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")
    # is_active = fields.BooleanField(default=True, description="是否激活")

    class Meta:
        table = "apps"
        indexes = ["account_id"]