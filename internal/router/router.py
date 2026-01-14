from fastapi import FastAPI, APIRouter, Depends
from internal.handle import AppHandler, BuiltinToolHandler, ApiToolHandler, UploadFileHandler, DatasetHandler
from injector import inject
from fastapi import Depends
from internal.schema import (CompletionRequest, ValidateOpenApiSchemaRequest,
                             CreateApiToolRequest, GetApiToolProvidersWithPageRequest, UpdateApiToolProviderRequest, CreateDatasetRequest, UpdateDatasetRequest, GetDatasetWithPageRequest)
import uuid
from internal.schema import UploadFileRequest, UploadImageRequest
from internal.utils.dependencies import get_redis


@inject
class DatasetRouter:
    dataset_handler: DatasetHandler

    def __init__(self, dataset_handler: DatasetHandler):
        self.dataset_handler = dataset_handler

    def get_router(self) -> APIRouter:
        """创建数据集路由实例"""
        router = APIRouter(prefix="/datasets")

        @router.post("")
        async def create_dataset(request: CreateDatasetRequest):
            return await self.dataset_handler.create_dataset(request)

        @router.get("/{dataset_id}")
        async def get_dataset(dataset_id: uuid.UUID):
            return await self.dataset_handler.get_dataset(dataset_id)

        @router.post("/{dataset_id}")
        async def update_dataset(dataset_id: uuid.UUID, request: UpdateDatasetRequest):
            return await self.dataset_handler.update_dataset(dataset_id, request)

        @router.get("")
        async def get_datasets_with_page(current_page: int = 1, page_size: int = 10, search: str = ""):
            return await self.dataset_handler.get_datasets_with_page(request=GetDatasetWithPageRequest(current_page=current_page, page_size=page_size, search=search))

        return router


@inject
class UploadFileRouter:
    """文件上传路由独立处理器"""
    upload_file_handler: UploadFileHandler

    def __init__(self, upload_file_handler: UploadFileHandler):
        self.upload_file_handler = upload_file_handler

    def get_router(self) -> APIRouter:
        """创建文件上传路由实例"""
        router = APIRouter(prefix="/upload-files")

        @router.post("/file")
        async def upload_file(request: UploadFileRequest = Depends()):
            return await self.upload_file_handler.upload_file(request)

        @router.post("/image")
        async def upload_image(request: UploadImageRequest = Depends()):
            return await self.upload_file_handler.upload_image(request)

        return router


@inject
class AppRouter:
    """应用相关路由独立处理器"""
    app_handler: AppHandler

    def __init__(self, app_handler: AppHandler):
        self.app_handler = app_handler

    def get_router(self) -> APIRouter:
        """创建应用路由实例"""
        router = APIRouter(prefix="/apps")

        @router.get("/ping")
        async def ping():
            return await self.app_handler.ping()

        @router.post("/{app_id}/debug")
        async def debug(request: CompletionRequest, app_id: uuid.UUID):
            return await self.app_handler.debug(request.query, app_id)

        @router.post("/deubg_redis/{key}/{value}")
        async def debug_redis_set(key: str, value: str, redis=Depends(get_redis)):
            res = await redis.set(key, value, ex=3600)
            return {"message": res}

        @router.get("/deubg_redis/{key}")
        async def debug_redis_get(key: str, redis=Depends(get_redis)):
            res = await redis.get(key)
            return {"message": res}

        @router.get("/test_db")
        async def test_db():
            return await self.app_handler.test_db()

        @router.post("")
        async def create_app():
            return await self.app_handler.create_app()

        @router.get("/{app_id}")
        async def get_app(app_id: uuid.UUID):
            return await self.app_handler.get_app(app_id)

        @router.put("/{app_id}")
        async def update_app(app_id: uuid.UUID):
            return await self.app_handler.update_app(app_id)

        @router.delete("/{app_id}")
        async def delete_app(app_id: uuid.UUID):
            return await self.app_handler.delete_app(app_id)

        return router


