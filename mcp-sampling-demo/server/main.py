from fastmcp import FastMCP
from tools.registry import register_tools
from service import MCPService


# 创建MCP服务实例
mcp_service = MCPService(name="mcp-sampling-server")


if __name__ == "__main__":
    mcp_service.run(transport="sse", host="127.0.0.1", port=8001)
