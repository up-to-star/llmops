from injector import Injector
from internal.server import Http
from internal.router import Router

# 创建依赖注入容器
injector = Injector()

# 创建应用实例
app = Http(router=injector.get(Router))