from fastmcp import Client
from fastmcp.client.sampling import (
    SamplingMessage,
    SamplingParams,
    RequestContext,
)
from qwen_client import QwenMaxClient
import asyncio
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 初始化QwenMaxClient实例
qwen_client = QwenMaxClient()


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    """处理来自服务器的采样请求"""
    print(f"Received sampling request with messages: {messages}")
    
    # 转换MCP消息格式为LangChain格式
    langchain_messages = []
    for msg in messages:
        # 获取消息内容
        content = msg.content.text if hasattr(msg.content, 'text') else str(msg.content)
        
        if msg.role == "user":
            langchain_messages.append(HumanMessage(content=content))
        elif msg.role == "assistant":
            langchain_messages.append(AIMessage(content=content))
        elif msg.role == "system":
            langchain_messages.append(SystemMessage(content=content))
    
    # 使用QwenMaxClient处理请求
    response = qwen_client.chat(langchain_messages)
    return response


async def run():
    # 使用HTTP方式连接到服务端
    client = Client("http://127.0.0.1:8003/mcp", sampling_handler=sampling_handler)
    
    async with client:
        result = await client.call_tool(
            "analyze_sentiment", {"text": "今天天气真好"}
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(run())