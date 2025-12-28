from pydantic import BaseModel, Field, field_validator


class CategoryEntity(BaseModel):
    """分类实体"""
    category: str = Field(description="分类唯一标识符")
    name: str = Field(description="分类名称")
    icon: str = Field(description="分类图标")

    @field_validator("icon")
    def check_icon_extension(cls, value: str):
        """分类图标必须是字母数字"""
        if not value.endswith(".svg"):
            raise ValueError("icon must be a svg file")
        return value
