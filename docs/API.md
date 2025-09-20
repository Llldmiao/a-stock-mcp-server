# A股MCP服务器API文档

## 概述

A股MCP服务器提供了一套完整的工具来查询A股市场数据，包括实时价格、历史数据、财务信息等。

## 工具列表

### 1. get_realtime_price

获取A股实时价格信息。

**参数:**
- `symbol` (string, 必需): 股票代码，如 "000001"

**返回:**
- 股票代码、名称、当前价格、涨跌幅、成交量等信息

**示例:**
```json
{
  "tool": "get_realtime_price",
  "arguments": {
    "symbol": "000001"
  }
}
```

### 2. get_stock_info

获取股票基本信息。

**参数:**
- `symbol` (string, 必需): 股票代码

**返回:**
- 股票的基本信息，包括所属行业、上市日期、股本等

**示例:**
```json
{
  "tool": "get_stock_info",
  "arguments": {
    "symbol": "000001"
  }
}
```

### 3. get_market_summary

获取市场概况，包括主要指数信息。

**参数:**
- 无

**返回:**
- 上证指数、深证成指、创业板指等主要指数信息

**示例:**
```json
{
  "tool": "get_market_summary",
  "arguments": {}
}
```

### 4. get_stock_history

获取股票历史K线数据。

**参数:**
- `symbol` (string, 必需): 股票代码
- `period` (string, 可选): 周期类型，支持 "daily", "weekly", "monthly"，默认为 "daily"
- `start_date` (string, 可选): 开始日期，格式为 "YYYYMMDD"
- `end_date` (string, 可选): 结束日期，格式为 "YYYYMMDD"

**返回:**
- 历史K线数据，包括开盘价、收盘价、最高价、最低价、成交量等

**示例:**
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

### 5. get_financial_data

获取股票财务数据。

**参数:**
- `symbol` (string, 必需): 股票代码
- `report_type` (string, 可选): 报告类型，支持 "income", "balance", "cashflow"，默认为 "income"

**返回:**
- 财务数据，包括利润表、资产负债表或现金流量表

**示例:**
```json
{
  "tool": "get_financial_data",
  "arguments": {
    "symbol": "000001",
    "report_type": "income"
  }
}
```

## 错误处理

所有工具在遇到错误时会返回包含错误信息的文本内容。常见错误包括：

- 股票代码不存在
- 网络连接问题
- 数据源API限制
- 参数格式错误

## 数据源

本服务器使用AKShare作为数据源，数据更新频率约为15-20分钟。

## 注意事项

1. 所有价格数据仅供参考，不构成投资建议
2. 数据可能存在延迟，请以交易所官方数据为准
3. 请遵守数据源的使用条款和限制
4. 建议合理控制API调用频率
