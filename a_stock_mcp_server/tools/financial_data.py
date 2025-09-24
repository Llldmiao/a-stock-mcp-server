"""
财务数据工具
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent

from .base import BaseTool


class FinancialDataTool(BaseTool):
    """财务数据工具"""

    @property
    def tool_definition(self) -> Tool:
        return Tool(
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
        )

    def _validate_arguments(self, arguments: Dict[str, Any]):
        """验证参数"""
        symbol = arguments.get("symbol", "")
        if not self._validate_symbol(symbol):
            raise ValueError(f"无效的股票代码格式: {symbol}，请使用6位数字代码")

        report_type = arguments.get("report_type", "income")
        if report_type not in ["income", "balance", "cashflow"]:
            raise ValueError("不支持的财务数据类型，请使用 income/balance/cashflow")

    async def _fetch_data(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """从数据源获取数据"""
        symbol = arguments["symbol"]
        kwargs = {
            "report_type": arguments.get("report_type", "income"),
        }
        return await self.data_source_manager.get_data(
            "get_financial_data", symbol=symbol, **kwargs
        )

    def _format_data(self, data: Dict[str, Any]) -> List[TextContent]:
        """格式化数据为MCP响应"""
        symbol = data.get("symbol", "N/A")
        report_type = data.get("report_type", "N/A")
        financial_data = data.get("data", [])

        if not financial_data:
            return [TextContent(type="text", text=f"未找到 {symbol} 的财务数据")]

        # 根据报告类型设置标题
        type_names = {"income": "利润表", "balance": "资产负债表", "cashflow": "现金流量表"}
        type_name = type_names.get(report_type, report_type)

        result = f"=== {symbol} {type_name} ===\n"

        # 格式化财务数据
        for item in financial_data:
            if isinstance(item, dict):
                for key, value in item.items():
                    result += f"{key}: {value}\n"
            else:
                result += f"{item}\n"

        result += f"\n数据源: {data.get('source', 'N/A')}"

        return [TextContent(type="text", text=result.strip())]
