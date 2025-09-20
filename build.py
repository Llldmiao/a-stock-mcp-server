#!/usr/bin/env python3
"""
A股MCP服务器本地构建脚本
用于本地测试包构建和检查，不包含上传功能
"""

import os
import sys
import subprocess
import shutil

def run_command(cmd, check=True):
    """运行命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def main():
    """主函数"""
    print("🔨 A股MCP服务器本地构建")
    print("=" * 35)
    
    if not os.path.exists("setup.py"):
        print("❌ 请在项目根目录运行")
        sys.exit(1)
    
    try:
        # 清理构建文件
        print("🧹 清理构建文件...")
        for pattern in ["build", "dist", "*.egg-info"]:
            if os.path.exists(pattern):
                if os.path.isdir(pattern):
                    shutil.rmtree(pattern)
                else:
                    os.remove(pattern)
        print("✅ 清理完成")
        
        # 构建包
        print("📦 构建包...")
        run_command("python3 setup.py sdist bdist_wheel")
        print("✅ 构建完成")
        
        # 检查包
        print("🔍 检查包...")
        run_command("python3 -m twine check dist/*")
        print("✅ 检查通过")
        
        # 显示构建结果
        print("\n📋 构建结果:")
        if os.path.exists("dist"):
            for file in os.listdir("dist"):
                file_path = os.path.join("dist", file)
                size = os.path.getsize(file_path)
                print(f"  📄 {file} ({size:,} bytes)")
        
        print("\n💡 提示:")
        print("- 包已构建完成，可以本地测试")
        print("- 正式发布请使用GitHub Actions")
        print("- 运行: python3 -m a_stock_mcp_server.local_test")
        
    except KeyboardInterrupt:
        print("\n❌ 构建取消")
    except Exception as e:
        print(f"❌ 构建失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
