from openai import OpenAI
from pkg.response import Response, HttpCode
import os
from injector import inject
from internal.service import AppService
import uuid


@inject
class AppHandler:
    def __init__(self, app_service: AppService):
        self.app_service = app_service

    async def create_app(self):
        app = await self.app_service.create_app()
        response = Response(
            code=HttpCode.SUCCESS,
            message="创建APP成功",
            data={
                "app_id": app.id,
                "name": app.name,
                "account_id": app.account_id,
                "description": app.description
            }
        )
        return response

    async def delete_app(self, app_id: uuid.UUID):
        app = await self.app_service.delete_app(app_id)
        if app is None:
            response = Response(
                code=HttpCode.NOT_FOUND,
                message="app not found",
                data={}
            )
            return response
        response = Response(
            code=HttpCode.SUCCESS,
            message=f"删除应用{app.name}成功",
            data={
                "app_id": app.id,
                "name": app.name,
                "account_id": app.account_id,
                "description": app.description
            }
        )
        return response

    async def update_app(self, app_id: uuid.UUID):
        app = await self.app_service.update_app(app_id)
        if app is None:
            response = Response(
                code=HttpCode.NOT_FOUND,
                message="app not found",
                data={}
            )
            return response
        response = Response(
            code=HttpCode.SUCCESS,
            message="success",
            data={
                "app_id": app.id,
                "name": app.name,
                "account_id": app.account_id,
                "description": app.description
            }
        )
        return response

    async def get_app(self, app_id: uuid.UUID):
        app = await self.app_service.get_app(app_id)
        if app is None:
            response = Response(
                code=HttpCode.NOT_FOUND,
                message="app not found",
                data={}
            )
            return response
        response = Response(
            code=HttpCode.SUCCESS,
            message="success",
            data={
                "app_id": app.id,
                "name": app.name,
                "account_id": app.account_id,
                "description": app.description
            }
        )
        return response

    async def completion(self, query: str):
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_API_BASE_URL"),
        )
        messages = [
            {"role": "system", "content": "你是OpenAI开发的聊天机器人"},
            {"role": "user", "content": query}
        ]
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False,
        )
        response = Response(
            code=HttpCode.SUCCESS,
            message="success",
            data={"content": completion.choices[0].message.content}
        )
        return response

    async def ping(self):
        response = Response(
            code=HttpCode.SUCCESS,
            message="success",
            data={"message": "pong"}
        )
        return response

    async def test_db(self):
        try:
            from internal.model import User
            from tortoise.exceptions import IntegrityError
            try:
                user = await User.create(
                    username="test_user",
                    password="test_pass",
                    email="test@example.com"
                )
                await user.save()
            except IntegrityError:
                user = await User.get(username="test_user")
            users = await User.all()
            response = Response(
                code=HttpCode.SUCCESS,
                message="Datebase connection successful",
                data={
                    "total_users": len(users),
                    "test_user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                }
            )
            return response
        except Exception as e:
            response = Response(
                code=HttpCode.INTERNAL_SERVER_ERROR,
                message="Database connection failed",
                data={"error": str(e)}
            )
            return response
