from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict, model_validator
from internal.entity.dataset_entity import ProcessType, DEFAULT_PROCESS_RULE
from uuid import UUID
from internal.model import Document
from internal.exception import ValidationException


class CreateDocumentRequest(BaseModel):
    """创建文档请求"""
    upload_file_ids: list[UUID] = Field(description="上传文件ID列表")
    process_type: ProcessType = Field(
        default=ProcessType.AUTOMATIC, description="处理类型")
    rule: dict = Field(default_factory=dict, description="规则")

    @field_validator("upload_file_ids")
    @classmethod
    def validate_upload_file_ids(cls, v: list[UUID]) -> list[UUID]:
        """验证上传文件ID列表"""
        if len(v) == 0:
            raise ValidationException("上传文件ID列表不能为空")
        if len(v) > 10:
            raise ValidationException("上传文件ID列表最多只能包含10个文件")

        return list(set(v))

    @model_validator(mode='after')
    def validate_rule(self) -> 'CreateDocumentRequest':
        """验证规则"""
        if self.process_type == ProcessType.AUTOMATIC:
            self.rule = DEFAULT_PROCESS_RULE["rule"]
        else:
            if not isinstance(self.rule, dict) or len(self.rule) == 0:
                raise ValidationException("自定义处理类型规则不能为空且必须是字典类型")
            if "pre_process_rules" not in self.rule or not isinstance(self.rule["pre_process_rules"], list):
                raise ValidationException(
                    "自定义处理类型规则必须包含pre_process_rules字段且必须是列表类型")
            unique_pre_process_rules = {}
            for pre_process_rule in self.rule["pre_process_rules"]:
                if "id" not in pre_process_rule or pre_process_rule["id"] not in ["remove_extra_space", "remove_url_and_email"]:
                    raise ValidationException(
                        "自定义处理类型规则pre_process_rules字段必须包含id字段且必须是remove_extra_space或remove_url_and_email")
                if "enabled" not in pre_process_rule or not isinstance(pre_process_rule["enabled"], bool):
                    raise ValidationException(
                        "自定义处理类型规则pre_process_rules字段必须包含enabled字段且必须是布尔类型")
                unique_pre_process_rules[pre_process_rule["id"]] = {
                    "id": pre_process_rule["id"],
                    "enabled": pre_process_rule["enabled"],
                }
            if len(unique_pre_process_rules) != 2:
                raise ValidationException(
                    "自定义处理类型规则pre_process_rules字段必须包含不同的id，分别是remove_extra_space和remove_url_and_email")
            self.rule["pre_process_rules"] = list(unique_pre_process_rules.values())
            if "segment" not in self.rule or not isinstance(self.rule["segment"], dict):
                raise ValidationException(
                    "自定义处理类型规则必须包含segment字段且必须是字典类型")
            if "separators" not in self.rule["segment"] or not isinstance(self.rule["segment"]["separators"], list):
                raise ValidationException(
                    "自定义处理类型规则segment字段必须包含separators字段且必须是列表类型")
            for separator in self.rule["segment"]["separators"]:
                if not isinstance(separator, str):
                    raise ValidationException(
                        "自定义处理类型规则segment字段中的separators字段必须包含字符串")
            if len(self.rule["segment"]["separators"]) == 0:
                raise ValidationException(
                    "自定义处理类型规则segment字段中的separators字段不能为空")
            if "chunk_size" not in self.rule["segment"] or not isinstance(self.rule["segment"]["chunk_size"], int):
                raise ValidationException(
                    "自定义处理类型规则segment字段必须包含chunk_size字段且必须是整数")
            if "chunk_overlap" not in self.rule["segment"] or not isinstance(self.rule["segment"]["chunk_overlap"], int):
                raise ValidationException(
                    "自定义处理类型规则segment字段必须包含chunk_overlap字段且必须是整数")
            if self.rule["segment"]["chunk_size"] < 100 or self.rule["segment"]["chunk_size"] > 1000:
                raise ValidationException(
                    "自定义处理类型规则segment字段中的chunk_size和chunk_overlap字段必须大于等于100且小于等于1000")
            if not (0 <= self.rule["segment"]["chunk_overlap"] <= self.rule["segment"]["chunk_size"] * 0.5):
                raise ValidationException(
                    "自定义处理类型规则segment字段中的chunk_overlap字段必须小于等于chunk_size的50%")
            self.rule = {
                "pre_process_rules": self.rule["pre_process_rules"],
                "segment": {
                    "separators": self.rule["segment"]["separators"],
                    "chunk_size": self.rule["segment"]["chunk_size"],
                    "chunk_overlap": self.rule["segment"]["chunk_overlap"],
                }
            }
        return self


class CreateDocumentResponse(BaseModel):
    """创建文档响应"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    documents: list[Document] = Field(default_factory=list, description="文档列表")
    batch: str = Field(default="", description="批次ID")

    @field_serializer('documents')
    @classmethod
    def serialize_documents(cls, documents: list[Document]) -> list[dict]:
        """序列化Document对象为字典"""
        return [
            {
                'id': str(doc.id),
                'name': doc.name,
                'status': doc.status,
                'created_at': int(doc.created_at.timestamp()),
            }
            for doc in documents
        ]
