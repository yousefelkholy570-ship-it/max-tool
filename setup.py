#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Max Tool - Setup Script
Package installation and distribution setup
"""

from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8") if (Path(__file__).parent / "README.md").exists() else ""

setup(
    name="max-tool",
    version="1.0.0",
    author="yousefelkholy570",
    author_email="yousefelkholy570@gmail.com",
    description="Professional Integrated Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yousefelkholy570-ship-it/max-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.6.0",
        "PyQt6-Charts>=6.6.0",
        "requests>=2.31.0",
        "packaging>=23.0",
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "max-tool=max_tool_main:main",
        ],
    },
    include_package_data=True,
    license="MIT",
    keywords="tool platform management monitoring",
)
