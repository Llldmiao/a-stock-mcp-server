# A股MCP服务器使用指南

## 概述
这是一个基于Model Context Protocol (MCP) 的A股实时行情查询服务器，专为AI助手设计。它提供了5个核心工具来查询A股市场数据。

## MCP配置
```json
{
  "mcpServers": {
    "a-stock-realtime": {
      "command": "python",
      "args": ["-m", "a_stock_mcp_server"]
    }
  }
}
```

## 可用工具

### 1. get_realtime_price - 获取实时价格
**用途**: 查询A股股票的实时价格信息

**参数**:
- `symbol` (必需): 股票代码，6位数字，如 "000001"

**示例**:
```json
{
  "name": "get_realtime_price",
  "arguments": {
    "symbol": "000001"
  }
}
```

**返回信息**:
- 股票代码和名称
- 当前价格、涨跌幅
- 成交量、成交额
- 最高价、最低价
- 市盈率、市净率
- 更新时间

### 2. get_stock_info - 获取股票基本信息
**用途**: 查询股票的基本信息和公司概况

**参数**:
- `symbol` (必需): 股票代码，6位数字

**示例**:
```json
{
  "name": "get_stock_info",
  "arguments": {
    "symbol": "000001"
  }
}
```

### 3. get_market_summary - 获取市场概况
**用途**: 获取主要市场指数的概况信息

**参数**: 无

**示例**:
```json
{
  "name": "get_market_summary",
  "arguments": {}
}
```

**返回信息**:
- 上证指数、深证成指
- 创业板指、科创50
- 各指数的价格和涨跌幅

### 4. get_stock_history - 获取历史数据
**用途**: 查询股票的历史K线数据

**参数**:
- `symbol` (必需): 股票代码
- `period` (可选): 周期类型，默认 "daily"
  - "daily": 日线
  - "weekly": 周线  
  - "monthly": 月线
- `start_date` (可选): 开始日期，格式 "20240101"
- `end_date` (可选): 结束日期，格式 "20241231"

**示例**:
```json
{
  "name": "get_stock_history",
  "arguments": {
    "symbol": "000001",
    "period": "daily",
    "start_date": "20240101",
    "end_date": "20240131"
  }
}
```

### 5. get_financial_data - 获取财务数据
**用途**: 查询公司的财务报告数据

**参数**:
- `symbol` (必需): 股票代码
- `report_type` (可选): 报告类型，默认 "income"
  - "income": 利润表
  - "balance": 资产负债表
  - "cashflow": 现金流量表

**示例**:
```json
{
  "name": "get_financial_data",
  "arguments": {
    "symbol": "000001",
    "report_type": "income"
  }
}
```

## 使用场景示例

### 场景1: 查询平安银行实时价格
```json
{
  "name": "get_realtime_price",
  "arguments": {
    "symbol": "000001"
  }
}
```

### 场景2: 获取市场整体情况
```json
{
  "name": "get_market_summary",
  "arguments": {}
}
```

### 场景3: 分析股票历史走势
```json
{
  "name": "get_stock_history",
  "arguments": {
    "symbol": "000001",
    "period": "daily",
    "start_date": "20240101",
    "end_date": "20240331"
  }
}
```

### 场景4: 查看公司财务状况
```json
{
  "name": "get_financial_data",
  "arguments": {
    "symbol": "000001",
    "report_type": "income"
  }
}
```

## 错误处理

### 常见错误类型
1. **无效股票代码**: 返回 "无效的股票代码格式"
2. **网络连接失败**: 返回 "获取数据失败: [错误详情]"
3. **股票不存在**: 返回 "未找到股票代码: [代码]"
4. **参数错误**: 返回相应的参数验证错误

### 错误处理建议
- 始终检查返回结果是否包含错误信息
- 对于网络错误，可以建议用户稍后重试
- 对于无效股票代码，提醒用户使用6位数字格式

## 数据源说明
- 数据来源: AKShare (开源金融数据接口)
- 更新频率: 实时（交易时间内）
- 数据范围: 沪深A股市场

## 注意事项
1. 股票代码必须是6位数字格式
2. 交易时间外可能无法获取最新数据
3. 网络连接问题可能导致查询失败
4. 建议在查询前验证股票代码的有效性

## 安装要求
- Python 3.11+
- 依赖包: akshare, mcp, aiohttp, pandas, numpy

## 联系信息
- GitHub: https://github.com/Llldmiao/a-stock-mcp-server
- PyPI: https://pypi.org/project/a-stock-mcp-server/
