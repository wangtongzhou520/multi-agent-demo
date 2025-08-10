"""
计算器工具模块
"""
from . import tool


@tool(name="Addition", description="加法运算", category="math")
def add(a: float, b: float) -> float:
    """加法运算

    参数:
    a: 第一个数字
    b: 第二个数字

    返回:
    两数之和
    """
    return a + b


@tool(name="Subtraction", description="减法运算", category="math")
def subtract(a: float, b: float) -> float:
    """减法运算

    参数:
    a: 被减数
    b: 减数

    返回:
    两数之差
    """
    return a - b


@tool(name="Multiplication", description="乘法运算", category="math")
def multiply(a: float, b: float) -> float:
    """乘法运算

    参数:
    a: 第一个数字
    b: 第二个数字

    返回:
    两数之积
    """
    return a * b


@tool(name="Division", description="除法运算", category="math")
def divide(a: float, b: float) -> float:
    """除法运算

    参数:
    a: 被除数
    b: 除数

    返回:
    两数之商

    异常:
    ZeroDivisionError: 当除数为0时抛出
    """
    if b == 0:
        raise ZeroDivisionError("除数不能为零")
    return a / b