@inject
class BuiltinToolRouter:
    """内置工具路由独立处理器"""
    builtin_tool_handler: BuiltinToolHandler

    def __init__(self, builtin_tool_handler: BuiltinToolHandler):
        self.builtin_tool_handler = builtin_tool_handler

    def get_router(self) -> APIRouter:
        """创建内置工具路由实例"""
        router = APIRouter(prefix="/builtin-tools")

        @router.get("")
        async def get_builtin_tools():
            return await self.builtin_tool_handler.get_builtin_tools()

        @router.get("/categories")
        async def get_categories():
            return await self.builtin_tool_handler.get_categories()

        @router.get("/{provider_name}/icon")
        async def get_provider_icon(provider_name: str):
            return await self.builtin_tool_handler.get_provider_icon(provider_name)

        @router.get("/{provider_name}/{tool_name}")
        async def get_provider_tool(provider_name: str, tool_name: str):
            return await self.builtin_tool_handler.get_provider_tool(provider_name, tool_name)

        return router


@inject
class ApiToolRouter:
    """API工具路由独立处理器"""
    api_tool_handler: ApiToolHandler

    def __init__(self, api_tool_handler: ApiToolHandler):
        self.api_tool_handler = api_tool_handler

    def get_router(self) -> APIRouter:
        """创建API工具路由实例"""
        router = APIRouter(prefix="/api-tools")

        @router.post("/validate-openapi-schema")
        async def validate_api_tool(request: ValidateOpenApiSchemaRequest):
            return await self.api_tool_handler.validate_openapi_schema(request)

        @router.post("")
        async def create_api_tool(request: CreateApiToolRequest):
            return await self.api_tool_handler.create_api_tool(request)

        @router.get("/{provider_id}")
        async def get_api_tool_provider(provider_id: uuid.UUID):
            return await self.api_tool_handler.get_api_tool_provider(provider_id)

        @router.get("/{provider_id}/{tool_name}")
        async def get_api_tool(provider_id: uuid.UUID, tool_name: str):
            return await self.api_tool_handler.get_api_tool(provider_id, tool_name)

        @router.post("/{provider_id}/delete")
        async def delete_api_tool_provider(provider_id: uuid.UUID):
            return await self.api_tool_handler.delete_api_tool_provider(provider_id)

        @router.get("")
        async def get_api_tool_providers_with_page(current_page: int = 1, page_size: int = 20, search_word: str = ""):
            return await self.api_tool_handler.get_api_tool_providers_with_page(req=GetApiToolProvidersWithPageRequest(current_page=current_page,
                                                                                                                       page_size=page_size, search_word=search_word))

        @router.post("/{provider_id}/update")
        async def update_api_tool_provider(provider_id: uuid.UUID, request: UpdateApiToolProviderRequest):
            return await self.api_tool_handler.update_api_tool_provider(provider_id, request)

        return router


@inject
class Router:
    """主路由器，统一管理所有独立的路由"""
    app_router: AppRouter
    builtin_tool_router: BuiltinToolRouter
    api_tool_router: ApiToolRouter
    upload_file_router: UploadFileRouter
    dataset_router: DatasetRouter

    def __init__(self,
                 app_router: AppRouter,
                 builtin_tool_router: BuiltinToolRouter,
                 api_tool_router: ApiToolRouter,
                 upload_file_router: UploadFileRouter,
                 dataset_router: DatasetRouter):
        self.app_router = app_router
        self.builtin_tool_router = builtin_tool_router
        self.api_tool_router = api_tool_router
        self.upload_file_router = upload_file_router
        self.dataset_router = dataset_router

    def register_routes(self, app: FastAPI):
        """注册所有独立的路由到FastAPI应用"""
        app.include_router(self.app_router.get_router())
        app.include_router(
            self.builtin_tool_router.get_router())
        app.include_router(self.api_tool_router.get_router())
        app.include_router(self.upload_file_router.get_router())
        app.include_router(self.dataset_router.get_router())
