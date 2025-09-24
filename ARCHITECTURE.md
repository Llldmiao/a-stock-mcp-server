# A股MCP服务器架构文档

## 概述

本项目已重构为支持多数据源的模块化MCP服务器架构，提供A股实时行情查询服务。

## 架构设计

### 1. 多数据源架构

```
数据源层 (Data Sources)
├── BaseDataSource (抽象基类)
├── AKShareDataSource (AKShare实现)
├── DataSourceManager (数据源管理器)
└── CacheManager (缓存管理器)
```

**核心特性：**
- 支持多个数据源故障转移
- 智能缓存机制
- 数据源健康检查
- 优先级管理

### 2. 工具模块化

```
工具层 (Tools)
├── BaseTool (工具基类)
├── RealtimePriceTool (实时价格)
├── StockInfoTool (股票信息)
├── MarketSummaryTool (市场概况)
├── StockHistoryTool (历史数据)
└── FinancialDataTool (财务数据)
```

**核心特性：**
- 统一的工具接口
- 参数验证和格式化
- 错误处理机制

### 3. 服务器层

```
服务器层 (Server)
├── AStockMCPServer (主服务器)
├── AStockMCPServerWithAKShare (兼容包装)
└── AStockTestClient (测试客户端)
```

## 数据源配置

### 数据源基类

```python
@dataclass
class DataSourceConfig:
    name: str                    # 数据源名称
    enabled: bool = True         # 是否启用
    priority: int = 1            # 优先级（数字越小优先级越高）
    timeout: int = 30            # 超时时间（秒）
    retry_count: int = 3         # 重试次数
    cache_ttl: int = 300         # 缓存时间（秒）
    max_requests_per_minute: int = 60  # 每分钟最大请求数
```

### 添加新数据源

1. 继承 `BaseDataSource` 类
2. 实现所有抽象方法
3. 在服务器中注册数据源

```python
class NewDataSource(BaseDataSource):
    async def get_realtime_price(self, symbol: str) -> Dict[str, Any]:
        # 实现获取实时价格逻辑
        pass
    
    # 实现其他抽象方法...
```

## 工具开发

### 工具基类

```python
class BaseTool(ABC):
    def __init__(self, data_source_manager):
        self.data_source_manager = data_source_manager
    
    @property
    @abstractmethod
    def tool_definition(self) -> Tool:
        pass
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        # 参数验证 -> 数据获取 -> 格式化 -> 返回
        pass
```

### 添加新工具

1. 继承 `BaseTool` 类
2. 实现 `tool_definition` 属性
3. 实现 `_fetch_data` 和 `_format_data` 方法
4. 在服务器中注册工具

## 缓存机制

### 缓存策略

- **实时数据**: 5分钟缓存
- **历史数据**: 1小时缓存
- **财务数据**: 24小时缓存
- **市场概况**: 5分钟缓存

### 缓存管理

```python
# 获取缓存数据
cached_data = await cache_manager.get(cache_key)

# 设置缓存数据
await cache_manager.set(cache_key, data, ttl)

# 清空缓存
cache_manager.clear()
```

## 错误处理

### 故障转移机制

1. 按优先级尝试数据源
2. 记录失败原因
3. 自动切换到下一个数据源
4. 所有数据源失败时返回错误

### 错误类型

- **网络错误**: 自动重试
- **数据格式错误**: 记录日志并跳过
- **参数错误**: 返回详细错误信息
- **数据源不可用**: 尝试其他数据源

## 性能优化

### 并发处理

- 异步数据获取
- 并发工具执行
- 非阻塞I/O操作

### 缓存优化

- 内存缓存
- 智能过期策略
- 缓存命中率监控

### 请求优化

- 连接池复用
- 请求去重
- 批量数据获取

## 监控和日志

### 日志级别

- **DEBUG**: 详细调试信息
- **INFO**: 一般信息
- **WARNING**: 警告信息
- **ERROR**: 错误信息

### 监控指标

- 数据源健康状态
- 缓存命中率
- 请求响应时间
- 错误率统计

## 扩展指南

### 添加新数据源

1. 创建新的数据源类
2. 实现数据获取方法
3. 配置数据源参数
4. 注册到数据源管理器

### 添加新工具

1. 创建新的工具类
2. 定义工具接口
3. 实现数据处理逻辑
4. 注册到服务器

### 自定义缓存策略

1. 继承 `CacheManager` 类
2. 实现自定义缓存逻辑
3. 配置缓存参数
4. 替换默认缓存管理器

## 部署配置

### 环境变量

```bash
# 数据源配置
DATA_SOURCE_AKSHARE_ENABLED=true
DATA_SOURCE_AKSHARE_PRIORITY=1
DATA_SOURCE_AKSHARE_TIMEOUT=30

# 缓存配置
CACHE_ENABLED=true
CACHE_TTL=300

# 日志配置
LOG_LEVEL=INFO
```

### MCP客户端配置

```json
{
  "mcpServers": {
    "a-stock-realtime": {
      "command": "python",
      "args": ["-m", "a_stock_mcp_server"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

## 测试

### 运行测试

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 运行特定测试
python3 -m pytest tests/test_mcp_server.py -v

# 运行测试客户端
python3 -m a_stock_mcp_server.test_client
```

### 测试覆盖

- 单元测试：工具和数据源
- 集成测试：端到端功能
- 性能测试：并发和缓存
- 错误测试：异常情况处理

## 维护指南

### 定期维护

1. **数据源健康检查**: 每日检查数据源状态
2. **缓存清理**: 定期清理过期缓存
3. **日志轮转**: 定期清理旧日志文件
4. **性能监控**: 监控响应时间和错误率

### 故障排除

1. **数据源不可用**: 检查网络连接和数据源状态
2. **缓存问题**: 清空缓存或调整缓存策略
3. **性能问题**: 检查并发设置和资源使用
4. **错误日志**: 查看详细错误信息进行诊断

## 版本历史

### v2.0.0 (当前版本)
- 重构为多数据源架构
- 模块化工具设计
- 改进的缓存机制
- 增强的错误处理
- 完整的测试覆盖

### v1.0.0 (历史版本)
- 基础MCP服务器实现
- AKShare数据源支持
- 基本工具功能
