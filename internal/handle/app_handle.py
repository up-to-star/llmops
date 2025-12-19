from pkg.response import Response, HttpCode
import os
from injector import inject
from internal.service import AppService
import uuid
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver


class CustomAgentState(AgentState):
    user_id: str
    preferences: dict


@inject
class AppHandler:
    def __init__(self, app_service: AppService):
        self.app_service = app_service
        # 创建一个全局的InMemorySaver实例，用于保存对话历史
        self.checkpointer = InMemorySaver()
        # 初始化chat model
        self.model = init_chat_model('deepseek-chat', model_provider='deepseek')
        # 创建agent实例，只需要创建一次
        self.agent = create_agent(
            model=self.model,
            system_prompt="你是一个强大的聊天机器人，能根据用户的问题进行回答",
            tools=[],
            state_schema=CustomAgentState,
            checkpointer=self.checkpointer,
        )

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

    async def debug(self, query: str, app_id: uuid.UUID):
        # 使用已创建的agent实例，传入当前查询和thread_id
        result = self.agent.invoke(
            {
                "messages": [{"role": "user", "content": query}],
                "user_id": str(app_id),
                "preferences": {"language": "zh-CN"},
            },
            config={"thread_id": str(app_id)}
        )
        response = Response(
            code=HttpCode.SUCCESS,
            message="success",
            data={"content": result['messages'][-1].content}
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
