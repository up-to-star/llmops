from pydantic import BaseModel, Field


class ValidateOpenApiSchemaRequest(BaseModel):
    """验证OpenAPI schema是否符合要求"""
    openapi_schema: str = Field(
        ...,
        description="OpenAPI schema字符串",
        max_length=2048,
        json_schema_extra={
            "error_msg": {
                "missing": "openapi_schema is required",
                "max_length": "openapi_schema must be less than 2048 characters"
            }
        }
    )