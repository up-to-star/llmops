from pkg.response import HttpCode
from typing import Any
from dataclasses import field


class CustomException(Exception):
    code: HttpCode = HttpCode.FAIL
    message: str = ""
    data: Any = field(default_factory=dict)

    def __init__(self, message: str = None, data: Any = None):
        super().__init__()
        self.message = message
        self.data = data


class FailException(CustomException):
    pass


class NotFoundException(CustomException):
    code: HttpCode = HttpCode.NOT_FOUND


class UnauthorizedException(CustomException):
    code: HttpCode = HttpCode.UNAUTHORIZED


class ForbiddenException(CustomException):
    code: HttpCode = HttpCode.FORBIDDEN


class ValidationException(CustomException):
    code: HttpCode = HttpCode.VALIDATION_ERROR
