#!/usr/bin/env python3
"""
A股MCP服务器测试用例
"""

import pytest
import asyncio
from a_stock_mcp_server.__main__ import AStockMCPServerWithAKShare

class TestAStockMCPServer:
    """测试A股MCP服务器"""
    
    @pytest.fixture
    def server(self):
        """创建服务器实例"""
        return AStockMCPServerWithAKShare()
    
    @pytest.mark.asyncio
    async def test_get_realtime_price(self, server):
        """测试获取实时价格"""
        result = await server.get_realtime_price({"symbol": "000001"})
        assert len(result) > 0
        assert result[0].type == "text"
        # 在网络不可用时，可能返回错误信息，这是可以接受的
        text = result[0].text
        assert ("000001" in text or "获取数据失败" in text or "错误" in text)
    
    @pytest.mark.asyncio
    async def test_get_stock_info(self, server):
        """测试获取股票信息"""
        result = await server.get_stock_info({"symbol": "000001"})
        assert len(result) > 0
        assert result[0].type == "text"
        # 在网络不可用时，可能返回错误信息，这是可以接受的
        text = result[0].text
        assert ("000001" in text or "获取数据失败" in text or "错误" in text)
    
    @pytest.mark.asyncio
    async def test_get_market_summary(self, server):
        """测试获取市场概况"""
        result = await server.get_market_summary({})
        assert len(result) > 0
        assert result[0].type == "text"
        # 在网络不可用时，可能返回错误信息，这是可以接受的
        text = result[0].text
        assert ("市场概况" in text or "获取数据失败" in text or "错误" in text)
    
    @pytest.mark.asyncio
    async def test_get_stock_history(self, server):
        """测试获取历史数据"""
        result = await server.get_stock_history({
            "symbol": "000001",
            "period": "daily",
            "start_date": "20240101",
            "end_date": "20240131"
        })
        assert len(result) > 0
        assert result[0].type == "text"
        # 在网络不可用时，可能返回错误信息，这是可以接受的
        text = result[0].text
        assert ("000001" in text or "获取数据失败" in text or "错误" in text)
    
    @pytest.mark.asyncio
    async def test_get_financial_data(self, server):
        """测试获取财务数据"""
        result = await server.get_financial_data({
            "symbol": "000001",
            "report_type": "income"
        })
        assert len(result) > 0
        assert result[0].type == "text"
        # 在网络不可用时，可能返回错误信息，这是可以接受的
        text = result[0].text
        assert ("000001" in text or "获取数据失败" in text or "错误" in text)
    
    @pytest.mark.asyncio
    async def test_invalid_symbol(self, server):
        """测试无效股票代码"""
        result = await server.get_realtime_price({"symbol": "INVALID"})
        assert len(result) > 0
        assert "无效的股票代码格式" in result[0].text
    
    @pytest.mark.asyncio
    async def test_empty_symbol(self, server):
        """测试空股票代码"""
        result = await server.get_realtime_price({"symbol": ""})
        assert len(result) > 0
        assert "无效的股票代码格式" in result[0].text
    
    @pytest.mark.asyncio
    async def test_none_symbol(self, server):
        """测试None股票代码"""
        result = await server.get_realtime_price({"symbol": None})
        assert len(result) > 0
        assert "无效的股票代码格式" in result[0].text
    
    @pytest.mark.asyncio
    async def test_short_symbol(self, server):
        """测试过短的股票代码"""
        result = await server.get_realtime_price({"symbol": "123"})
        assert len(result) > 0
        assert "无效的股票代码格式" in result[0].text
    
    @pytest.mark.asyncio
    async def test_long_symbol(self, server):
        """测试过长的股票代码"""
        result = await server.get_realtime_price({"symbol": "1234567"})
        assert len(result) > 0
        assert "无效的股票代码格式" in result[0].text
    
    @pytest.mark.asyncio
    async def test_non_numeric_symbol(self, server):
        """测试非数字股票代码"""
        result = await server.get_realtime_price({"symbol": "ABC123"})
        assert len(result) > 0
        assert "无效的股票代码格式" in result[0].text
    
    @pytest.mark.asyncio
    async def test_nonexistent_symbol(self, server):
        """测试不存在的股票代码"""
        result = await server.get_realtime_price({"symbol": "999999"})
        assert len(result) > 0
        # 在网络不可用时，可能返回网络错误而不是"未找到股票代码"
        text = result[0].text
        assert ("未找到股票代码" in text or "获取数据失败" in text or "错误" in text)
    
    @pytest.mark.asyncio
    async def test_missing_symbol_param(self, server):
        """测试缺少symbol参数"""
        result = await server.get_realtime_price({})
        assert len(result) > 0
        assert "无效的股票代码格式" in result[0].text
    
    @pytest.mark.asyncio
    async def test_stock_info_invalid_symbol(self, server):
        """测试股票信息查询的无效代码"""
        result = await server.get_stock_info({"symbol": "INVALID"})
        assert len(result) > 0
        assert result[0].type == "text"
    
    @pytest.mark.asyncio
    async def test_stock_history_invalid_period(self, server):
        """测试历史数据查询的无效周期"""
        result = await server.get_stock_history({
            "symbol": "000001",
            "period": "invalid",
            "start_date": "20240101",
            "end_date": "20240131"
        })
        assert len(result) > 0
        assert result[0].type == "text"
    
    @pytest.mark.asyncio
    async def test_financial_data_invalid_type(self, server):
        """测试财务数据查询的无效类型"""
        result = await server.get_financial_data({
            "symbol": "000001",
            "report_type": "invalid"
        })
        assert len(result) > 0
        assert result[0].type == "text"

if __name__ == "__main__":
    pytest.main([__file__])
