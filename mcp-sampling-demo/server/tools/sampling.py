
from fastmcp import Context
from . import tool
from typing import List, Dict, Any




@tool(name="Analyze Sentiment", description="分析文本情感倾向", category="analysis")
async def analyze_sentiment(text: str, ctx: Context) -> dict:
    """分析文本情感倾向
    
    参数:
    text: 要分析的文本
    ctx: MCP上下文对象
    
    返回:
    包含文本和情感分析结果的字典
    """
    prompt = f"""分析以下文本的情感倾向，将其分类为积极、中性或消极中的一种。
    请只输出一个单词：'积极'、'中性'或'消极'。
    
    要分析的文本: {text}"""
    
    # 请求LLM分析
    response = await ctx.sample(prompt)
    
    # 处理LLM的响应
    sentiment = response.text.strip()
    
    # 映射到标准情感值
    if "积极" in sentiment:
        sentiment = "积极"
    elif "消极" in sentiment:
        sentiment = "消极"
    else:
        sentiment = "中性"
    
    return {"text": text, "sentiment": sentiment}


# 模拟微博数据
MOCK_WEIBO_DATA = [
    {
        "weibo_id": "1001",
        "user_name": "科技爱好者",
        "publish_date": "2023-01-01",
        "publish_time": "08:30",
        "weibo_content": "新的一年开始了，希望今年能学到更多新技术，提升自己的能力。加油！",
    },
    {
        "weibo_id": "1002",
        "user_name": "美食家小李",
        "publish_date": "2023-01-01",
        "publish_time": "12:15",
        "weibo_content": "今天尝试了新的菜谱，结果完全失败了，浪费了一下午时间，心情糟糕透了。",
    },
    {
        "weibo_id": "1003",
        "user_name": "旅游达人",
        "publish_date": "2023-01-01",
        "publish_time": "16:45",
        "weibo_content": "刚刚结束了海南之旅，风景美不胜收，这次旅行真是太值了！",
    },
    {
        "weibo_id": "1004",
        "user_name": "健身教练",
        "publish_date": "2023-01-02",
        "publish_time": "07:00",
        "weibo_content": "早起跑步5公里，感觉精力充沛，一天的好状态从运动开始。",
    },
    {
        "weibo_id": "1005",
        "user_name": "学生小王",
        "publish_date": "2023-01-02",
        "publish_time": "22:30",
        "weibo_content": "期末考试终于结束了，可以好好休息几天了。",
    }
]


@tool(name="Get Weibo Data", description="获取微博数据并进行情感分析", category="data")
async def get_weibo_data(ctx: Context, limit: int = 5) -> List[Dict[str, Any]]:
    """获取微博数据并进行情感分析
    
    参数:
    ctx: MCP上下文对象
    limit: 返回微博数量限制
    
    返回:
    包含微博数据和情感分析结果的列表
    """
    # 获取采样数据
    sampled_data = MOCK_WEIBO_DATA
    
    # 对每条微博进行情感分析
    for weibo in sampled_data:
        # 调用情感分析工具
        sentiment_result = await analyze_sentiment(weibo["weibo_content"], ctx)
        weibo["sentiment"] = sentiment_result["sentiment"]
    
    return sampled_data