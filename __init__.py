"""
A股实时行情MCP服务器
基于Model Context Protocol的A股数据查询工具
"""

__version__ = "1.0.0"
__author__ = "Financial Tools Developer"
__email__ = "financial-tools@example.com"

from .local_test import AStockLocalTest

__all__ = ["AStockLocalTest"]
