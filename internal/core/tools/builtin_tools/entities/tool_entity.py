from pydantic import BaseModel, Field
from typing import Optional, Any
from enum import Enum

class ToolParamType(str, Enum):
    """工具参数类型枚举类"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    SELECT = "select"

class ToolParam(BaseModel):
    """工具参数类"""
    name: str = Field(description="参数名称")
    label: str = Field(description="参数显示标签")
    type: ToolParamType = Field(description="参数类型")
    required: bool = Field(description="参数是否必填")
    default: Optional[Any] = Field(description="参数默认值")
    min: Optional[float] = Field(default=None, description="参数最小值")
    max: Optional[float] = Field(default=None, description="参数最大值")
    options: list[dict[str, Any]] = Field(default_factory=list, description="参数可选值")

class ToolEntity(BaseModel):
    """工具实体类, 映射的数据是 工具名.yaml文件中的数据"""
    name: str = Field(description="工具名称")
    label: str = Field(description="工具显示名称")
    description: str = Field(description="工具描述")
    params: list[ToolParam] = Field(default_factory=list, description="工具参数")