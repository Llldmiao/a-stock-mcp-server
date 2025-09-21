# A股实时行情MCP服务器

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io/)
[![PyPI version](https://badge.fury.io/py/a-stock-mcp-server.svg)](https://badge.fury.io/py/a-stock-mcp-server)
[![Downloads](https://pepy.tech/badge/a-stock-mcp-server)](https://pepy.tech/project/a-stock-mcp-server)

这是一个基于Model Context Protocol (MCP) 的A股实时行情查询服务器，支持查询A股实时价格、历史数据、财务信息等。专为AI助手和金融分析工具设计。

## 功能特性

### 🔥 核心功能
- **实时价格查询**: 获取A股实时价格、涨跌幅、成交量等
- **股票基本信息**: 查询股票的基本信息和公司概况
- **市场概况**: 获取上证、深证等主要指数信息
- **历史数据**: 查询股票的历史K线数据
- **财务数据**: 获取利润表、资产负债表、现金流量表

### 🛠️ 支持的工具
1. `get_realtime_price` - 获取实时价格
2. `get_stock_info` - 获取股票基本信息
3. `get_market_summary` - 获取市场概况
4. `get_stock_history` - 获取历史数据
5. `get_financial_data` - 获取财务数据

## 安装和使用

### 🚀 PyPI安装（推荐）

```bash
pip install a-stock-mcp-server
```

### 📦 从源码安装

```bash
# 克隆仓库
git clone https://github.com/Llldmiao/a-stock-mcp-server.git
cd a-stock-mcp-server

# 使用Poetry安装（推荐）
poetry install

# 或者使用pip安装
pip install -r requirements.txt
pip install -e .
```

### 🛠️ 命令行工具使用

安装后可以使用命令行工具：

```bash
# 查询股票价格
a-stock-cli price -s 000001

# 查询股票信息
a-stock-cli info -s 000001

# 查询市场概况
a-stock-cli market
```

### 🧪 本地测试

```bash
# 运行完整测试
python3 local_test.py
```

### 📚 Python代码使用

```python
import asyncio
from a_stock_mcp_server.local_test import AStockLocalTest

async def main():
    server = AStockLocalTest()
    
    # 查询平安银行实时价格
    result = await server.call_tool("get_realtime_price", {"symbol": "000001"})
    print(result)

asyncio.run(main())
```

**输出示例：**
```
股票代码: 000001
股票名称: 平安银行
当前价格: ¥11.45
涨跌额: +0.04
涨跌幅: +0.35%
成交量: 834,651.0
成交额: ¥955,004,096.91
最高价: ¥11.51
最低价: ¥11.37
开盘价: ¥11.41
昨收价: ¥11.41
换手率: 0.43%
市盈率: 4.47
市净率: 0.5
```

## 使用示例

### 查询实时价格
```json
{
  "tool": "get_realtime_price",
  "arguments": {
    "symbol": "000001"
  }
}
```

### 查询历史数据
```json
{
  "tool": "get_stock_history", 
  "arguments": {
    "symbol": "000001",
    "period": "daily",
    "start_date": "20240101",
    "end_date": "20241231"
  }
}
```

### 查询财务数据
```json
{
  "tool": "get_financial_data",
  "arguments": {
    "symbol": "000001",
    "report_type": "income"
  }
}
```

## 🔧 常用股票代码

| 股票名称 | 代码 | 市场 |
|---------|------|------|
| 平安银行 | 000001 | 深市 |
| 万科A | 000002 | 深市 |
| 中国平安 | 601318 | 沪市 |
| 招商银行 | 600036 | 沪市 |
| 工商银行 | 601398 | 沪市 |
| 建设银行 | 601939 | 沪市 |
| 农业银行 | 601288 | 沪市 |

## 数据源

本MCP服务器使用 [AKShare](https://github.com/akfamily/akshare) 作为数据源：
- 免费、开源
- 数据更新及时
- 支持多种金融数据
- 社区活跃

## 扩展建议

### 1. 多数据源支持
- 集成新浪财经API
- 集成腾讯财经API
- 添加数据源故障转移

### 2. 缓存机制
- 添加Redis缓存
- 减少API调用频率
- 提高响应速度

### 3. 数据验证
- 添加数据有效性检查
- 异常数据处理
- 错误重试机制

### 4. 更多功能
- 技术指标计算
- 股票筛选器
- 实时推送
- 历史回测

## 注意事项

1. **数据延迟**: AKShare数据可能有15-20分钟延迟
2. **API限制**: 注意API调用频率限制
3. **数据准确性**: 仅供参考，投资决策请谨慎
4. **网络依赖**: 需要稳定的网络连接

## 故障排除

### 常见问题

#### 问题1: 导入错误
```
ModuleNotFoundError: No module named 'akshare'
```
**解决方案**: 安装AKShare
```bash
pip3 install akshare
```

#### 问题2: 网络超时
```
获取数据失败: timeout
```
**解决方案**: 检查网络连接，可能需要代理

#### 问题3: 股票代码不存在
```
未找到股票代码: XXXXXX
```
**解决方案**: 检查股票代码格式，确保是6位数字

#### 问题4: 数据为空
**解决方案**: 检查股票代码格式是否正确

### 日志调试
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 完整使用示例

```python
#!/usr/bin/env python3
import asyncio
from a_stock_mcp_server.local_test import AStockLocalTest

async def main():
    # 创建服务器实例
    server = AStockLocalTest()
    
    # 查询平安银行实时价格
    print("=== 平安银行实时价格 ===")
    price = await server.call_tool("get_realtime_price", {"symbol": "000001"})
    print(price)
    
    # 查询股票基本信息
    print("\n=== 平安银行基本信息 ===")
    info = await server.call_tool("get_stock_info", {"symbol": "000001"})
    print(info)
    
    # 查询市场概况（只显示前10个）
    print("\n=== 市场概况（前10个）===")
    market = await server.call_tool("get_market_summary", {})
    lines = market.split('\n')
    for line in lines[:12]:  # 标题 + 前10个指数
        print(line)

if __name__ == "__main__":
    asyncio.run(main())
```

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License
