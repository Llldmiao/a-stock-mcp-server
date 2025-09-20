#!/usr/bin/env python3
"""
版本管理脚本
用于自动更新版本号、更新CHANGELOG和创建Git标签
"""

import os
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result

def get_current_version():
    """获取当前版本号"""
    try:
        result = run_command("poetry version --short", check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # 从pyproject.toml读取
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        match = re.search(r'version = "([^"]+)"', content)
        if match:
            return match.group(1)
    
    return "1.0.0"

def update_changelog(new_version, version_type):
    """更新CHANGELOG.md"""
    changelog_path = Path("CHANGELOG.md")
    
    if not changelog_path.exists():
        changelog_content = f"""# Changelog

所有重要的项目变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [{new_version}] - {datetime.now().strftime('%Y-%m-%d')}

### {version_type}
- 初始版本发布
"""
    else:
        content = changelog_path.read_text()
        
        # 添加新版本到Unreleased之后
        new_entry = f"""## [{new_version}] - {datetime.now().strftime('%Y-%m-%d')}

### {version_type}
- 版本更新

"""
        
        # 替换Unreleased部分
        if "## [Unreleased]" in content:
            content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n{new_entry}")
        else:
            content = f"## [Unreleased]\n\n{new_entry}\n\n{content}"
    
        changelog_content = content
    
    changelog_path.write_text(changelog_content)
    print(f"✅ 已更新 CHANGELOG.md")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 bump_version.py <version_type>")
        print("版本类型: patch, minor, major")
        print("示例: python3 bump_version.py patch")
        sys.exit(1)
    
    version_type = sys.argv[1].lower()
    if version_type not in ['patch', 'minor', 'major']:
        print("错误: 版本类型必须是 patch, minor 或 major")
        sys.exit(1)
    
    print(f"🚀 开始版本更新 ({version_type})")
    print("=" * 40)
    
    # 获取当前版本
    current_version = get_current_version()
    print(f"当前版本: {current_version}")
    
    # 更新版本
    print(f"更新版本 ({version_type})...")
    run_command(f"poetry version {version_type}")
    
    # 获取新版本
    new_version = get_current_version()
    print(f"新版本: {new_version}")
    
    # 更新CHANGELOG
    print("更新CHANGELOG...")
    update_changelog(new_version, version_type)
    
    # 提交更改
    print("提交更改...")
    run_command("git add pyproject.toml CHANGELOG.md")
    run_command(f'git commit -m "Bump version to {new_version}"')
    
    # 创建标签
    print(f"创建标签 v{new_version}...")
    run_command(f'git tag -a v{new_version} -m "Release version {new_version}"')
    
    print(f"\n🎉 版本更新完成!")
    print(f"新版本: {new_version}")
    print(f"标签: v{new_version}")
    print("\n下一步:")
    print("1. 推送标签: git push origin v{new_version}")
    print("2. GitHub Actions将自动发布到PyPI")

if __name__ == "__main__":
    main()
