from fastapi import FastAPI, APIRouter
from internal.handle import AppHandler, BuiltinToolHandler
from injector import inject
from pydantic import BaseModel
from internal.schema import CompletionRequest
import uuid


@inject
class Router:
    app_handler: AppHandler
    builtin_tool_handler: BuiltinToolHandler

    def __init__(self, app_handler: AppHandler, builtin_tool_handler: BuiltinToolHandler):
        self.router = APIRouter()
        self.app_handler = app_handler
        self.builtin_tool_handler = builtin_tool_handler
        self._register_routes()
        self._register_builtin_tool_routes()

    def _register_routes(self):
        @self.router.get("/ping")
        async def ping():
            return await self.app_handler.ping()

        @self.router.post("/apps/{app_id}/debug")
        async def debug(request: CompletionRequest, app_id: uuid.UUID):
            return await self.app_handler.debug(request.query, app_id)

        @self.router.get("/test_db")
        async def test_db():
            return await self.app_handler.test_db()

        @self.router.post("/app")
        async def create_app():
            return await self.app_handler.create_app()

        @self.router.get("/app/{app_id}")
        async def get_app(app_id: uuid.UUID):
            return await self.app_handler.get_app(app_id)

        @self.router.post("/app/{app_id}")
        async def update_app(app_id: uuid.UUID):
            return await self.app_handler.update_app(app_id)

        @self.router.delete("/app/{app_id}")
        async def delete_app(app_id: uuid.UUID):
            return await self.app_handler.delete_app(app_id)

    def _register_builtin_tool_routes(self):
        @self.router.get("/builtin-tools")
        async def get_builtin_tools():
            return await self.builtin_tool_handler.get_builtin_tools()
        
        @self.router.get("/builtin-tools/categories")
        async def get_categories():
            return await self.builtin_tool_handler.get_categories()
        
        @self.router.get("/builtin-tools/{provider_name}/icon")
        async def get_provider_icon(provider_name: str):
            return await self.builtin_tool_handler.get_provider_icon(provider_name)
        
        @self.router.get("/builtin-tools/{provider_name}/{tool_name}")
        async def get_provider_tool(provider_name: str, tool_name: str):
            return await self.builtin_tool_handler.get_provider_tool(provider_name, tool_name)
        
        

    def register_router(self, app: FastAPI):
        app.include_router(self.router)
