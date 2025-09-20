#!/bin/bash
# A股MCP服务器快速启动脚本

echo "🚀 A股MCP服务器快速启动"
echo "=========================="

# 检查环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✅ Python3 已安装"

# 检查Poetry是否安装
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry 未安装，正在安装..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v poetry &> /dev/null; then
        echo "❌ Poetry 安装失败，请手动安装"
        echo "📖 安装指南: https://python-poetry.org/docs/#installation"
        exit 1
    fi
fi

echo "✅ Poetry 已安装"

# 安装依赖
echo "📥 安装依赖包..."
poetry install

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 运行本地测试
echo "🧪 运行本地测试..."
poetry run python -m a_stock_mcp_server.local_test

echo ""
echo "🎉 快速启动完成！"
echo "📖 使用说明："
echo "1. 运行MCP服务器: poetry run python -m a_stock_mcp_server"
echo "2. 命令行工具: poetry run a-stock-cli price -s 000001"
echo "3. 查看文档: cat README.md"
echo "4. 进入Poetry环境: poetry shell"
