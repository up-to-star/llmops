from tortoise.models import Model
from tortoise import fields
import uuid


class ApiToolProvider(Model):
    """API工具供应商模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="供应商ID")
    account_id = fields.UUIDField(null=False, description="账号ID")
    name = fields.CharField(max_length=255, default="",
                            null=False, description="供应商名称")
    icon = fields.CharField(max_length=1024, default="",
                            null=False, description="供应商图标")
    description = fields.TextField(
        default="", null=False, description="供应商描述")
    openapi_schema = fields.TextField(
        default="", null=False, description="OpenAPI规范")
    headers = fields.JSONField(
        default="", null=False, description="请求头")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "api_tool_provider"


class ApiTool(Model):
    """API工具模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="工具ID")
    account_id = fields.UUIDField(null=False, description="账号ID")
    provider_id = fields.UUIDField(null=False, description="供应商ID")
    name = fields.CharField(max_length=255, default="",
                            null=False, description="工具名称")
    description = fields.TextField(
        default="", null=False, description="工具描述")
    url = fields.CharField(max_length=1024, default="",
                           null=False, description="工具URL")
    method = fields.CharField(max_length=255, default="",
                              null=False, description="工具方法")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "api_tool"
