#!/usr/bin/env python3
"""
A股实时行情MCP服务器
支持查询A股实时价格、基本信息、市场概况等
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AStockMCPServer:
    def __init__(self):
        self.server = Server("a-stock-realtime")
        self.setup_handlers()
        
    def setup_handlers(self):
        """设置MCP处理器"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """列出可用工具"""
            return [
                Tool(
                    name="get_realtime_price",
                    description="获取A股实时价格",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "股票代码，如000001（平安银行）"
                            },
                            "market": {
                                "type": "string", 
                                "description": "市场类型：sz（深市）/sse（沪市）",
                                "default": "sz"
                            }
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_stock_info",
                    description="获取股票基本信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "股票代码"
                            }
                        },
                        "required": ["symbol"]
                    }
                ),
                Tool(
                    name="get_market_summary",
                    description="获取市场概况（上证、深证指数等）",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "market": {
                                "type": "string",
                                "description": "市场类型：sz/sse/all",
                                "default": "all"
                            }
                        }
                    }
                ),
                Tool(
                    name="search_stock",
                    description="根据股票名称搜索股票代码",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "股票名称或简称"
                            }
                        },
                        "required": ["name"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """处理工具调用"""
            try:
                if name == "get_realtime_price":
                    return await self.get_realtime_price(arguments)
                elif name == "get_stock_info":
                    return await self.get_stock_info(arguments)
                elif name == "get_market_summary":
                    return await self.get_market_summary(arguments)
                elif name == "search_stock":
                    return await self.search_stock(arguments)
                else:
                    return [TextContent(type="text", text=f"未知工具: {name}")]
            except Exception as e:
                logger.error(f"工具调用错误: {e}")
                return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    async def get_realtime_price(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取实时价格"""
        symbol = args.get("symbol", "")
        market = args.get("market", "sz")
        
        # 这里集成AKShare或其他数据源
        # 示例数据，实际需要调用真实API
        mock_data = {
            "symbol": symbol,
            "name": "示例股票",
            "current_price": 10.50,
            "change": 0.15,
            "change_percent": 1.45,
            "volume": 1234567,
            "turnover": 12963000,
            "high": 10.80,
            "low": 10.20,
            "open": 10.35,
            "prev_close": 10.35,
            "timestamp": "2024-01-01 15:00:00"
        }
        
        result = f"""
股票代码: {mock_data['symbol']}
股票名称: {mock_data['name']}
当前价格: ¥{mock_data['current_price']}
涨跌额: {mock_data['change']:+.2f}
涨跌幅: {mock_data['change_percent']:+.2f}%
成交量: {mock_data['volume']:,}
成交额: ¥{mock_data['turnover']:,}
最高价: ¥{mock_data['high']}
最低价: ¥{mock_data['low']}
开盘价: ¥{mock_data['open']}
昨收价: ¥{mock_data['prev_close']}
更新时间: {mock_data['timestamp']}
        """
        
        return [TextContent(type="text", text=result.strip())]
    
    async def get_stock_info(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取股票基本信息"""
        symbol = args.get("symbol", "")
        
        # 示例数据
        info = f"""
股票代码: {symbol}
股票名称: 示例股票
所属行业: 银行
上市日期: 1991-04-03
总股本: 194.59亿股
流通股本: 194.59亿股
市盈率: 4.5
市净率: 0.6
        """
        
        return [TextContent(type="text", text=info.strip())]
    
    async def get_market_summary(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取市场概况"""
        market = args.get("market", "all")
        
        # 示例数据
        summary = f"""
=== 市场概况 ===
上证指数: 3,234.56 (+12.34, +0.38%)
深证成指: 10,567.89 (-23.45, -0.22%)
创业板指: 2,156.78 (+5.67, +0.26%)
科创50: 987.65 (-8.90, -0.89%)

涨跌统计:
上涨: 1,234家
下跌: 2,345家
平盘: 123家

成交量: 3,456.78亿
成交额: 4,567.89亿
更新时间: 2024-01-01 15:00:00
        """
        
        return [TextContent(type="text", text=summary.strip())]
    
    async def search_stock(self, args: Dict[str, Any]) -> List[TextContent]:
        """搜索股票"""
        name = args.get("name", "")
        
        # 示例搜索结果
        results = f"""
搜索关键词: {name}

搜索结果:
1. 平安银行 (000001) - 银行
2. 招商银行 (600036) - 银行  
3. 工商银行 (601398) - 银行
4. 建设银行 (601939) - 银行
5. 农业银行 (601288) - 银行
        """
        
        return [TextContent(type="text", text=results.strip())]

async def main():
    """主函数"""
    app = AStockMCPServer()
    
    # 使用stdio传输
    async with stdio_server() as (read_stream, write_stream):
        await app.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="a-stock-realtime",
                server_version="1.0.0",
                capabilities=app.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
