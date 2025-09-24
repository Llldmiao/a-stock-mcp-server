#!/usr/bin/env python3
"""
A股实时行情MCP服务器 - 多数据源架构
需要安装: pip install akshare mcp
"""

import asyncio
import logging
from .server import AStockMCPServer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AStockMCPServerWithAKShare:
    """向后兼容的包装类"""

    def __init__(self):
        self.mcp_server = AStockMCPServer()
        self.server = self.mcp_server.server

    async def run(self):
        """运行服务器"""
        await self.mcp_server.run()


async def main():
    """主函数"""
    app = AStockMCPServerWithAKShare()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
