#!/usr/bin/env python3
"""
A股MCP服务器测试用例
"""

import pytest
import asyncio
from a_stock_mcp_server import AStockMCPServerWithAKShare

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
        assert "000001" in result[0].text
    
    @pytest.mark.asyncio
    async def test_get_stock_info(self, server):
        """测试获取股票信息"""
        result = await server.get_stock_info({"symbol": "000001"})
        assert len(result) > 0
        assert result[0].type == "text"
        assert "000001" in result[0].text
    
    @pytest.mark.asyncio
    async def test_get_market_summary(self, server):
        """测试获取市场概况"""
        result = await server.get_market_summary({})
        assert len(result) > 0
        assert result[0].type == "text"
        assert "市场概况" in result[0].text
    
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
        assert "000001" in result[0].text
    
    @pytest.mark.asyncio
    async def test_get_financial_data(self, server):
        """测试获取财务数据"""
        result = await server.get_financial_data({
            "symbol": "000001",
            "report_type": "income"
        })
        assert len(result) > 0
        assert result[0].type == "text"
        assert "000001" in result[0].text
    
    @pytest.mark.asyncio
    async def test_invalid_symbol(self, server):
        """测试无效股票代码"""
        result = await server.get_realtime_price({"symbol": "INVALID"})
        assert len(result) > 0
        assert "未找到" in result[0].text or "错误" in result[0].text

if __name__ == "__main__":
    pytest.main([__file__])
