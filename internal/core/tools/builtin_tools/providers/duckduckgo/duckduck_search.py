from langchain.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import BaseModel, Field
from internal.lib.helper import add_attribute

class DDGInput(BaseModel):
    """DuckDuckGo搜索参数描述"""
    query: str = Field(description="需要检索查询的语句")

@add_attribute("args_schema", DDGInput)
def duckduckgo_search(**kwargs) -> BaseTool:
    """返回 DuckDuckGo 搜索工具"""
    return DuckDuckGoSearchRun(
        description="用于进行 DuckDuckGo 搜索的工具, DuckDuckGo是一个注重隐私的搜索引擎, 工具的输入是一个查询语句",
        args_schema=DDGInput,
    )