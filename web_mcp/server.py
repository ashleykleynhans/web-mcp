from mcp.server.fastmcp import FastMCP

from bs4 import BeautifulSoup
import httpx

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"

mcp = FastMCP("web-mcp")


@mcp.tool()
async def fetch_raw(url: str) -> str:
    """Fetch a URL and return the raw HTML/text content."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"User-Agent": USER_AGENT},
                follow_redirects=True,
            )
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        return f"HTTP error {e.response.status_code} fetching {url}"
    except httpx.RequestError:
        return f"Request error fetching {url}"


@mcp.tool()
async def fetch_text(url: str) -> str:
    """Fetch a URL and return extracted readable text (no HTML tags, scripts, or styles)."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"User-Agent": USER_AGENT},
                follow_redirects=True,
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            return soup.get_text(separator="\n", strip=True)
    except httpx.HTTPStatusError as e:
        return f"HTTP error {e.response.status_code} fetching {url}"
    except httpx.RequestError:
        return f"Request error fetching {url}"
