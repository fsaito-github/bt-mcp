#!/usr/bin/env python3
"""
Setup script for Beach Tennis MCP Server
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("mcp_server/requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="beach-tennis-mcp",
    version="1.0.0",
    author="Beach Tennis MCP Team",
    author_email="contato@exemplo.com",
    description="MCP Server para consultar disponibilidade de quadras de Beach Tennis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/beach-tennis-mcp",
    project_urls={
        "Bug Reports": "https://github.com/seu-usuario/beach-tennis-mcp/issues",
        "Source": "https://github.com/seu-usuario/beach-tennis-mcp",
        "Documentation": "https://github.com/seu-usuario/beach-tennis-mcp#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Sports",
    ],
    python_requires=">=3.9",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "beach-tennis-mcp=mcp_server.beach_tennis_mcp:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="mcp, beach-tennis, court-availability, web-scraping, crawl4ai",
)
