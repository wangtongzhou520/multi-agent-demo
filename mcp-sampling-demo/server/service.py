"""
MCP服务模块
"""
from fastmcp import FastMCP
from tools.registry import register_tools


class MCPService:
    """MCP服务类"""
    
    def __init__(self, name: str = "mcp-service"):
        """初始化MCP服务
        
        参数:
        name: 服务名称
        """
        self.mcp = FastMCP(name=name)
        self._register_tools()
    
    def _register_tools(self):
        """注册工具"""
        register_tools(self.mcp)
    
    def run(self, transport: str = "sse", host: str = "127.0.0.1", port: int = 8001):
        """运行服务
        
        参数:
        transport: 传输协议
        host: 主机地址
        port: 端口号
        """
        self.mcp.run(transport=transport, host=host, port=port)