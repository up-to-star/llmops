from pkg.response import HttpCode
import pytest


class TestAppHandle:

    @pytest.mark.parametrize("query", [None, "你好，你是谁？"])
    def test_completion(self, client, query):
        response = client.post("/completion", json={"query": query})
        assert response.status_code == 200
        if query is None:
            assert response.json()["code"] == HttpCode.VALIDATION_ERROR
        else:
            assert response.json()["code"] == HttpCode.SUCCESS
