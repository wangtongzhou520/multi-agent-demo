import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from typing import List, Dict, Any, Optional, Union


class QwenMaxClient:
    """
    Qwen-Max模型客户端封装类
    提供统一的接口来调用Qwen-Max模型的各种功能
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化Qwen-Max客户端
        
        Args:
            api_key: DashScope API密钥，如果不提供将从环境变量DASHSCOPE_API_KEY获取
            base_url: API基础URL，默认为DashScope的兼容API端点
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY", "your-api-key")
        self.base_url = base_url
        self.model = self._create_model()

    def _create_model(self) -> ChatOpenAI:
        """
        创建Qwen-Max模型实例
        
        Returns:
            ChatOpenAI: Qwen-Max模型实例
        """
        return ChatOpenAI(
            model="qwen-max",
            api_key=self.api_key,
            base_url=self.base_url
        )

    def chat(self, messages: List[Union[HumanMessage, SystemMessage, AIMessage]]) -> str:
        """
        基础对话功能
        
        Args:
            messages: 消息列表，包含系统消息、用户消息和AI消息
            
        Returns:
            str: 模型响应内容
        """
        response = self.model.invoke(messages)
        return response.content

    def simple_chat(self, user_input: str, system_prompt: Optional[str] = None) -> str:
        """
        简单对话功能
        
        Args:
            user_input: 用户输入内容
            system_prompt: 系统提示词（可选）
            
        Returns:
            str: 模型响应内容
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=user_input))
        
        response = self.model.invoke(messages)
        return response.content

    def conversation(self, conversation_history: List[Dict[str, str]]) -> str:
        """
        多轮对话功能
        
        Args:
            conversation_history: 对话历史，格式为[{"role": "system/human/ai", "content": "内容"}, ...]
            
        Returns:
            str: 模型响应内容
        """
        messages = []
        for item in conversation_history:
            role = item["role"]
            content = item["content"]
            if role == "system":
                messages.append(SystemMessage(content=content))
            elif role == "human":
                messages.append(HumanMessage(content=content))
            elif role == "ai":
                messages.append(AIMessage(content=content))
                
        response = self.model.invoke(messages)
        return response.content

    def sentiment_analysis(self, text: str) -> str:
        """
        情感分析功能
        
        Args:
            text: 待分析的文本
            
        Returns:
            str: 情感分析结果（positive/negative/neutral）
        """
        system_prompt = "你是一个情感分析专家，请分析给定文本的情感倾向。只需回答'positive'、'negative'或'neutral'，不要包含其他内容。"
        user_input = f"分析以下文本的情感倾向：\n\n{text}"
        
        return self.simple_chat(user_input, system_prompt)

    def structured_output(self, query: str, format_instruction: str = "请以JSON格式回答") -> str:
        """
        结构化输出功能
        
        Args:
            query: 用户查询
            format_instruction: 格式化指令
            
        Returns:
            str: 结构化输出结果
        """
        messages = [
            SystemMessage(content=format_instruction),
            HumanMessage(content=query)
        ]
        
        response = self.model.invoke(messages)
        return response.content

    def custom_request(self, system_prompt: str, user_input: str, 
                      conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        自定义请求功能
        
        Args:
            system_prompt: 系统提示词
            user_input: 用户输入
            conversation_history: 对话历史（可选）
            
        Returns:
            str: 模型响应内容
        """
        messages = [SystemMessage(content=system_prompt)]
        
        # 添加对话历史（如果提供）
        if conversation_history:
            for item in conversation_history:
                role = item["role"]
                content = item["content"]
                if role == "human":
                    messages.append(HumanMessage(content=content))
                elif role == "ai":
                    messages.append(AIMessage(content=content))
        
        # 添加当前用户输入
        messages.append(HumanMessage(content=user_input))
        
        response = self.model.invoke(messages)
        return response.content


def main():
    """
    使用示例
    """
    # 创建客户端实例
    client = QwenMaxClient()
    
    print("Qwen-Max LangChain 类封装示例")
    print("=" * 50)
    
    # 1. 基础对话示例
    print("=== 基础对话示例 ===")
    messages = [HumanMessage(content="你好，介绍一下你自己")]
    response = client.chat(messages)
    print(f"用户: {messages[0].content}")
    print(f"Qwen-Max: {response}")
    print()
    
    # 2. 简单对话示例
    print("=== 简单对话示例 ===")
    response = client.simple_chat("什么是人工智能？", "你是一个AI助手，请用简洁明了的语言回答问题。")
    print(f"Qwen-Max: {response}")
    print()
    
    # 3. 多轮对话示例
    print("=== 多轮对话示例 ===")
    conversation_history = [
        {"role": "system", "content": "你是一个乐于助人的AI助手"},
        {"role": "human", "content": "你好，我想了解人工智能的发展历史"},
        {"role": "ai", "content": "人工智能的发展可以追溯到20世纪50年代，当时图灵提出了著名的图灵测试..."},
        {"role": "human", "content": "那你能详细说说近年来的重要突破吗？"}
    ]
    response = client.conversation(conversation_history)
    print("对话历史:")
    for msg in conversation_history:
        print(f"{msg['role']}: {msg['content']}")
    print(f"Qwen-Max: {response}")
    print()
    
    # 4. 情感分析示例
    print("=== 情感分析示例 ===")
    text = "今天天气真好，阳光明媚，让人心情愉悦"
    result = client.sentiment_analysis(text)
    print(f"待分析文本: {text}")
    print(f"情感分析结果: {result}")
    print()
    
    # 5. 结构化输出示例
    print("=== 结构化输出示例 ===")
    query = "列出Python中常用的数据结构及其特点"
    result = client.structured_output(query, "请以JSON格式回答，包含'name'和'description'字段")
    print(f"用户查询: {query}")
    print(f"结构化输出: {result}")
    print()
    
    # 6. 自定义请求示例
    print("=== 自定义请求示例 ===")
    system_prompt = "你是一个技术专家，请以专业的角度回答问题。"
    user_input = "解释一下什么是大语言模型？"
    result = client.custom_request(system_prompt, user_input)
    print(f"系统提示: {system_prompt}")
    print(f"用户输入: {user_input}")
    print(f"Qwen-Max: {result}")
    print()
    
    print("所有示例运行完成！")


if __name__ == "__main__":
    # 设置API密钥环境变量示例（如果需要）
    # os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"
    
    main()