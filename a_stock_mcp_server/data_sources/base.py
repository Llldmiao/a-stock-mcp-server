"""
数据源基类
定义所有数据源必须实现的接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class DataSourceConfig:
    """数据源配置"""

    name: str
    enabled: bool = True
    priority: int = 1  # 优先级，数字越小优先级越高
    timeout: int = 30
    retry_count: int = 3
    cache_ttl: int = 300  # 缓存时间（秒）
    max_requests_per_minute: int = 60  # 每分钟最大请求数


class BaseDataSource(ABC):
    """数据源基类"""

    def __init__(self, config: DataSourceConfig):
        self.config = config
        self.name = config.name
        self.logger = logging.getLogger(f"{__name__}.{self.name}")

    @abstractmethod
    async def get_realtime_price(self, symbol: str) -> Dict[str, Any]:
        """获取实时价格"""
        pass

    @abstractmethod
    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """获取股票信息"""
        pass

    @abstractmethod
    async def get_market_summary(self) -> Dict[str, Any]:
        """获取市场概况"""
        pass

    @abstractmethod
    async def get_stock_history(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取历史数据"""
        pass

    @abstractmethod
    async def get_financial_data(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """获取财务数据"""
        pass

    async def health_check(self) -> bool:
        """健康检查"""
        try:
            # 简单的健康检查实现
            await self.get_market_summary()
            return True
        except Exception as e:
            self.logger.warning(f"健康检查失败: {e}")
            return False

    def get_config(self) -> DataSourceConfig:
        """获取配置"""
        return self.config

    def is_enabled(self) -> bool:
        """检查是否启用"""
        return self.config.enabled

    def get_priority(self) -> int:
        """获取优先级"""
        return self.config.priority
