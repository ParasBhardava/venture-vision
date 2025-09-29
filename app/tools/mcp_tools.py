from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from app.web.settings import settings

parallel_mcp_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.parallel.ai/v1beta/search_mcp/",
        headers={"x-api-key": settings.parallel_api_key},
    )
)

exa_mcp_toolset = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=f"https://mcp.exa.ai/mcp?exaApiKey={settings.exa_api_key}",
        )
    )


brightdata_mcp_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=f"https://mcp.brightdata.com/mcp?token={settings.brightdata_api_key}",
    )
)