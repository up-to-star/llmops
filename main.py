from injector import Injector
from internal.server import Http
from internal.router import Router
import uvicorn

if __name__ == "__main__":
    injector = Injector()
    app = Http(router=injector.get(Router))

    uvicorn.run(app, host="0.0.0.0", port=10000)