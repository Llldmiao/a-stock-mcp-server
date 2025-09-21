#!/usr/bin/env python3
"""
A股MCP服务器基础类
提取公共逻辑，减少代码重复
"""

import logging
from typing import Any, List, Union
from abc import ABC, abstractmethod

# 配置日志
logger = logging.getLogger(__name__)


class AStockBase(ABC):
    """A股数据查询基础类"""

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """设置日志"""
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)

    @abstractmethod
    def format_result(self, data: Any, result_type: str = "text") -> Union[str, List]:
        """格式化结果 - 子类需要实现"""
        pass

    async def safe_get_data(self, func, *args, **kwargs) -> Any:
        """安全获取数据，包含错误处理"""
        try:
            return await func(*args, **kwargs)
        except ImportError as e:
            logger.warning(f"依赖包未安装: {e}")
            return None
        except Exception as e:
            logger.error(f"获取数据失败: {e}")
            raise

    def validate_symbol(self, symbol: str) -> bool:
        """验证股票代码格式"""
        if not symbol or not isinstance(symbol, str):
            return False
        # 检查是否为6位数字
        return symbol.isdigit() and len(symbol) == 6

    def safe_get_field(self, data: Any, field: str, default: Any = "N/A") -> Any:
        """安全获取字段值"""
        try:
            if hasattr(data, "get"):
                return data.get(field, default)
            elif hasattr(data, field):
                return getattr(data, field, default)
            else:
                return default
        except (KeyError, AttributeError):
            return default

    def format_price(self, price: Any) -> str:
        """格式化价格"""
        try:
            if price is None or price == "":
                return "N/A"
            return f"¥{float(price):.2f}"
        except (ValueError, TypeError):
            return str(price)

    def format_percentage(self, value: Any) -> str:
        """格式化百分比"""
        try:
            if value is None or value == "":
                return "N/A"
            return f"{float(value):+.2f}%"
        except (ValueError, TypeError):
            return str(value)

    def format_number(self, value: Any) -> str:
        """格式化数字（添加千分位分隔符）"""
        try:
            if value is None or value == "":
                return "N/A"
            return f"{int(float(value)):,}"
        except (ValueError, TypeError):
            return str(value)
