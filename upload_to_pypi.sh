#!/bin/bash
# PyPI上传脚本

echo "🚀 上传A股MCP服务器到PyPI"
echo "=========================="

# 检查环境变量
if [ -z "$PYPI_USERNAME" ] || [ -z "$PYPI_PASSWORD" ]; then
    echo "❌ 请设置环境变量:"
    echo "export PYPI_USERNAME='__token__'"
    echo "export PYPI_PASSWORD='your_api_token_here'"
    echo ""
    echo "然后重新运行此脚本"
    exit 1
fi

# 上传到PyPI
echo "📦 上传包到PyPI..."
python3 -m twine upload --username "$PYPI_USERNAME" --password "$PYPI_PASSWORD" dist/*

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 上传成功！"
    echo ""
    echo "📋 下一步:"
    echo "1. 访问: https://pypi.org/project/a-stock-mcp-server/"
    echo "2. 验证包是否正确显示"
    echo "3. 测试安装: pip install a-stock-mcp-server"
    echo ""
    echo "🔗 PyPI链接: https://pypi.org/project/a-stock-mcp-server/"
else
    echo "❌ 上传失败，请检查API Token和网络连接"
fi
