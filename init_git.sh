#!/bin/bash
# Git仓库初始化脚本

echo "🚀 初始化A股MCP服务器Git仓库"
echo "================================"

# 检查是否在正确的目录
if [ ! -f "setup.py" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 初始化Git仓库
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote add origin https://github.com/Llldmiao/a-stock-mcp-server.git
echo "✅ 远程仓库添加完成"

# 添加所有文件
echo "📁 添加文件到Git..."
git add .
echo "✅ 文件添加完成"

# 创建初始提交
echo "💾 创建初始提交..."
git commit -m "🎉 初始提交: A股MCP服务器 v1.0.0

- ✅ 支持A股实时价格查询
- ✅ 支持股票基本信息查询  
- ✅ 支持市场概况查询
- ✅ 提供命令行工具接口
- ✅ 完整的API文档和使用指南
- ✅ 本地测试版本（无需MCP包依赖）
- ✅ 快速启动脚本

技术特性:
- 基于AKShare数据源获取真实A股数据
- 异步处理支持，性能优秀
- 完善的错误处理和日志记录
- 模块化设计，易于扩展
- 支持Python 3.8+"
echo "✅ 初始提交完成"

# 创建主分支
echo "🌿 创建主分支..."
git branch -M main
echo "✅ 主分支创建完成"

echo ""
echo "🎉 Git仓库初始化完成！"
echo ""
echo "📋 下一步操作:"
echo "1. 推送代码到GitHub:"
echo "   git push -u origin main"
echo ""
echo "2. 创建GitHub Release:"
echo "   - 访问: https://github.com/Llldmiao/a-stock-mcp-server/releases"
echo "   - 点击 'Create a new release'"
echo "   - 标签: v1.0.0"
echo "   - 标题: A股MCP服务器 v1.0.0"
echo "   - 描述: 详见CHANGELOG.md"
echo ""
echo "3. 发布到PyPI:"
echo "   python3 publish.py"
echo ""
echo "🔗 GitHub仓库: https://github.com/Llldmiao/a-stock-mcp-server"
