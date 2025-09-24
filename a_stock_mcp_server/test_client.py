"""
测试客户端
用于测试新的多数据源架构
"""

import asyncio
import logging
from typing import Dict, Any

from .data_sources import DataSourceManager, AKShareDataSource, DataSourceConfig
from .tools import (
    RealtimePriceTool,
    StockInfoTool,
    MarketSummaryTool,
    StockHistoryTool,
    FinancialDataTool,
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AStockTestClient:
    """A股测试客户端"""
    
    def __init__(self):
        self.data_source_manager = DataSourceManager()
        self.tools = []
        
        # 初始化数据源
        self._setup_data_sources()
        
        # 初始化工具
        self._setup_tools()
    
    def _setup_data_sources(self):
        """设置数据源"""
        # 创建AKShare数据源
        akshare_config = DataSourceConfig(
            name="akshare",
            enabled=True,
            priority=1,
            timeout=30,
            retry_count=3,
            cache_ttl=300
        )
        
        akshare_source = AKShareDataSource(akshare_config)
        self.data_source_manager.register_source(akshare_source)
        
        logger.info("数据源初始化完成")
    
    def _setup_tools(self):
        """设置工具"""
        self.tools = [
            RealtimePriceTool(self.data_source_manager),
            StockInfoTool(self.data_source_manager),
            MarketSummaryTool(self.data_source_manager),
            StockHistoryTool(self.data_source_manager),
            FinancialDataTool(self.data_source_manager),
        ]
        
        logger.info(f"工具初始化完成，共{len(self.tools)}个工具")
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """调用工具"""
        try:
            # 查找对应的工具
            tool = None
            for t in self.tools:
                if t.tool_definition.name == name:
                    tool = t
                    break
            
            if tool is None:
                return f"未知工具: {name}"
            
            # 执行工具
            result = await tool.execute(arguments)
            return result[0].text if result else "无结果"
            
        except Exception as e:
            logger.error(f"工具调用错误: {e}")
            return f"错误: {str(e)}"
    
    def list_tools(self):
        """列出可用工具"""
        return [tool.tool_definition for tool in self.tools]
    
    async def health_check(self):
        """健康检查"""
        return await self.data_source_manager.health_check_all()
    
    def get_source_info(self):
        """获取数据源信息"""
        return self.data_source_manager.get_source_info()


async def demo_usage():
    """演示使用"""
    print("🚀 A股MCP服务器测试")
    print("=" * 40)

    # 创建测试客户端
    client = AStockTestClient()

    # 健康检查
    print("\n🏥 健康检查:")
    health_status = await client.health_check()
    for source_name, status in health_status.items():
        status_text = "✅ 正常" if status else "❌ 异常"
        print(f"- {source_name}: {status_text}")

    # 简单测试一个功能
    print("\n🔍 测试实时价格:")
    result = await client.call_tool("get_realtime_price", {"symbol": "000001"})
    print(result[:200] + "..." if len(result) > 200 else result)

    print("\n✅ 测试完成！")


async def quick_test():
    """快速测试"""
    print("🚀 快速测试")
    print("=" * 20)

    client = AStockTestClient()
    
    # 只做健康检查
    health_status = await client.health_check()
    all_healthy = all(health_status.values())
    
    if all_healthy:
        print("✅ 所有数据源正常")
    else:
        print("❌ 部分数据源异常")
        for source_name, status in health_status.items():
            if not status:
                print(f"  - {source_name}: 异常")
    
    print("测试完成！")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        asyncio.run(quick_test())
    else:
        asyncio.run(demo_usage())
