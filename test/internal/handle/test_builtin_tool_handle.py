from pkg.response import HttpCode
import pytest

class TestBuiltinToolHandler:

    def test_get_category(self, client):
        resp = client.get("/builtin-tools/categories")
        assert resp.status_code == 200
        assert resp.json().get("code") == HttpCode.SUCCESS
        assert len(resp.json().get("data")) > 0

    def test_get_builtin_tools(self, client):
        resp = client.get("/builtin-tools")
        assert resp.status_code == 200
        assert resp.json().get("code") == HttpCode.SUCCESS
        assert len(resp.json().get("data")) > 0

    @pytest.mark.parametrize("provider_name, tool_name", [
        ("google", "google_serper"),
        ("openai", "openai_chat"),
    ])
    def test_get_provider_tool(self, provider_name, tool_name, client):
        resp = client.get(f"/builtin-tools/{provider_name}/{tool_name}")
        assert resp.status_code == 200
        if provider_name == "google":
            assert resp.json().get("code") == HttpCode.SUCCESS
            assert resp.json().get("data").get('name') == tool_name
        elif provider_name == "openai":
            assert resp.json().get("code") == HttpCode.NOT_FOUND
            assert resp.json().get("message") == f"Provider {provider_name} not found"

    @pytest.mark.parametrize("provider_name", [
        ("google"),
        ("openai"),
    ])
    def test_get_provider_icon(self, provider_name, client):
        resp = client.get(f"/builtin-tools/{provider_name}/icon")
        assert resp.status_code == 200
        if provider_name == "openai":
            assert resp.json().get("code") == HttpCode.NOT_FOUND
    