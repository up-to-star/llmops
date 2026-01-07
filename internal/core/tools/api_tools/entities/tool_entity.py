from pydantic import BaseModel, Field


class ToolEntity(BaseModel):
    """工具实体"""
    id: str = Field(default="", description="API工具提供者对应的ID")
    name: str = Field(default="", description="工具名称")
    url: str = Field(default="", description="工具对应的URL")
    method: str = Field(default="get", description="工具对应的HTTP方法")
    description: str = Field(default="", description="工具的描述")
    headers: list[dict] = Field(default_factory=list, description="工具对应的HTTP头")
    parameters: list[dict] = Field(default_factory=list, description="工具对应的HTTP参数")
