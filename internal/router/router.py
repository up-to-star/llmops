from fastapi import FastAPI, APIRouter
from internal.handle.app_handle import AppHandler
from injector import inject
from pydantic import BaseModel
from internal.schema import CompletionRequest


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

        @self.router.post("/completion")
        async def completion(request: CompletionRequest):
            return await self.app_handler.completion(request.query)

        @self.router.get("/test_db")
        async def test_db():
            return await self.app_handler.test_db()

    def register_router(self, app: FastAPI):
        app.include_router(self.router)
