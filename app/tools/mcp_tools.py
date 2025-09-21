from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from app.web.settings import settings

mcp_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.parallel.ai/v1beta/search_mcp/",
        headers={"x-api-key": settings.parallel_api_key},
    )
)