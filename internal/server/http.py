from fastapi import FastAPI
from internal.router import Router

class Http(FastAPI):
    def __init__(self, *args, router: Router, **kwargs):
        super().__init__(*args, **kwargs)
        router.register_router(self)