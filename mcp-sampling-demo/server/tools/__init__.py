def tool(name: str = None, description: str = None, category: str = "default"):
    """标记工具函数并添加元数据"""
    def decorator(func):
        func._is_tool = True
        func._metadata = {
            "name": name or func.__name__,
            "description": description or func.__doc__ or "",
            "category": category,
        }
        return func
    return decorator