#!/usr/bin/env python3
"""
A股实时行情MCP服务器 - 集成AKShare数据源
需要安装: pip install akshare mcp
"""

import asyncio
import logging
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.types import (
    Tool,
    TextContent,
)
from .base import AStockBase

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AStockMCPServerWithAKShare(AStockBase):
    def __init__(self):
        super().__init__()
        self.server = Server("a-stock-realtime-akshare")
        self.setup_handlers()

    def format_result(self, data: Any, result_type: str = "text") -> List[TextContent]:
        """格式化结果为MCP TextContent列表"""
        return [TextContent(type="text", text=str(data))]

    def setup_handlers(self):
        """设置MCP处理器"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """列出可用工具"""
            return [
                Tool(
                    name="get_realtime_price",
                    description="获取A股实时价格（使用AKShare）",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "股票代码，如000001（平安银行）",
                            }
                        },
                        "required": ["symbol"],
                    },
                ),
                Tool(
                    name="get_stock_info",
                    description="获取股票基本信息",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "股票代码"}
                        },
                        "required": ["symbol"],
                    },
                ),
                Tool(
                    name="get_market_summary",
                    description="获取市场概况（上证、深证指数等）",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="get_stock_history",
                    description="获取股票历史数据",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "股票代码"},
                            "period": {
                                "type": "string",
                                "description": "周期：daily/weekly/monthly",
                                "default": "daily",
                            },
                            "start_date": {
                                "type": "string",
                                "description": "开始日期，格式：20240101",
                            },
                            "end_date": {
                                "type": "string",
                                "description": "结束日期，格式：20241231",
                            },
                        },
                        "required": ["symbol"],
                    },
                ),
                Tool(
                    name="get_financial_data",
                    description="获取财务数据",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string", "description": "股票代码"},
                            "report_type": {
                                "type": "string",
                                "description": "报告类型：income/balance/cashflow",
                                "default": "income",
                            },
                        },
                        "required": ["symbol"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[TextContent]:
            """处理工具调用"""
            try:
                if name == "get_realtime_price":
                    return await self.get_realtime_price(arguments)
                elif name == "get_stock_info":
                    return await self.get_stock_info(arguments)
                elif name == "get_market_summary":
                    return await self.get_market_summary(arguments)
                elif name == "get_stock_history":
                    return await self.get_stock_history(arguments)
                elif name == "get_financial_data":
                    return await self.get_financial_data(arguments)
                else:
                    return [TextContent(type="text", text=f"未知工具: {name}")]
            except Exception as e:
                logger.error(f"工具调用错误: {e}")
                return [TextContent(type="text", text=f"错误: {str(e)}")]

    async def get_realtime_price(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取实时价格 - 使用AKShare"""
        symbol = args.get("symbol", "")

        # 验证股票代码
        if not self.validate_symbol(symbol):
            return [TextContent(type="text", text=f"无效的股票代码格式: {symbol}，请使用6位数字代码")]

        try:
            # 使用AKShare获取实时数据
            import akshare as ak

            # 获取实时行情
            stock_realtime = ak.stock_zh_a_spot_em()

            # 查找指定股票
            stock_data = stock_realtime[stock_realtime["代码"] == symbol]

            if stock_data.empty:
                return [TextContent(type="text", text=f"未找到股票代码: {symbol}")]

            stock_info = stock_data.iloc[0]

            result = f"""
股票代码: {self.safe_get_field(stock_info, '代码', symbol)}
股票名称: {self.safe_get_field(stock_info, '名称', 'N/A')}
当前价格: {self.format_price(self.safe_get_field(stock_info, '最新价'))}
涨跌额: {self.safe_get_field(stock_info, '涨跌额', 0):+.2f}
涨跌幅: {self.format_percentage(self.safe_get_field(stock_info, '涨跌幅'))}
成交量: {self.format_number(self.safe_get_field(stock_info, '成交量'))}
成交额: {self.format_price(self.safe_get_field(stock_info, '成交额'))}
最高价: {self.format_price(self.safe_get_field(stock_info, '最高'))}
最低价: {self.format_price(self.safe_get_field(stock_info, '最低'))}
开盘价: {self.format_price(self.safe_get_field(stock_info, '今开'))}
昨收价: {self.format_price(self.safe_get_field(stock_info, '昨收'))}
换手率: {self.format_percentage(self.safe_get_field(stock_info, '换手率'))}
市盈率: {self.safe_get_field(stock_info, '市盈率-动态', 'N/A')}
市净率: {self.safe_get_field(stock_info, '市净率', 'N/A')}
更新时间: {self.safe_get_field(stock_info, '时间', 'N/A')}
            """

            return [TextContent(type="text", text=result.strip())]

        except ImportError as e:
            logger.error(f"AKShare未安装: {e}")
            return [
                TextContent(type="text", text="错误: AKShare未安装，请运行 pip install akshare")
            ]
        except Exception as e:
            logger.error(f"获取实时价格失败: {e}")
            return [TextContent(type="text", text=f"获取数据失败: {str(e)}")]

    async def get_stock_info(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取股票基本信息"""
        symbol = args.get("symbol", "")

        try:
            import akshare as ak

            # 获取股票基本信息
            stock_info = ak.stock_individual_info_em(symbol=symbol)

            result = f"""
=== {symbol} 基本信息 ===
"""
            for _, row in stock_info.iterrows():
                result += f"{row['item']}: {row['value']}\n"

            return [TextContent(type="text", text=result.strip())]

        except Exception as e:
            logger.error(f"获取股票信息失败: {e}")
            return [TextContent(type="text", text=f"获取数据失败: {str(e)}")]

    async def get_market_summary(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取市场概况"""
        try:
            import akshare as ak

            # 获取大盘指数
            index_data = ak.stock_zh_index_spot_em()

            result = "=== 市场概况 ===\n"
            for _, row in index_data.iterrows():
                result += (
                    f"{row['名称']}: {row['最新价']} "
                    f"({row['涨跌额']:+.2f}, {row['涨跌幅']:+.2f}%)\n"
                )

            return [TextContent(type="text", text=result.strip())]

        except Exception as e:
            logger.error(f"获取市场概况失败: {e}")
            return [TextContent(type="text", text=f"获取数据失败: {str(e)}")]

    async def get_stock_history(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取股票历史数据"""
        symbol = args.get("symbol", "")
        period = args.get("period", "daily")
        start_date = args.get("start_date", "20240101")
        end_date = args.get("end_date", "20241231")

        try:
            import akshare as ak

            # 获取历史数据
            if period == "daily":
                hist_data = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                )
            elif period == "weekly":
                hist_data = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="weekly",
                    start_date=start_date,
                    end_date=end_date,
                )
            elif period == "monthly":
                hist_data = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="monthly",
                    start_date=start_date,
                    end_date=end_date,
                )
            else:
                return [TextContent(type="text", text="不支持的周期类型")]

            if hist_data.empty:
                return [TextContent(type="text", text=f"未找到 {symbol} 的历史数据")]

            # 格式化输出最近10条数据
            recent_data = hist_data.tail(10)

            result = f"=== {symbol} 历史数据（最近10条）===\n"
            result += "日期\t开盘\t收盘\t最高\t最低\t成交量\t成交额\n"

            for _, row in recent_data.iterrows():
                result += (
                    f"{row['日期']}\t{row['开盘']}\t{row['收盘']}\t{row['最高']}\t{row['最低']}\t"
                    f"{row['成交量']:,}\t{row['成交额']:,}\n"
                )

            return [TextContent(type="text", text=result.strip())]

        except Exception as e:
            logger.error(f"获取历史数据失败: {e}")
            return [TextContent(type="text", text=f"获取数据失败: {str(e)}")]

    async def get_financial_data(self, args: Dict[str, Any]) -> List[TextContent]:
        """获取财务数据"""
        symbol = args.get("symbol", "")
        report_type = args.get("report_type", "income")

        try:
            import akshare as ak

            if report_type == "income":
                # 利润表
                financial_data = ak.stock_financial_abstract(symbol=symbol)
            elif report_type == "balance":
                # 资产负债表
                financial_data = ak.stock_balance_sheet_by_report_em(symbol=symbol)
            elif report_type == "cashflow":
                # 现金流量表
                financial_data = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
            else:
                return [TextContent(type="text", text="不支持的财务数据类型")]

            if financial_data.empty:
                return [TextContent(type="text", text=f"未找到 {symbol} 的财务数据")]

            result = f"=== {symbol} {report_type} 财务数据 ===\n"
            result += financial_data.to_string()

            return [TextContent(type="text", text=result.strip())]

        except Exception as e:
            logger.error(f"获取财务数据失败: {e}")
            return [TextContent(type="text", text=f"获取数据失败: {str(e)}")]


async def main():
    """主函数"""
    app = AStockMCPServerWithAKShare()

    # 创建通知选项
    notification_options = NotificationOptions(
        prompts_changed=False, resources_changed=False, tools_changed=False
    )

    # 使用stdio传输
    async with stdio_server() as (read_stream, write_stream):
        await app.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="a-stock-realtime-akshare",
                server_version="1.0.0",
                capabilities=app.server.get_capabilities(
                    notification_options=notification_options,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
