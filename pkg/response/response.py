from .http_code import HttpCode
from dataclasses import field, dataclass
from typing import Any


@dataclass
class Response:
    code: HttpCode = HttpCode.SUCCESS
    message: str = ""
    data: Any = field(default_factory=dict)
