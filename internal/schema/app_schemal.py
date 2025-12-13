from pydantic import BaseModel, Field


class CompletionRequest(BaseModel):
    query: str = Field(
        ...,
        max_length=2048,
        error_msg={
            "missing": "query is required",
            "max_length": "query must be less than 2048 characters"
        }
    )
