from fastapi import FastAPI, APIRouter
from internal.handle.app_handle import AppHandler
from injector import inject

@inject
class Router:
    def __init__(self, app_handler: AppHandler):
        self.router = APIRouter()
        self.app_handler = app_handler
        self._register_routes()
    
    def _register_routes(self):
        @self.router.get("/ping")
        def ping():
            return self.app_handler.ping()
    
    def register_router(self, app: FastAPI):
        app.include_router(self.router)
