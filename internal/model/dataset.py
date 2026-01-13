from tortoise.models import Model
from tortoise import fields
import uuid


class Dataset(Model):
    """数据集基础模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="数据集ID")
    account_id = fields.UUIDField(null=False, description="账号ID")
    name = fields.CharField(max_length=255, default="", description="数据集名称")
    icon = fields.CharField(max_length=1024, default="", description="数据集图标")
    description = fields.TextField(default="", description="数据集描述")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")


class Document(Model):
    """文档基础模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="文档ID")
    account_id = fields.UUIDField(null=False, description="账号ID")
    dataset_id = fields.UUIDField(null=False, description="数据集ID")
    upload_file_id = fields.UUIDField(null=False, description="上传文件ID")
    process_rule_id = fields.UUIDField(null=False, description="处理规则ID")
    batch = fields.CharField(max_length=255, default="", description="批次")
    name = fields.CharField(max_length=255, default="", description="文档名称")
    position = fields.IntField(null=False, default=1, description="文档位置")
    character_count = fields.IntField(null=False, default=0, description="字符数")
    token_count = fields.IntField(null=False, default=0, description="Token数")
    process_started_at = fields.DatetimeField(null=True, description="处理开始时间")
    parsing_completed_at = fields.DatetimeField(
        null=True, description="解析完成时间")
    splitting_completed_at = fields.DatetimeField(
        null=True, description="拆分完成时间")
    indexing_completed_at = fields.DatetimeField(
        null=True, description="索引完成时间")
    completed_at = fields.DatetimeField(null=True, description="完成时间")
    stopped_at = fields.DatetimeField(null=True, description="停止时间")
    error = fields.TextField(default="", description="错误信息")
    enabled = fields.BooleanField(
        null=False, default=False, description="是否启用")
    disabled_at = fields.DatetimeField(null=True, description="禁用时间")
    status = fields.CharField(
        max_length=255, default="waiting", description="状态")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")


class Segment(Model):
    """段落基础模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="段落ID")
    account_id = fields.UUIDField(null=False, description="账号ID")
    document_id = fields.UUIDField(null=False, description="文档ID")
    node_id = fields.UUIDField(null=False, description="节点ID")
    position = fields.IntField(null=False, default=1, description="段落位置")
    content = fields.TextField(default="", description="段落内容")
    character_count = fields.IntField(null=False, default=0, description="字符数")
    token_count = fields.IntField(null=False, default=0, description="Token数")
    keywords = fields.JSONField(
        null=False, default_factory=list, description="关键词")
    hash = fields.CharField(max_length=255, default="", description="哈希值")
    hit_count = fields.IntField(null=False, default=0, description="命中次数")
    enabled = fields.BooleanField(
        null=False, default=False, description="是否启用")
    disabled_at = fields.DatetimeField(null=True, description="禁用时间")
    process_started_at = fields.DatetimeField(null=True, description="处理开始时间")
    indexing_completed_at = fields.DatetimeField(
        null=True, description="索引完成时间")
    completed_at = fields.DatetimeField(null=True, description="完成时间")
    stopped_at = fields.DatetimeField(null=True, description="停止时间")
    error = fields.TextField(default="", description="错误信息")
    status = fields.CharField(
        max_length=255, null=False, default="waiting", description="状态")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")


class KeywordTable(Model):
    """关键词表基础模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="关键词ID")
    dataset_id = fields.UUIDField(null=False, description="数据集ID")
    keyword_table = fields.JSONField(
        null=False, default_factory=list, description="关键词表")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")


class DatasetQuery(Model):
    """数据集查询基础模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="查询ID")
    dataset_id = fields.UUIDField(null=False, description="数据集ID")
    query = fields.TextField(default="", description="查询内容")
    source = fields.CharField(
        max_length=255, default="HitTesting", description="查询来源")
    source_app_id = fields.UUIDField(null=False, description="查询来源应用ID")
    created_by = fields.UUIDField(null=False, description="创建人ID")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")


class ProcessRule(Model):
    """处理规则基础模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="规则ID")
    account_id = fields.UUIDField(null=False, description="账号ID")
    dataset_id = fields.UUIDField(null=False, description="数据集ID")
    mode = fields.CharField(max_length=255, null=False, default="automic", description="模式")
    rule = fields.JSONField(null=False, default_factory=list, description="规则")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")


class AppDatasetJoin(Model):
    """应用数据集关联基础模型类"""
    id = fields.UUIDField(
        primary_key=True, default_factory=uuid.uuid4, description="关联ID")
    app_id = fields.UUIDField(null=False, description="应用ID")
    dataset_id = fields.UUIDField(null=False, description="数据集ID")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_at = fields.DatetimeField(auto_now=True, description="更新时间")
