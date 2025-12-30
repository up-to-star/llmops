from pydantic import BaseModel, Field
from typing import Any


class CompletionRequest(BaseModel):
    query: str = Field(
        ...,
        max_length=2048,
        json_schema_extra={
            "error_msg": {
                "missing": "query is required",
                "max_length": "query must be less than 2048 characters"
            }
        }
    )
