# 本地配置和使用指南

## 📋 环境要求

- Python 3.11+
- pip 或 poetry
- 网络连接（用于获取股票数据）

## 🛠️ 安装步骤

### 方法1：使用 Poetry（推荐）

```bash
# 进入项目目录
cd a-stock-mcp-server

# 安装依赖
poetry install

# 激活虚拟环境
poetry shell
```

### 方法2：使用 pip

```bash
# 进入项目目录
cd a-stock-mcp-server

# 安装依赖
pip3 install -e .

# 或者安装到虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip3 install -e .
```

## 🧪 测试安装

### 1. 运行测试套件

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 运行特定测试
python3 -m pytest tests/test_mcp_server.py::TestAStockMCPServer::test_get_realtime_price -v
```

### 2. 运行测试客户端

```bash
# 快速测试（推荐，输出简洁）
python3 -m a_stock_mcp_server.test_client --quick

# 完整测试（详细输出）
python3 -m a_stock_mcp_server.test_client

# 运行旧版测试客户端（兼容性）
python3 -m a_stock_mcp_server.local_test
```

### 3. 命令行工具测试

```bash
# 查询股票价格
python3 -m a_stock_mcp_server.cli_tool price -s 000001

# 查询股票信息
python3 -m a_stock_mcp_server.cli_tool info -s 000001

# 查询市场概况
python3 -m a_stock_mcp_server.cli_tool market
```

## 🔧 MCP客户端配置

### 1. Claude Desktop 配置

编辑 Claude Desktop 配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "a-stock-realtime": {
      "command": "python3",
      "args": ["-m", "a_stock_mcp_server"],
      "cwd": "/Users/lengmiao/Dev/financial-tools/a-stock-mcp-server",
      "env": {
        "PYTHONPATH": "/Users/lengmiao/Dev/financial-tools/a-stock-mcp-server"
      }
    }
  }
}
```

### 2. 其他MCP客户端配置

#### Cline 配置

```json
{
  "mcpServers": {
    "a-stock-realtime": {
      "command": "python3",
      "args": ["-m", "a_stock_mcp_server"],
      "cwd": "/path/to/a-stock-mcp-server"
    }
  }
}
```

#### Continue 配置

```json
{
  "mcpServers": {
    "a-stock-realtime": {
      "command": "python3",
      "args": ["-m", "a_stock_mcp_server"],
      "cwd": "/path/to/a-stock-mcp-server"
    }
  }
}
```

## 🐍 Python代码使用

### 1. 新版本API（推荐）

```python
import asyncio
from a_stock_mcp_server.test_client import AStockTestClient

async def main():
    # 创建客户端
    client = AStockTestClient()
    
    # 查询实时价格
    price = await client.call_tool("get_realtime_price", {"symbol": "000001"})
    print("实时价格:", price)
    
    # 查询股票信息
    info = await client.call_tool("get_stock_info", {"symbol": "000001"})
    print("股票信息:", info)
    
    # 查询市场概况
    market = await client.call_tool("get_market_summary", {})
    print("市场概况:", market)
    
    # 健康检查
    health = await client.health_check()
    print("数据源状态:", health)
    
    # 获取数据源信息
    sources = client.get_source_info()
    print("数据源信息:", sources)

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. 旧版本API（兼容性）

```python
import asyncio
from a_stock_mcp_server.local_test import AStockLocalTest

async def main():
    # 创建服务器
    server = AStockLocalTest()
    
    # 查询实时价格
    price = await server.call_tool("get_realtime_price", {"symbol": "000001"})
    print("实时价格:", price)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔍 调试和故障排除

### 1. 检查数据源状态

```python
import asyncio
from a_stock_mcp_server.test_client import AStockTestClient

async def check_status():
    client = AStockTestClient()
    
    # 健康检查
    health = await client.health_check()
    print("数据源健康状态:", health)
    
    # 数据源信息
    sources = client.get_source_info()
    print("数据源配置:", sources)

asyncio.run(check_status())
```

