from injector import inject
from dataclasses import dataclass
from internal.schema import ValidateOpenApiSchemaRequest
from internal.service import ApiToolService
from pkg.response import HttpCode, Response


@inject
@dataclass
class ApiToolHandler:
    """自定义API工具处理类"""
    api_tool_service: ApiToolService

    async def validate_openapi_schema(self, req: ValidateOpenApiSchemaRequest):
        """验证OpenAPI schema是否符合要求"""
        await self.api_tool_service.parse_openapi_schema(req.openapi_schema)

        return Response(
            code=HttpCode.SUCCESS,
            message="OpenAPI schema验证成功",
            data={}
        )
