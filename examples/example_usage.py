#!/usr/bin/env python3
"""
A股MCP服务器使用示例
演示如何调用各种工具获取A股数据
"""

import asyncio
import json
from a_stock_mcp_server.__main__ import AStockMCPServerWithAKShare

async def demo_usage():
    """演示MCP服务器的各种功能"""
    
    # 创建服务器实例
    server = AStockMCPServerWithAKShare()
    
    print("=== A股MCP服务器功能演示 ===\n")
    
    # 1. 获取实时价格
    print("1. 获取平安银行(000001)实时价格:")
    result = await server.get_realtime_price({"symbol": "000001"})
    print(result[0].text)
    print("\n" + "="*50 + "\n")
    
    # 2. 获取股票信息
    print("2. 获取平安银行基本信息:")
    result = await server.get_stock_info({"symbol": "000001"})
    print(result[0].text)
    print("\n" + "="*50 + "\n")
    
    # 3. 获取市场概况
    print("3. 获取市场概况:")
    result = await server.get_market_summary({})
    print(result[0].text)
    print("\n" + "="*50 + "\n")
    
    # 4. 获取历史数据
    print("4. 获取平安银行历史数据:")
    result = await server.get_stock_history({
        "symbol": "000001",
        "period": "daily",
        "start_date": "20240101",
        "end_date": "20240131"
    })
    print(result[0].text)
    print("\n" + "="*50 + "\n")
    
    # 5. 获取财务数据
    print("5. 获取平安银行财务数据:")
    result = await server.get_financial_data({
        "symbol": "000001",
        "report_type": "income"
    })
    print(result[0].text)

if __name__ == "__main__":
    asyncio.run(demo_usage())
