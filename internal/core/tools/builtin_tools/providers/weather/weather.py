from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
import os
import json


class WeatherArgsSchema(BaseModel):
    city: str = Field(description="要查询天气的目标城市, 例如：广州")


class WeatherTool(BaseTool):
    name: str = "weather"
    description: str = "当你想查询天气或者天气相关的问题时可以使用的工具"
    args_schema: Type[BaseModel] = WeatherArgsSchema

    def _run(self, *args, **kwargs) -> str:
        """根据传入的城市名称运行调用API获取城市对应的天气预报信息"""
        api_box_id = os.getenv("API_BOX_ID")
        api_box_key = os.getenv("API_BOX_KEY")
        try:
            if not api_box_id or not api_box_key:
                raise ValueError(
                    "API_BOX_ID and API_BOX_KEY must be set in environment variables")
            city = kwargs.get("city", "")
            print(city)
            base_url = "https://cn.apihz.cn/api/tianqi/tqyb.php"

            session = requests.session()
            response = session.request(
                method="GET",
                url=f"{base_url}?id={api_box_id}&key={api_box_key}&place={city}&day=1&hourtype=1"
            )
            if response.status_code != 200:
                raise ValueError(
                    f"Failed to get weather data, status code: {response.status_code}")
            data = response.json()
            if data.get("code") != 200:
                return f"Failed to get weather data, error message: {data.get('msg', '')}"

            return json.dumps(data, ensure_ascii=False)

        except Exception as e:
            return f"Failed to get weather data, error message: {str(e)}"


def weather(**kwargs) -> BaseTool:
    """返回天气查询工具"""
    return WeatherTool(**kwargs)


