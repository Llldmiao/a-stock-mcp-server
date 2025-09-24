"""
数据源管理器
负责管理多个数据源，实现故障转移和负载均衡
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import hashlib
import json

from .base import BaseDataSource, DataSourceConfig

logger = logging.getLogger(__name__)


class CacheManager:
    """简单的内存缓存管理器"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def _generate_key(self, method: str, symbol: str = None, **kwargs) -> str:
        """生成缓存键"""
        data = {
            "method": method,
            "symbol": symbol,
            **kwargs
        }
        key_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """获取缓存数据"""
        if key in self._cache:
            cache_data = self._cache[key]
            if datetime.now() < cache_data["expires_at"]:
                return cache_data["data"]
            else:
                # 过期，删除缓存
                del self._cache[key]
        return None
    
    async def set(self, key: str, data: Dict[str, Any], ttl: int):
        """设置缓存数据"""
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = {
            "data": data,
            "expires_at": expires_at
        }
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self.sources: List[BaseDataSource] = []
        self.cache_manager = CacheManager()
        self.logger = logging.getLogger(__name__)
    
    def register_source(self, source: BaseDataSource):
        """注册数据源"""
        if not isinstance(source, BaseDataSource):
            raise ValueError("数据源必须继承自BaseDataSource")
        
        self.sources.append(source)
        # 按优先级排序
        self.sources.sort(key=lambda x: x.get_priority())
        self.logger.info(f"注册数据源: {source.name} (优先级: {source.get_priority()})")
    
    def get_enabled_sources(self) -> List[BaseDataSource]:
        """获取启用的数据源"""
        return [source for source in self.sources if source.is_enabled()]
    
    def _generate_cache_key(self, method: str, symbol: str = None, **kwargs) -> str:
        """生成缓存键"""
        return self.cache_manager._generate_key(method, symbol, **kwargs)
    
    async def get_data(self, method: str, symbol: str = None, **kwargs) -> Dict[str, Any]:
        """获取数据，支持故障转移"""
        enabled_sources = self.get_enabled_sources()
        if not enabled_sources:
            raise Exception("没有可用的数据源")
        
        # 先检查缓存
        cache_key = self._generate_cache_key(method, symbol, **kwargs)
        cached_data = await self.cache_manager.get(cache_key)
        if cached_data:
            self.logger.debug(f"从缓存获取数据: {method}")
            return cached_data
        
        # 尝试各个数据源
        last_error = None
        successful_source = None
        
        for source in enabled_sources:
            try:
                self.logger.debug(f"尝试数据源: {source.name}")
                method_func = getattr(source, method)
                
                if symbol:
                    data = await method_func(symbol, **kwargs)
                else:
                    data = await method_func(**kwargs)
                
                # 缓存结果
                cache_ttl = source.get_config().cache_ttl
                await self.cache_manager.set(cache_key, data, cache_ttl)
                
                successful_source = source.name
                self.logger.info(f"成功从 {source.name} 获取数据: {method}")
                return data
                
            except Exception as e:
                last_error = e
                self.logger.warning(f"数据源 {source.name} 失败: {e}")
                continue
        
        # 所有数据源都失败
        error_msg = f"所有数据源都失败，最后错误: {last_error}"
        self.logger.error(error_msg)
        raise Exception(error_msg)
    
    async def health_check_all(self) -> Dict[str, bool]:
        """检查所有数据源的健康状态"""
        results = {}
        for source in self.sources:
            try:
                results[source.name] = await source.health_check()
            except Exception as e:
                self.logger.error(f"健康检查失败 {source.name}: {e}")
                results[source.name] = False
        return results
    
    def get_source_info(self) -> List[Dict[str, Any]]:
        """获取数据源信息"""
        info = []
        for source in self.sources:
            config = source.get_config()
            info.append({
                "name": source.name,
                "enabled": config.enabled,
                "priority": config.priority,
                "timeout": config.timeout,
                "retry_count": config.retry_count,
                "cache_ttl": config.cache_ttl
            })
        return info
    
    def clear_cache(self):
        """清空缓存"""
        self.cache_manager.clear()
        self.logger.info("缓存已清空")
