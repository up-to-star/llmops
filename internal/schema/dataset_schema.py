from pydantic import BaseModel, Field, HttpUrl
from pkg.paginator import PaginatorRequest


class CreateDatasetRequest(BaseModel):
    '''创建知识库请求'''
    name: str = Field(
        ...,
        max_length=100,
        json_schema_extra={
            "error_msg": {
                "missing": "name is required",
                "max_length": "name must be less than 100 characters"
            }
        }
    )
    icon: HttpUrl = Field(
        ...,
        json_schema_extra={
            "error_msg": {
                "missing": "icon is required",
                "type": "icon must be a valid url"
            }
        }
    )
    description: str = Field(
        max_length=2000, default="",
        json_schema_extra={
            "error_msg": {
                "max_length": "description must be less than 2000 characters"
            }
        }
    )


class GetDatasetResponse(BaseModel):
    '''获取知识库响应'''
    id: str = Field(default="")
    name: str = Field(default="")
    icon: HttpUrl = Field(default="")
    description: str = Field(default="")
    document_count: int = Field(default=0)
    character_count: int = Field(default=0)
    related_app_count: int = Field(default=0)
    hit_count: int = Field(default=0)
    created_at: int = Field(default=0)
    update_at: int = Field(default=0)


class UpdateDatasetRequest(BaseModel):
    '''创建知识库请求'''
    name: str = Field(
        ...,
        max_length=100,
        json_schema_extra={
            "error_msg": {
                "missing": "name is required",
                "max_length": "name must be less than 100 characters"
            }
        }
    )
    icon: HttpUrl = Field(
        ...,
        json_schema_extra={
            "error_msg": {
                "missing": "icon is required",
                "type": "icon must be a valid url"
            }
        }
    )
    description: str = Field(
        max_length=2000, default="",
        json_schema_extra={
            "error_msg": {
                "max_length": "description must be less than 2000 characters"
            }
        }
    )


class GetDatasetWithPageRequest(PaginatorRequest):
    search_word: str = Field(default="")

class GetDatasetWithPageResponse(BaseModel):
    '''获取知识库响应'''
    id: str = Field(default="")
    name: str = Field(default="")
    icon: HttpUrl = Field(default="")
    description: str = Field(default="")
    document_count: int = Field(default=0)
    character_count: int = Field(default=0)
    related_app_count: int = Field(default=0)
    created_at: int = Field(default=0)
    update_at: int = Field(default=0)