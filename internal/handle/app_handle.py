from openai import OpenAI
from pkg.response import Response, HttpCode
from internal.exception import NotFoundException
import os


class AppHandler:

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
