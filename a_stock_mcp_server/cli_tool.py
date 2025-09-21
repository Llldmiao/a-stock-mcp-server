#!/usr/bin/env python3
"""
A股MCP服务器命令行工具
提供简单的命令行接口来查询A股数据
"""

import asyncio
import argparse
import sys
from .local_test import AStockLocalTest


async def query_stock_price(symbol):
    """查询股票价格"""
    server = AStockLocalTest()
    result = await server.call_tool("get_realtime_price", {"symbol": symbol})
    print(result)


async def query_stock_info(symbol):
    """查询股票信息"""
    server = AStockLocalTest()
    result = await server.call_tool("get_stock_info", {"symbol": symbol})
    print(result)


async def query_market_summary():
    """查询市场概况"""
    server = AStockLocalTest()
    result = await server.call_tool("get_market_summary", {})
    print(result)


def main():
    parser = argparse.ArgumentParser(description="A股MCP服务器命令行工具")
    parser.add_argument(
        "command",
        choices=["price", "info", "market"],
        help="命令类型: price(价格), info(信息), market(市场)",
    )
    parser.add_argument("-s", "--symbol", help="股票代码 (price和info命令需要)")

    args = parser.parse_args()

    if args.command in ["price", "info"] and not args.symbol:
        print("错误: price和info命令需要指定股票代码 (-s)")
        print("示例: python3 cli_tool.py price -s 000001")
        sys.exit(1)

    try:
        if args.command == "price":
            asyncio.run(query_stock_price(args.symbol))
        elif args.command == "info":
            asyncio.run(query_stock_info(args.symbol))
        elif args.command == "market":
            asyncio.run(query_market_summary())
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
