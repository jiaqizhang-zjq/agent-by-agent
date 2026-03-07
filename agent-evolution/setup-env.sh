#!/bin/bash

# 设置环境变量，让项目能够找到本地的第三方库
echo "设置环境变量..."

# 获取项目根目录
PROJECT_ROOT=$(pwd)

# 设置PYTHONPATH，包含本地第三方库
export PYTHONPATH="$PROJECT_ROOT/third-party/langchain:$PROJECT_ROOT/third-party/langgraph:$PROJECT_ROOT/third-party/mem0:$PYTHONPATH"

echo "PYTHONPATH已设置："
echo "$PYTHONPATH"

echo "\n环境设置完成！"
echo "现在可以运行项目了。"
