from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import BaseTool

def wikipedia_search(**kwargs) -> BaseTool:
    """返回维基百科搜索工具"""
    return WikipediaQueryRun(
        name="wikipedia_search",
        api_wrapper=WikipediaAPIWrapper(),
    )