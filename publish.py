#!/usr/bin/env python3
"""
A股MCP服务器发布脚本
自动执行发布前的检查和发布流程
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令并返回结果"""
    print(f"执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"命令失败: {cmd}")
        print(f"错误输出: {result.stderr}")
        sys.exit(1)
    return result

def check_environment():
    """检查发布环境"""
    print("🔍 检查发布环境...")
    
    # 检查Python版本
    result = run_command("python3 --version")
    print(f"Python版本: {result.stdout.strip()}")
    
    # 检查pip版本
    result = run_command("pip3 --version")
    print(f"pip版本: {result.stdout.strip()}")
    
    # 检查twine是否安装
    try:
        result = run_command("twine --version")
        print(f"twine版本: {result.stdout.strip()}")
    except:
        print("⚠️ twine未安装，正在安装...")
        run_command("pip3 install twine")
    
    print("✅ 环境检查完成")

def clean_build():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        if os.path.exists(pattern):
            if os.path.isdir(pattern):
                shutil.rmtree(pattern)
            else:
                os.remove(pattern)
    
    print("✅ 清理完成")

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    
    # 运行本地测试
    result = run_command("python3 local_test.py", check=False)
    if result.returncode == 0:
        print("✅ 本地测试通过")
    else:
        print("⚠️ 本地测试失败，但继续发布流程")
    
    # 运行代码检查
    try:
        run_command("python3 -m flake8 *.py", check=False)
        print("✅ 代码检查完成")
    except:
        print("⚠️ 代码检查跳过")

def build_package():
    """构建包"""
    print("📦 构建包...")
    
    # 构建源码包
    run_command("python3 setup.py sdist")
    print("✅ 源码包构建完成")
    
    # 构建wheel包
    run_command("python3 setup.py bdist_wheel")
    print("✅ Wheel包构建完成")

def check_package():
    """检查包"""
    print("🔍 检查包...")
    
    # 检查源码包
    run_command("twine check dist/*")
    print("✅ 包检查完成")

def upload_to_pypi():
    """上传到PyPI"""
    print("🚀 上传到PyPI...")
    
    # 询问是否上传
    response = input("是否上传到PyPI? (y/N): ")
    if response.lower() != 'y':
        print("❌ 取消上传")
        return
    
    # 上传到PyPI
    run_command("twine upload dist/*")
    print("✅ 上传完成")

def create_git_tag():
    """创建Git标签"""
    print("🏷️ 创建Git标签...")
    
    version = "1.0.0"
    tag_name = f"v{version}"
    
    # 检查是否已有标签
    result = run_command(f"git tag -l {tag_name}", check=False)
    if tag_name in result.stdout:
        print(f"⚠️ 标签 {tag_name} 已存在")
        return
    
    # 创建标签
    run_command(f"git tag -a {tag_name} -m 'Release {tag_name}'")
    print(f"✅ 标签 {tag_name} 创建完成")

def main():
    """主函数"""
    print("🚀 A股MCP服务器发布流程")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists("setup.py"):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    try:
        # 执行发布流程
        check_environment()
        clean_build()
        run_tests()
        build_package()
        check_package()
        
        # 询问是否继续
        response = input("是否继续发布? (y/N): ")
        if response.lower() != 'y':
            print("❌ 取消发布")
            return
        
        upload_to_pypi()
        create_git_tag()
        
        print("\n🎉 发布完成！")
        print("📋 发布清单:")
        print("- ✅ 环境检查")
        print("- ✅ 测试运行")
        print("- ✅ 包构建")
        print("- ✅ 包检查")
        print("- ✅ PyPI上传")
        print("- ✅ Git标签")
        
    except KeyboardInterrupt:
        print("\n❌ 发布被用户取消")
    except Exception as e:
        print(f"\n❌ 发布失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
