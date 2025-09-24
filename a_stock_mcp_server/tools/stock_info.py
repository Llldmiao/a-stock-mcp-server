"""
股票信息工具
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent

from .base import BaseTool


class StockInfoTool(BaseTool):
    """股票信息工具"""
    
    @property
    def tool_definition(self) -> Tool:
        return Tool(
            name="get_stock_info",
            description="获取股票基本信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "股票代码"}
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
        return await self.data_source_manager.get_data("get_stock_info", symbol=symbol)
    
    def _format_data(self, data: Dict[str, Any]) -> List[TextContent]:
        """格式化数据为MCP响应"""
        symbol = data.get("symbol", "N/A")
        info_dict = data.get("info", {})
        
        result = f"=== {symbol} 基本信息 ===\n"
        for key, value in info_dict.items():
            result += f"{key}: {value}\n"
        
        result += f"\n数据源: {data.get('source', 'N/A')}"
        
        return [TextContent(type="text", text=result.strip())]