### 2. 常见问题解决

#### 问题1：AKShare未安装
```bash
pip3 install akshare
```

#### 问题2：网络连接问题
```bash
# 检查网络连接
ping baidu.com

# 如果在中国大陆，可能需要配置代理
export https_proxy=http://your-proxy:port
export http_proxy=http://your-proxy:port
```

#### 问题3：权限问题
```bash
# 确保有执行权限
chmod +x /path/to/a-stock-mcp-server/a_stock_mcp_server/__main__.py
```

#### 问题4：Python路径问题
```bash
# 检查Python路径
which python3

# 使用绝对路径
/path/to/python3 -m a_stock_mcp_server
```

### 3. 日志调试

```python
import logging

# 启用详细日志
logging.basicConfig(level=logging.DEBUG)

# 运行测试
import asyncio
from a_stock_mcp_server.test_client import AStockTestClient

async def debug_test():
    client = AStockTestClient()
    result = await client.call_tool("get_realtime_price", {"symbol": "000001"})
    print(result)

asyncio.run(debug_test())
```

## 📊 性能优化

### 1. 缓存配置

```python
from a_stock_mcp_server.data_sources import DataSourceConfig, AKShareDataSource, DataSourceManager

# 自定义缓存配置
config = DataSourceConfig(
    name="akshare",
    enabled=True,
    priority=1,
    timeout=30,
    retry_count=3,
    cache_ttl=600,  # 10分钟缓存
    max_requests_per_minute=30  # 限制请求频率
)

# 创建数据源
source = AKShareDataSource(config)
manager = DataSourceManager()
manager.register_source(source)
```

### 2. 并发控制

```python
import asyncio
from a_stock_mcp_server.test_client import AStockTestClient

async def batch_query():
    client = AStockTestClient()
    
    # 并发查询多个股票
    symbols = ["000001", "000002", "600036", "601318"]
    
    tasks = []
    for symbol in symbols:
        task = client.call_tool("get_realtime_price", {"symbol": symbol})
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    
    for i, result in enumerate(results):
        print(f"{symbols[i]}: {result}")

asyncio.run(batch_query())
```

## 🔄 更新和维护

### 1. 更新依赖

```bash
# 使用poetry
poetry update

# 使用pip
pip3 install --upgrade akshare mcp pandas
```

### 2. 清理缓存

```python
from a_stock_mcp_server.test_client import AStockTestClient

client = AStockTestClient()
client.data_source_manager.clear_cache()
print("缓存已清理")
```

### 3. 重启服务

如果使用MCP客户端，重启客户端应用即可。

## 📝 使用示例

### 完整的股票分析示例

```python
import asyncio
from a_stock_mcp_server.test_client import AStockTestClient

async def stock_analysis(symbol):
    client = AStockTestClient()
    
    print(f"=== {symbol} 股票分析 ===")
    
    # 1. 实时价格
    price = await client.call_tool("get_realtime_price", {"symbol": symbol})
    print("1. 实时价格:")
    print(price)
    
    # 2. 基本信息
    info = await client.call_tool("get_stock_info", {"symbol": symbol})
    print("\n2. 基本信息:")
    print(info)
    
    # 3. 历史数据
    history = await client.call_tool("get_stock_history", {
        "symbol": symbol,
        "period": "daily",
        "start_date": "20240101",
        "end_date": "20241231"
    })
    print("\n3. 历史数据:")
    print(history)
    
    # 4. 财务数据
    financial = await client.call_tool("get_financial_data", {
        "symbol": symbol,
        "report_type": "income"
    })
    print("\n4. 财务数据:")
    print(financial)

# 分析平安银行
asyncio.run(stock_analysis("000001"))
```

这个配置指南应该能帮助您在本地成功配置和使用重构后的 a-stock-mcp-server！
