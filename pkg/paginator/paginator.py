from pydantic import BaseModel, Field
from typing import Optional, Any, TypeVar
from tortoise.models import Model
from tortoise.queryset import QuerySet
import math
import asyncio


class PaginatorRequest(BaseModel):
    """分页请求参数"""
    current_page: Optional[int] = Field(
        default=1, ge=1, le=10000, description="当前页码，默认1")
    page_size: Optional[int] = Field(
        default=20, ge=1, le=50, description="每页数量，最大50")


class Paginator(BaseModel):
    """分页器"""
    total_page: int = Field(default=0, description="总页数")
    total_record: int = Field(default=0, description="总记录数")
    current_page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=20, description="每页数量")


class PageModel(BaseModel):
    data: list[Any] = Field(default_factory=list, description="分页数据")
    paginator: Paginator = Field(default_factory=Paginator, description="分页器")


ModelType = TypeVar("ModelType", bound=Model)


class BaseQuery:
    """
    基础查询类，封装分页逻辑
    """

    def __init__(self, model: type[ModelType], page: int = 1, page_size: int = 20):
        self.model = model
        self.current_page = max(1, page)
        self.page_size = min(max(1, page_size), 1000)  # 防止过大
        self.paginator = Paginator(
            current_page=self.current_page,
            page_size=self.page_size
        )

    async def paginate(self, select: QuerySet[Any]):
        """
        对传入的查询进行分页
        :param select: Tortoise 查询集（QuerySet）
        :return: PageModel 包含数据和分页信息
        """
        # 1. 并发获取总数和分页数据
        total, items = await asyncio.gather(
            select.count(),
            select.offset((self.current_page - 1) * self.page_size)
            .limit(self.page_size)
            .order_by('-created_at')  # 可选排序
        )

        # 2. 更新分页器信息
        self.paginator.total_record = total
        self.paginator.total_page = math.ceil(total / self.page_size)

        return items, self.paginator
