"""
A股实时行情MCP服务器
基于Model Context Protocol的A股数据查询工具
"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("a-stock-mcp-server")
except PackageNotFoundError:
    __version__ = "1.0.0"

__author__ = "Llldmiao"
__email__ = "llldmiao@users.noreply.github.com"

from .local_test import AStockLocalTest
from .__main__ import AStockMCPServerWithAKShare
from .base import AStockBase

__all__ = ["AStockLocalTest", "AStockMCPServerWithAKShare", "AStockBase"]
