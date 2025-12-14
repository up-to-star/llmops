from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from internal.router import Router
from pkg.response import Response, HttpCode
from internal.exception import CustomException


class Http(FastAPI):
    def __init__(self, *args, router: Router, **kwargs):
        super().__init__(*args, **kwargs)
        router.register_router(self)
        # 添加自定义验证异常处理器
        self.add_exception_handler(
            RequestValidationError, self._validation_exception_handler)
        # 添加自定义异常处理器
        self.add_exception_handler(
            CustomException, self._custom_exception_handler)

    async def _custom_exception_handler(self, request: Request, exc: CustomException):

        # 构建自定义响应
        response_data = Response(
            code=exc.code,
            message=exc.message or "An error occurred",
            data=exc.data or {}
        )

        # 返回 JSON 响应
        return JSONResponse(
            status_code=200,
            content=response_data.__dict__
        )

    async def _validation_exception_handler(self, request: Request, exc: RequestValidationError):
        # 获取第一个验证错误信息
        first_error = exc.errors()[0]
        error_msg = first_error.get("msg", "Validation error")

        # 构建自定义响应
        response_data = Response(
            code=HttpCode.VALIDATION_ERROR,
            message=error_msg,
            data={}
        )

        # 返回 JSON 响应
        return JSONResponse(
            status_code=200,
            content=response_data.__dict__
        )
