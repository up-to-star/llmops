from internal.model import App
from dataclasses import dataclass
import uuid


@dataclass
class AppService:
    """AI应用服务类"""

    async def create_app(self):
        app = await App.create(
            name="测试机器人",
            account_id=uuid.uuid4(),
            description="这是一个简单的聊天机器人应用体验会话中"
        )
        return app

    async def get_app(self, app_id: uuid.UUID):
        app = await App.get_or_none(id=app_id)
        return app

    async def update_app(self, app_id: uuid.UUID):
        app = await App.get_or_none(id=app_id)
        if app is None:
            return None
        app.name = "新的聊天机器人"
        app.description = "这是一个新的聊天机器人应用"
        await app.save()
        return app

    async def delete_app(self, app_id: uuid.UUID):
        app = await App.get_or_none(id=app_id)
        if app is None:
            return None
        await app.delete()
        return app
