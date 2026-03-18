from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from web_mcp.server import USER_AGENT, fetch_raw, fetch_text, main, mcp as mcp_server


@pytest.fixture
def mock_response():
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 200
    response.text = "<html><body><h1>Hello</h1></body></html>"
    response.headers = {"content-type": "text/html"}
    response.raise_for_status = Mock()
    return response


class TestFetchRaw:
    async def test_returns_raw_html(self, mock_response):
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("web_mcp.server.httpx.AsyncClient", return_value=mock_client):
            result = await fetch_raw(url="https://example.com")

        assert result == "<html><body><h1>Hello</h1></body></html>"
        mock_client.get.assert_called_once_with(
            "https://example.com",
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
        )

    async def test_http_error_returns_message(self):
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.raise_for_status = Mock(
            side_effect=httpx.HTTPStatusError(
                "Not Found", request=Mock(), response=mock_response
            )
        )
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("web_mcp.server.httpx.AsyncClient", return_value=mock_client):
            result = await fetch_raw(url="https://example.com/missing")

        assert "HTTP error 404" in result

    async def test_request_error_returns_message(self):
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get = AsyncMock(
            side_effect=httpx.RequestError("Connection refused", request=Mock())
        )
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("web_mcp.server.httpx.AsyncClient", return_value=mock_client):
            result = await fetch_raw(url="https://unreachable.test")

        assert "Request error" in result


class TestFetchText:
    async def test_returns_extracted_text(self, mock_response):
        mock_response.text = "<html><body><script>var x=1;</script><style>body{}</style><h1>Hello</h1><p>World</p></body></html>"
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("web_mcp.server.httpx.AsyncClient", return_value=mock_client):
            result = await fetch_text(url="https://example.com")

        assert "Hello" in result
        assert "World" in result
        assert "var x=1" not in result
        assert "body{}" not in result

    async def test_http_error_returns_message(self):
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = AsyncMock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.raise_for_status = Mock(
            side_effect=httpx.HTTPStatusError(
                "Server Error", request=Mock(), response=mock_response
            )
        )
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("web_mcp.server.httpx.AsyncClient", return_value=mock_client):
            result = await fetch_text(url="https://example.com/error")

        assert "HTTP error 500" in result

    async def test_request_error_returns_message(self):
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get = AsyncMock(
            side_effect=httpx.RequestError("Connection refused", request=Mock())
        )
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("web_mcp.server.httpx.AsyncClient", return_value=mock_client):
            result = await fetch_text(url="https://unreachable.test")

        assert "Request error" in result


class TestMain:
    def test_main_calls_run(self):
        with patch.object(mcp_server, "run") as mock_run:
            main()
            mock_run.assert_called_once()
