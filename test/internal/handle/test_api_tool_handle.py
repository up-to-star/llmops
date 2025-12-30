import pytest
from pkg.response import HttpCode
from internal.schema.api_tool_schema import ValidateOpenApiSchemaRequest

openapi_schema = """{
  "server": "http://localhost:8000",
  "description": "Test API",
  "paths": {"./test": {
    "get": {
      "summary": "Test GET",
      "description": "Test GET endpoint",
      "operationId": "test_get",
      "parameters": [],
      "responses": {
        "200": {
          "description": "A successful response",
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "message": {
                    "type": "string",
                    "description": "A successful message"
                  }
                }
              }
            }
          }
        }
      }
    }
  }}
}"""

class TestApiToolHandle:

    @pytest.mark.parametrize("openapi_schema", [
        "123",
        openapi_schema,
    ])
    def test_validate_openapi_schema(self, openapi_schema, client):
        resp = client.post("/api-tools/validate-openapi-schema", json={"openapi_schema": openapi_schema})
        assert resp.status_code == 200
        if openapi_schema == "123":
            assert resp.json().get("code") == HttpCode.VALIDATION_ERROR
        else:
            assert resp.json().get("code") == HttpCode.SUCCESS
