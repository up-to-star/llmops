from enum import Enum


class HttpCode(int, Enum):
    SUCCESS = 200
    FAIL = 400
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    VALIDATION_ERROR = 422
