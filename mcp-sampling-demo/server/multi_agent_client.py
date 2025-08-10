"""
多智能体微博情感分析客户端
模拟多个智能体协作完成微博情感分析任务
"""
import asyncio
import json
from fastmcp import Client
from typing import List, Dict, Any


class WeiboAnalysisAgent:
    """微博分析智能体基类"""
    
    def __init__(self, name: str, mcp_client: Client):
        self.name = name
        self.mcp_client = mcp_client
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """处理任务"""
        raise NotImplementedError


class DataCollectionAgent(WeiboAnalysisAgent):
    """数据收集智能体"""
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """收集微博数据"""
        print(f"[{self.name}] 开始收集微博数据...")
        
        try:
            # 调用MCP服务获取微博数据
            weibo_data = await self.mcp_client.call_tool(
                "Get Weibo Data", 
                {"limit": task.get("limit", 5)}
            )
            
            print(f"[{self.name}] 成功收集到 {len(weibo_data)} 条微博数据")
            return {
                "agent": self.name,
                "status": "success",
                "data": weibo_data
            }
        except Exception as e:
            print(f"[{self.name}] 数据收集失败: {e}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e)
            }


class SentimentAnalysisAgent(WeiboAnalysisAgent):
    """情感分析智能体"""
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """分析微博情感"""
        print(f"[{self.name}] 开始分析微博情感...")
        
        try:
            # 获取微博数据
            weibo_data = task.get("data", [])
            
            # 统计情感分布
            sentiment_counts = {"积极": 0, "中性": 0, "消极": 0}
            for weibo in weibo_data:
                sentiment = weibo.get("sentiment", "中性")
                if sentiment in sentiment_counts:
                    sentiment_counts[sentiment] += 1
            
            result = {
                "agent": self.name,
                "status": "success",
                "sentiment_distribution": sentiment_counts,
                "total_count": len(weibo_data)
            }
            
            print(f"[{self.name}] 情感分析完成: {sentiment_counts}")
            return result
        except Exception as e:
            print(f"[{self.name}] 情感分析失败: {e}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e)
            }


class ReportGenerationAgent(WeiboAnalysisAgent):
    """报告生成智能体"""
    
    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """生成分析报告"""
        print(f"[{self.name}] 开始生成分析报告...")
        
        try:
            # 获取情感分析结果
            sentiment_data = task.get("sentiment_distribution", {})
            total_count = task.get("total_count", 0)
            
            # 生成报告
            report = f"""
微博情感分析报告
================
总微博数: {total_count}

情感分布:
"""
            
            for sentiment, count in sentiment_data.items():
                percentage = (count / total_count * 100) if total_count > 0 else 0
                report += f"  {sentiment}: {count} 条 ({percentage:.1f}%)\n"
            
            # 分析主要情感倾向
            if sentiment_data:
                dominant_sentiment = max(sentiment_data, key=sentiment_data.get)
                report += f"\n主要情感倾向: {dominant_sentiment}\n"
            
            result = {
                "agent": self.name,
                "status": "success",
                "report": report
            }
            
            print(f"[{self.name}] 报告生成完成")
            return result
        except Exception as e:
            print(f"[{self.name}] 报告生成失败: {e}")
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e)
            }


class MultiAgentCoordinator:
    """多智能体协调器"""
    
    def __init__(self, mcp_client: Client):
        self.mcp_client = mcp_client
        self.agents = [
            DataCollectionAgent("数据收集智能体", mcp_client),
            SentimentAnalysisAgent("情感分析智能体", mcp_client),
            ReportGenerationAgent("报告生成智能体", mcp_client)
        ]
    
    async def run_analysis(self, limit: int = 5) -> Dict[str, Any]:
        """运行完整的微博情感分析流程"""
        print("开始多智能体微博情感分析流程...")
        
        # 第一步：数据收集
        data_task = {"limit": limit}
        data_result = await self.agents[0].process(data_task)
        
        if data_result["status"] != "success":
            return {"error": "数据收集失败", "details": data_result}
        
        # 第二步：情感分析
        analysis_task = {"data": data_result["data"]}
        analysis_result = await self.agents[1].process(analysis_task)
        
        if analysis_result["status"] != "success":
            return {"error": "情感分析失败", "details": analysis_result}
        
        # 第三步：生成报告
        report_task = {
            "sentiment_distribution": analysis_result["sentiment_distribution"],
            "total_count": analysis_result["total_count"]
        }
        report_result = await self.agents[2].process(report_task)
        
        if report_result["status"] != "success":
            return {"error": "报告生成失败", "details": report_result}
        
        # 返回最终结果
        return {
            "data_collection": data_result,
            "sentiment_analysis": analysis_result,
            "report_generation": report_result
        }


async def main():
    """主函数"""
    print("初始化MCP客户端...")
    
    # 创建MCP客户端
    async with Client("http://127.0.0.1:8001/sse") as mcp_client:
        # 创建协调器
        coordinator = MultiAgentCoordinator(mcp_client)
        
        # 运行分析流程
        result = await coordinator.run_analysis(limit=5)
        
        # 输出结果
        if "error" in result:
            print(f"分析流程出错: {result['error']}")
            print(f"详细信息: {result['details']}")
        else:
            print("\n" + "="*50)
            print("分析完成，最终报告:")
            print("="*50)
            print(result["report_generation"]["report"])


if __name__ == "__main__":
    asyncio.run(main())