from pydantic import BaseModel, Field, field_validator
from internal.exception import ValidationException
from enum import Enum


class ParameterIn(str, Enum):
    """参数位置枚举类"""
    PATH = "path"
    QUERY = "query"
    HEADER = "header"
    COOKIE = "cookie"
    REQUEST_BODY = "request_body"


class ParamaterType(str, Enum):
    """参数类型枚举类"""
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"


class OpenAPISchema(BaseModel):
    """OpenAPI 规范的实体类"""
    description: str = Field(
        default="", validate_default=True, description="工具提供者的描述信息")
    server: str = Field(default="", validate_default=True,
                        description="工具提供者的服务基础地址")
    paths: dict[str, dict] = Field(
        default_factory=dict, validate_default=True, description="工具提供者的路径参数字典")

    @field_validator("server", mode="before")
    def validate_server(cls, server: str) -> str:
        """验证server数据"""
        if server is None or server.strip() == "":
            raise ValidationException("server字段不能为空且为字符串")
        return server

    @field_validator("description", mode="before")
    def validate_description(cls, description: str) -> str:
        """验证description数据"""
        if description is None or description.strip() == "":
            raise ValidationException("description字段不能为空且为字符串")
        return description

    @field_validator("paths", mode="before")
    def validate_paths(cls, paths: dict[str, dict]) -> dict[str, dict]:
        """验证paths数据, 涵盖、方法提取、operationId、参数信息"""
        if not paths or not isinstance(paths, dict):
            raise ValidationException("paths字段不能为空且为字典")
        methods = ["get", "post"]
        interfaces = []
        extra_paths = {}

        for path, path_item in paths.items():
            for method in methods:
                if method in path_item:
                    interfaces.append({
                        "path": path,
                        "method": method,
                        "operation": path_item[method]
                    })
        operation_ids = []
        for interface in interfaces:
            if not isinstance(interface["operation"].get("description"), str):
                raise ValidationException(
                    f"description字段不能为空且为字符串, paths.{interface['path']}.{interface['method']}")
            if not isinstance(interface["operation"].get("operationId"), str):
                raise ValidationException(
                    f"operationId字段不能为空且为字符串, paths.{interface['path']}.{interface['method']}")
            if not isinstance(interface["operation"].get("parameters", []), list):
                raise ValidationException(
                    f"parameters字为空或为列表, paths.{interface['path']}.{interface['method']}")

            if interface["operation"].get("operationId") in operation_ids:
                raise ValidationException(
                    f"operationId字段值重复, {interface['operation'].get('operationId')}")
            operation_ids.append(interface["operation"].get("operationId"))
            for parameter in interface["operation"].get("parameters", []):
                if not isinstance(parameter.get("name"), str):
                    raise ValidationException(
                        f"parameters字段中name字段不能为空且为字符串, paths.{interface['path']}.{interface['method']}")
                if not isinstance(parameter.get("description"), str):
                    raise ValidationException(
                        f"parameters字段中description字段不能为空且为字符串, paths.{interface['path']}.{interface['method']}")
                if not isinstance(parameter.get("required"), bool):
                    raise ValidationException(
                        f"parameters字段中required字段不能为空且为布尔值, paths.{interface['path']}.{interface['method']}")
                if not isinstance(parameter.get("in"), str) or parameter.get("in") not in ParameterIn.__members__.values():
                    raise ValidationException(
                        f"parameters字段中in字段必须为{'/'.join(ParameterIn.__members__.values())}, paths.{interface['path']}.{interface['method']}")
                if not isinstance(parameter.get("type"), str) or parameter.get("type") not in ParamaterType.__members__.values():
                    raise ValidationException(
                        f"parameters字段中type字段必须为{'/'.join(ParamaterType.__members__.values())}, paths.{interface['path']}.{interface['method']}")
            extra_paths[interface["path"]] = {
                interface["method"]: {
                    "operationId": interface["operation"].get("operationId"),
                    "description": interface["operation"].get("description"),
                    "parameters": [{
                        "name": parameter.get("name"),
                        "description": parameter.get("description"),
                        "required": parameter.get("required"),
                        "in": parameter.get("in"),
                        "type": parameter.get("type")
                    } for parameter in interface["operation"].get("parameters", [])]
                }
            }
        return extra_paths
