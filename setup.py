#!/usr/bin/env python3
"""
A股实时行情MCP服务器安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="a-stock-mcp-server",
    version="1.0.0",
    author="Financial Tools Developer",
    author_email="financial-tools@example.com",
    description="A股实时行情MCP服务器 - 基于Model Context Protocol的A股数据查询工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Llldmiao/a-stock-mcp-server",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "akshare>=1.12.0",
        "pandas>=1.5.0",
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "a-stock-mcp=local_test:demo_usage",
            "a-stock-cli=cli_tool:main",
        ],
    },
    keywords="mcp, stock, china, a-share, real-time, financial, data, investment, trading",
    project_urls={
        "Bug Reports": "https://github.com/Llldmiao/a-stock-mcp-server/issues",
        "Source": "https://github.com/Llldmiao/a-stock-mcp-server",
        "Documentation": "https://github.com/Llldmiao/a-stock-mcp-server#readme",
        "Changelog": "https://github.com/Llldmiao/a-stock-mcp-server/blob/main/CHANGELOG.md",
    },
    include_package_data=True,
    zip_safe=False,
)
