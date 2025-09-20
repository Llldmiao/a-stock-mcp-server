# 贡献指南

感谢您对A股MCP服务器的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题
- 使用GitHub Issues报告bug
- 提供详细的错误信息和复现步骤
- 包含系统环境信息

### 功能建议
- 在Issues中提出新功能建议
- 详细描述功能需求和用例
- 讨论实现方案

### 代码贡献
- Fork项目到您的GitHub账户
- 创建功能分支
- 提交代码并创建Pull Request

## 🛠️ 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/Llldmiao/a-stock-mcp-server.git
cd a-stock-mcp-server
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt  # 开发依赖
```

### 4. 运行测试
```bash
python3 -m pytest tests/
```

## 📝 代码规范

### Python代码风格
- 遵循PEP 8规范
- 使用Black进行代码格式化
- 使用flake8进行代码检查
- 使用mypy进行类型检查

### 提交信息规范
使用以下格式：
```
类型(范围): 简短描述

详细描述（可选）

相关Issue: #123
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例
```
feat(api): 添加股票筛选功能

新增根据行业、市值等条件筛选股票的功能

相关Issue: #45
```

## 🧪 测试指南

### 编写测试
- 为新功能编写测试用例
- 测试覆盖率应达到80%以上
- 使用pytest框架

### 测试结构
```
tests/
├── test_mcp_server.py      # 主要功能测试
├── test_data_source.py    # 数据源测试
└── test_utils.py          # 工具函数测试
```

### 运行测试
```bash
# 运行所有测试
python3 -m pytest

# 运行特定测试文件
python3 -m pytest tests/test_mcp_server.py

# 生成覆盖率报告
python3 -m pytest --cov=. --cov-report=html
```

## 📚 文档贡献

### 文档类型
- API文档更新
- 使用示例添加
- 故障排除指南
- 最佳实践分享

### 文档格式
- 使用Markdown格式
- 代码示例要完整可运行
- 包含必要的截图和图表

## 🔄 发布流程

### 版本号规则
使用语义化版本号：`主版本.次版本.修订版本`

- 主版本：不兼容的API修改
- 次版本：向下兼容的功能性新增
- 修订版本：向下兼容的问题修正

### 发布检查清单
参考 [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)

## 🏷️ 标签系统

### Issue标签
- `bug`: 错误报告
- `enhancement`: 功能增强
- `documentation`: 文档相关
- `question`: 问题咨询
- `good first issue`: 适合新手的任务

### Pull Request标签
- `ready for review`: 准备审查
- `work in progress`: 进行中
- `needs testing`: 需要测试
- `breaking change`: 破坏性变更

## 📞 联系方式

- GitHub Issues: 项目问题讨论
- Email: 重要事务联系
- 微信群: 日常交流（如有）

## 📄 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

---

**Happy Contributing! 🎉**
