# A股MCP服务器使用指南

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+
- pip3

### 2. 安装步骤

```bash
# 进入项目目录
cd /Users/lengmiao/Dev/financial-tools/a-stock-mcp-server

# 安装依赖
pip3 install -r requirements.txt

# 运行本地测试
python3 local_test.py
```

## 📊 功能使用

### 1. 查询股票实时价格

```python
from local_test import AStockLocalTest

# 创建实例
server = AStockLocalTest()

# 查询平安银行实时价格
result = await server.call_tool("get_realtime_price", {"symbol": "000001"})
print(result)
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

### 2. 查询股票基本信息

```python
# 查询股票基本信息
result = await server.call_tool("get_stock_info", {"symbol": "000001"})
print(result)
```

**输出示例：**
```
=== 000001 基本信息 ===
最新: 11.45
股票代码: 000001
股票简称: 平安银行
总股本: 19405918198.0
流通股: 19405600653.0
总市值: 222197763367.09998
流通市值: 222194127476.84998
行业: 银行
上市时间: 19910403
```

### 3. 查询市场概况

```python
# 查询市场概况
result = await server.call_tool("get_market_summary", {})
print(result)
```

**输出示例：**
```
=== 市场概况 ===
300地产: 2914.32 (+69.87, +2.46%)
煤炭指数: 4204.17 (+96.94, +2.36%)
380能源: 1292.19 (+28.91, +2.29%)
内地地产: 2850.95 (+56.37, +2.02%)
A股资源: 5925.06 (+94.75, +1.63%)
...
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

## 📝 完整使用示例

```python
#!/usr/bin/env python3
import asyncio
from local_test import AStockLocalTest

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

## ⚠️ 注意事项

1. **数据延迟**: AKShare数据可能有15-20分钟延迟
2. **网络依赖**: 需要稳定的网络连接
3. **数据准确性**: 仅供参考，投资决策请谨慎
4. **API限制**: 注意API调用频率限制

## 🛠️ 故障排除

### 问题1: 导入错误
```
ModuleNotFoundError: No module named 'akshare'
```
**解决方案**: 安装AKShare
```bash
pip3 install akshare
```

### 问题2: 网络超时
```
获取数据失败: timeout
```
**解决方案**: 检查网络连接，可能需要代理

### 问题3: 股票代码不存在
```
未找到股票代码: XXXXXX
```
**解决方案**: 检查股票代码格式，确保是6位数字

## 📞 技术支持

如果遇到问题，可以：
1. 查看项目文档
2. 检查网络连接
3. 确认股票代码格式
4. 查看错误日志

## 🎯 下一步

- 等待MCP包发布后，可以集成到AI助手中
- 可以扩展更多功能（技术指标、股票筛选等）
- 可以添加缓存机制提高性能
