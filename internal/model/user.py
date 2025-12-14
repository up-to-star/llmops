from tortoise.models import Model
from tortoise import fields
from datetime import datetime


class User(Model):
    """用户模型"""
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    password = fields.CharField(max_length=100, description="密码")
    email = fields.CharField(max_length=100, unique=True, description="邮箱")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")
    is_active = fields.BooleanField(default=True, description="是否激活")

    class Meta:
        table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
