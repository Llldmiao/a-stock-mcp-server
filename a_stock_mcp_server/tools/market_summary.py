"""
市场概况工具
"""

from typing import Dict, Any, List
from mcp.types import Tool, TextContent

from .base import BaseTool


class MarketSummaryTool(BaseTool):
    """市场概况工具"""

    @property
    def tool_definition(self) -> Tool:
        return Tool(
            name="get_market_summary",
            description="获取市场概况（上证、深证指数等）",
            inputSchema={"type": "object", "properties": {}},
        )

    async def _fetch_data(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """从数据源获取数据"""
        return await self.data_source_manager.get_data("get_market_summary")

    def _format_data(self, data: Dict[str, Any]) -> List[TextContent]:
        """格式化数据为MCP响应"""
        summary_list = data.get("summary", [])

        result = "=== 市场概况 ===\n"
        for item in summary_list:
            name = item.get("name", "N/A")
            price = item.get("price", "N/A")
            change = item.get("change", 0)
            change_percent = item.get("change_percent", 0)

            result += f"{name}: {price} ({change:+.2f}, {change_percent:+.2f}%)\n"

        result += f"\n数据源: {data.get('source', 'N/A')}"

        return [TextContent(type="text", text=result.strip())]
