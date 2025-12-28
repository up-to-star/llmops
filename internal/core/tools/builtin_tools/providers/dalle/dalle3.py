from langchain.tools import BaseTool
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from pydantic import Field, BaseModel
from internal.lib.helper import add_attribute

class Dalle3ArgsSchema(BaseModel):
    """DALLE-3绘图工具参数"""
    query: str = Field(description="输入是生成图像的文本提示(prompt)")

@add_attribute("args_schema", Dalle3ArgsSchema)
def dalle3(**kwargs) -> BaseTool:
    """返回DALLE-3绘图工具"""
    return OpenAIDALLEImageGenerationTool(
        name="dalle3",
        api_wrapper=DallEAPIWrapper(model="dall-e-3", **kwargs),
        args_schema=Dalle3ArgsSchema,
    )