from fastapi import FastAPI, APIRouter
from internal.handle.app_handle import AppHandler
from injector import inject
from pydantic import BaseModel
from internal.schema import CompletionRequest
import uuid


@inject
class Router:
    def __init__(self, app_handler: AppHandler):
        self.router = APIRouter()
        self.app_handler = app_handler
        self._register_routes()

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
        
    def register_router(self, app: FastAPI):
        app.include_router(self.router)
