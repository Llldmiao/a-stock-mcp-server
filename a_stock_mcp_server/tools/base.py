"""
工具基类
定义所有MCP工具的基础接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging

from mcp.types import Tool, TextContent

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """工具基类"""

    def __init__(self, data_source_manager):
        self.data_source_manager = data_source_manager
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    @abstractmethod
    def tool_definition(self) -> Tool:
        """工具定义"""
        pass

    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """执行工具"""
        try:
            # 验证参数
            self._validate_arguments(arguments)

            # 获取数据
            data = await self._fetch_data(arguments)

            # 格式化数据
            return self._format_data(data)

        except Exception as e:
            self.logger.error(f"工具执行失败: {e}")
            return [TextContent(type="text", text=f"错误: {str(e)}")]

    @abstractmethod
    async def _fetch_data(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """从数据源获取数据"""
        pass

    @abstractmethod
    def _format_data(self, data: Dict[str, Any]) -> List[TextContent]:
        """格式化数据为MCP响应"""
        pass

    def _validate_arguments(self, arguments: Dict[str, Any]):
        """验证参数（子类可以重写）"""
        pass

    def _validate_symbol(self, symbol: str) -> bool:
        """验证股票代码格式"""
        if not symbol or not isinstance(symbol, str):
            return False
        # 检查是否为6位数字
        return symbol.isdigit() and len(symbol) == 6

    def _format_price(self, price: Any) -> str:
        """格式化价格"""
        try:
            if price is None or price == "":
                return "N/A"
            return f"¥{float(price):.2f}"
        except (ValueError, TypeError):
            return str(price)

    def _format_percentage(self, value: Any) -> str:
        """格式化百分比"""
        try:
            if value is None or value == "":
                return "N/A"
            return f"{float(value):+.2f}%"
        except (ValueError, TypeError):
            return str(value)

    def _format_number(self, value: Any) -> str:
        """格式化数字（添加千分位分隔符）"""
        try:
            if value is None or value == "":
                return "N/A"
            return f"{int(float(value)):,}"
        except (ValueError, TypeError):
            return str(value)
