"""
实时价格工具
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent

from .base import BaseTool


class RealtimePriceTool(BaseTool):
    """实时价格工具"""

    @property
    def tool_definition(self) -> Tool:
        return Tool(
            name="get_realtime_price",
            description="获取A股实时价格",
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
        )

    def _validate_arguments(self, arguments: Dict[str, Any]):
        """验证参数"""
        symbol = arguments.get("symbol", "")
        if not self._validate_symbol(symbol):
            raise ValueError(f"无效的股票代码格式: {symbol}，请使用6位数字代码")

    async def _fetch_data(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """从数据源获取数据"""
        symbol = arguments["symbol"]
        return await self.data_source_manager.get_data(
            "get_realtime_price", symbol=symbol
        )

    def _format_data(self, data: Dict[str, Any]) -> List[TextContent]:
        """格式化数据为MCP响应"""
        result = f"""
股票代码: {data.get('symbol', 'N/A')}
股票名称: {data.get('name', 'N/A')}
当前价格: {self._format_price(data.get('current_price'))}
涨跌额: {data.get('change', 0):+.2f}
涨跌幅: {self._format_percentage(data.get('change_percent'))}
成交量: {self._format_number(data.get('volume'))}
成交额: {self._format_price(data.get('turnover'))}
最高价: {self._format_price(data.get('high'))}
最低价: {self._format_price(data.get('low'))}
开盘价: {self._format_price(data.get('open'))}
昨收价: {self._format_price(data.get('prev_close'))}
换手率: {self._format_percentage(data.get('turnover_rate'))}
市盈率: {data.get('pe_ratio', 'N/A')}
市净率: {data.get('pb_ratio', 'N/A')}
更新时间: {data.get('timestamp', 'N/A')}
数据源: {data.get('source', 'N/A')}
        """

        return [TextContent(type="text", text=result.strip())]
