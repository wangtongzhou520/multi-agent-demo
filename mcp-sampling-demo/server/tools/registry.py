"""
工具注册模块
"""
import inspect
from fastmcp import FastMCP
from . import calculator
from . import sampling


def register_tools(mcp: FastMCP):
    """注册所有工具到MCP实例
    
    参数:
    mcp: FastMCP实例
    """
    # 获取当前模块中的所有子模块
    modules = [calculator, sampling]
    
    # 遍历所有模块中的函数
    for module in modules:
        for name, func in inspect.getmembers(module, inspect.isfunction):
            # 检查是否有工具标记
            if hasattr(func, "_is_tool"):
                # 获取元数据
                metadata = getattr(func, "_metadata", {})
                
                # 注册工具
                mcp.tool(
                    name=metadata.get("name"),
                    description=metadata.get("description"),
                    category=metadata.get("category"),
                )(func)