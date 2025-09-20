#!/bin/bash
# A股MCP服务器快速启动脚本

echo "🚀 A股MCP服务器快速启动"
echo "=========================="

# 检查Python3是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查pip3是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装，请先安装pip3"
    exit 1
fi

echo "✅ Python3 和 pip3 已安装"

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境？(y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 安装依赖
echo "📥 安装依赖包..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 运行测试
echo "🧪 运行测试..."
python3 -m pytest tests/ -v

if [ $? -eq 0 ]; then
    echo "✅ 测试通过"
else
    echo "⚠️  测试失败，但可以继续运行示例"
fi

# 运行示例
echo "🎯 运行使用示例..."
python3 examples/example_usage.py

echo ""
echo "🎉 快速启动完成！"
echo ""
echo "📖 使用说明："
echo "1. 运行MCP服务器: python3 a_stock_mcp_with_akshare.py"
echo "2. 查看文档: cat README.md"
echo "3. 查看API文档: cat docs/API.md"
echo ""
echo "🔗 更多信息请查看项目文档"
