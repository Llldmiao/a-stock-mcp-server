"""
A股MCP服务器
使用多数据源架构的标准MCP服务器实现
"""

import asyncio
import logging
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.server.lowlevel.server import NotificationOptions
from mcp.types import Tool, TextContent

from .data_sources import DataSourceManager, AKShareDataSource, DataSourceConfig
from .tools import (
    RealtimePriceTool,
    StockInfoTool,
    MarketSummaryTool,
    StockHistoryTool,
    FinancialDataTool,
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AStockMCPServer:
    """A股MCP服务器"""
    
    def __init__(self):
        self.server = Server("a-stock-realtime")
        self.data_source_manager = DataSourceManager()
        self.tools = []
        
        # 初始化数据源
        self._setup_data_sources()
        
        # 初始化工具
        self._setup_tools()
        
        # 设置MCP处理器
        self._setup_handlers()
    
    def _setup_data_sources(self):
        """设置数据源"""
        # 创建AKShare数据源
        akshare_config = DataSourceConfig(
            name="akshare",
            enabled=True,
            priority=1,
            timeout=30,
            retry_count=3,
            cache_ttl=300
        )
        
        akshare_source = AKShareDataSource(akshare_config)
        self.data_source_manager.register_source(akshare_source)
        
        logger.info("数据源初始化完成")
    
    def _setup_tools(self):
        """设置工具"""
        self.tools = [
            RealtimePriceTool(self.data_source_manager),
            StockInfoTool(self.data_source_manager),
            MarketSummaryTool(self.data_source_manager),
            StockHistoryTool(self.data_source_manager),
            FinancialDataTool(self.data_source_manager),
        ]
        
        logger.info(f"工具初始化完成，共{len(self.tools)}个工具")
    
    def _setup_handlers(self):
        """设置MCP处理器"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """列出可用工具"""
            return [tool.tool_definition for tool in self.tools]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[TextContent]:
            """处理工具调用"""
            try:
                # 查找对应的工具
                tool = None
                for t in self.tools:
                    if t.tool_definition.name == name:
                        tool = t
                        break
                
                if tool is None:
                    return [TextContent(type="text", text=f"未知工具: {name}")]
                
                # 执行工具
                return await tool.execute(arguments)
                
            except Exception as e:
                logger.error(f"工具调用错误: {e}")
                return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    async def run(self):
        """运行服务器"""
        # 创建通知选项
        notification_options = NotificationOptions(
            prompts_changed=False, 
            resources_changed=False, 
            tools_changed=False
        )
        
        # 使用stdio传输
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="a-stock-realtime",
                    server_version="2.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=notification_options,
                        experimental_capabilities={},
                    ),
                ),
            )


async def main():
    """主函数"""
    app = AStockMCPServer()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
