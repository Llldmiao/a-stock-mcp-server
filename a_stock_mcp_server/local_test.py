#!/usr/bin/env python3
"""
A股MCP服务器本地测试版本
不依赖MCP包，直接测试核心功能
"""

import asyncio
import logging
from typing import Any, Dict

try:
    from .base import AStockBase
except ImportError:
    from base import AStockBase

logger = logging.getLogger(__name__)


class AStockLocalTest(AStockBase):
    """A股数据查询本地测试类"""

    def __init__(self):
        super().__init__()
        self.setup_handlers()

    def setup_handlers(self):
        """设置处理器"""
        self.tools = [
            {
                "name": "get_realtime_price",
                "description": "获取A股实时价格",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "股票代码，如000001（平安银行）",
                        }
                    },
                    "required": ["symbol"],
                },
            },
            {
                "name": "get_stock_info",
                "description": "获取股票基本信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {"symbol": {"type": "string", "description": "股票代码"}},
                    "required": ["symbol"],
                },
            },
            {
                "name": "get_market_summary",
                "description": "获取市场概况",
                "inputSchema": {"type": "object", "properties": {}},
            },
        ]

    def format_result(self, data: Any, result_type: str = "text") -> str:
        """格式化结果为字符串"""
        return str(data)

    def list_tools(self):
        """列出可用工具"""
        return self.tools

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """调用工具"""
        try:
            if name == "get_realtime_price":
                return await self.get_realtime_price(arguments)
            elif name == "get_stock_info":
                return await self.get_stock_info(arguments)
            elif name == "get_market_summary":
                return await self.get_market_summary(arguments)
            else:
                return f"未知工具: {name}"
        except Exception as e:
            logger.error(f"工具调用错误: {e}")
            return f"错误: {str(e)}"

    async def get_realtime_price(self, args: Dict[str, Any]) -> str:
        """获取实时价格"""
        symbol = args.get("symbol", "")

        # 验证股票代码
        if not self.validate_symbol(symbol):
            return f"无效的股票代码格式: {symbol}，请使用6位数字代码"

        try:
            # 尝试使用AKShare获取真实数据
            import akshare as ak

            # 获取实时行情
            stock_realtime = ak.stock_zh_a_spot_em()

            # 查找指定股票
            stock_data = stock_realtime[stock_realtime["代码"] == symbol]

            if stock_data.empty:
                return f"未找到股票代码: {symbol}"

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

            return result.strip()

        except ImportError:
            # 如果没有安装AKShare，返回模拟数据
            return self._get_mock_realtime_price(symbol)
        except Exception as e:
            logger.error(f"获取实时价格失败: {e}")
            return f"获取数据失败: {str(e)}"

    def _get_mock_realtime_price(self, symbol: str) -> str:
        """获取模拟实时价格数据"""
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
            "timestamp": "2024-01-01 15:00:00",
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

        return result.strip()

    async def get_stock_info(self, args: Dict[str, Any]) -> str:
        """获取股票基本信息"""
        symbol = args.get("symbol", "")

        try:
            import akshare as ak

            # 获取股票基本信息
            stock_info = ak.stock_individual_info_em(symbol=symbol)

            result = f"=== {symbol} 基本信息 ===\n"
            for _, row in stock_info.iterrows():
                result += f"{row['item']}: {row['value']}\n"

            return result.strip()

        except ImportError:
            # 如果没有安装AKShare，返回模拟数据
            return self._get_mock_stock_info(symbol)
        except Exception as e:
            logger.error(f"获取股票信息失败: {e}")
            return f"获取数据失败: {str(e)}"

    def _get_mock_stock_info(self, symbol: str) -> str:
        """获取模拟股票信息"""
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

        return info.strip()

    async def get_market_summary(self, args: Dict[str, Any]) -> str:
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

            return result.strip()

        except ImportError:
            # 如果没有安装AKShare，返回模拟数据
            return self._get_mock_market_summary()
        except Exception as e:
            logger.error(f"获取市场概况失败: {e}")
            return f"获取数据失败: {str(e)}"

    def _get_mock_market_summary(self) -> str:
        """获取模拟市场概况"""
        summary = """
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

        return summary.strip()


async def demo_usage():
    """演示使用"""
    print("🚀 A股MCP服务器本地测试")
    print("=" * 50)

    # 创建测试实例
    server = AStockLocalTest()

    # 显示可用工具
    print("\n📋 可用工具:")
    tools = server.list_tools()
    for tool in tools:
        print(f"- {tool['name']}: {tool['description']}")

    print("\n" + "=" * 50)

    # 测试各个功能
    test_cases = [
        ("get_realtime_price", {"symbol": "000001"}),
        ("get_stock_info", {"symbol": "000001"}),
        ("get_market_summary", {}),
    ]

    for tool_name, args in test_cases:
        print(f"\n🔍 测试工具: {tool_name}")
        print("-" * 30)
        result = await server.call_tool(tool_name, args)
        print(result)
        print("\n" + "=" * 50)

    print("\n✅ 本地测试完成！")
    print("\n💡 提示:")
    print("- 如果看到模拟数据，说明AKShare未安装")
    print("- 安装AKShare: pip3 install akshare")
    print("- 安装后重新运行将获取真实数据")


if __name__ == "__main__":
    asyncio.run(demo_usage())
