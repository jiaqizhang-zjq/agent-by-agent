#!/bin/bash

# Agent自我进化项目安装脚本

echo "开始安装Agent自我进化项目依赖..."

# 检查Python版本
echo "检查Python版本..."
python --version

# 安装uv（如果未安装）
if ! command -v uv &> /dev/null; then
    echo "安装uv..."
    pip install uv
fi

# 使用uv创建虚拟环境
echo "使用uv创建虚拟环境..."
uv venv venv

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖（不包括第三方库，使用本地克隆版本）
echo "安装项目依赖..."
uv pip install fastapi uvicorn sqlalchemy docker pytest requests beautifulsoup4 numpy pandas gitpython python-dotenv

# 提示安装完成
echo "\n安装完成！"
echo "项目将使用本地克隆的第三方库（langchain、langgraph、mem0）"
echo "可以通过以下命令启动项目："
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 启动核心引擎: python src/core/engine.py"
echo "3. 运行示例: python examples/basic/example.py"
