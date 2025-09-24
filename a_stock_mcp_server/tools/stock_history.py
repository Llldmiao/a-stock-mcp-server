"""
股票历史数据工具
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent

from .base import BaseTool


class StockHistoryTool(BaseTool):
    """股票历史数据工具"""
    
    @property
    def tool_definition(self) -> Tool:
        return Tool(
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
        )
    
    def _validate_arguments(self, arguments: Dict[str, Any]):
        """验证参数"""
        symbol = arguments.get("symbol", "")
        if not self._validate_symbol(symbol):
            raise ValueError(f"无效的股票代码格式: {symbol}，请使用6位数字代码")
        
        period = arguments.get("period", "daily")
        if period not in ["daily", "weekly", "monthly"]:
            raise ValueError("不支持的周期类型，请使用 daily/weekly/monthly")
    
    async def _fetch_data(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """从数据源获取数据"""
        symbol = arguments["symbol"]
        kwargs = {
            "period": arguments.get("period", "daily"),
            "start_date": arguments.get("start_date", "20240101"),
            "end_date": arguments.get("end_date", "20241231"),
        }
        return await self.data_source_manager.get_data("get_stock_history", symbol=symbol, **kwargs)
    
    def _format_data(self, data: Dict[str, Any]) -> List[TextContent]:
        """格式化数据为MCP响应"""
        symbol = data.get("symbol", "N/A")
        period = data.get("period", "N/A")
        history_list = data.get("history", [])
        
        if not history_list:
            return [TextContent(type="text", text=f"未找到 {symbol} 的历史数据")]
        
        # 格式化输出最近50条数据
        recent_data = history_list[-50:] if len(history_list) > 50 else history_list
        
        result = f"=== {symbol} 历史数据（最近{len(recent_data)}条）===\n"
        result += "日期\t开盘\t收盘\t最高\t最低\t成交量\t成交额\n"
        
        for item in recent_data:
            date = item.get("date", "N/A")
            open_price = self._format_price(item.get("open"))
            close_price = self._format_price(item.get("close"))
            high_price = self._format_price(item.get("high"))
            low_price = self._format_price(item.get("low"))
            volume = self._format_number(item.get("volume"))
            turnover = self._format_number(item.get("turnover"))
            
            result += f"{date}\t{open_price}\t{close_price}\t{high_price}\t{low_price}\t{volume}\t{turnover}\n"
        
        result += f"\n数据源: {data.get('source', 'N/A')}"
        
        return [TextContent(type="text", text=result.strip())]
