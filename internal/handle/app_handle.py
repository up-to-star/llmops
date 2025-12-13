from openai import OpenAI
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

        return {"content": completion.choices[0].message.content}

    async def ping(self):
        return {"message": "pong"}
