"""
数据源模块
支持多数据源的A股数据查询
"""

from .base import BaseDataSource, DataSourceConfig
from .source_manager import DataSourceManager
from .akshare_source import AKShareDataSource

__all__ = [
    "BaseDataSource",
    "DataSourceConfig", 
    "DataSourceManager",
    "AKShareDataSource",
]
