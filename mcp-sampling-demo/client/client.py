from fastmcp import Client
from fastmcp.client.sampling import (
    SamplingMessage,
    SamplingParams,
    RequestContext,
)
from fastmcp.client.transports import StreamableHttpTransport
import asyncio
from langchain_openai import ChatOpenAI
import os


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    # Extract message content
    conversation = []
    for message in messages:
        content = message.content.text if hasattr(message.content, 'text') else str(message.content)
        conversation.append(f"{message.role}: {content}")

    # Use the system prompt if provided
    system_prompt = params.systemPrompt or "You are a helpful assistant."

    # Here you would integrate with your preferred LLM service
    # This is just a placeholder response
    return f"Response based on conversation: {' | '.join(conversation)}"


async def run():
    transport = StreamableHttpTransport(url="http://127.0.0.1:8003/mcp")

    # 使用HTTP方式连接到服务端
    client = Client(transport, sampling_handler=sampling_handler)
    
    async with client:
        result = await client.call_tool(
            "analyze_sentiment", {"text": "今天天气真好"}
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(run())