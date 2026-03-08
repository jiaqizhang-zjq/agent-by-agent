#!/usr/bin/env python
"""自动化测试Agent"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.fortune_telling.intelligent_agent import IntelligentAgent

def test_agent():
    """测试Agent"""
    print("=" * 60)
    print("自动化测试Agent")
    print("=" * 60)
    
    # 创建Agent
    agent = IntelligentAgent()
    
    # 测试1: 简单对话
    print("\n【测试1】简单对话")
    print("-" * 40)
    response = agent.chat("你好")
    print(f"响应: {response[:100]}...")
    
    # 测试2: 询问信息
    print("\n【测试2】询问信息")
    print("-" * 40)
    response = agent.chat("我的信息是什么？")
    print(f"响应: {response[:100]}...")
    
    # 测试3: 提供出生信息
    print("\n【测试3】提供出生信息")
    print("-" * 40)
    response = agent.chat("我是1990年5月15日下午2点出生的，男")
    print(f"响应: {response[:100]}...")
    
    # 测试4: 检查context
    print("\n【测试4】检查context")
    print("-" * 40)
    context = agent.get_context()
    print(f"Context: {context}")
    
    # 测试5: 再次询问信息
    print("\n【测试5】再次询问信息")
    print("-" * 40)
    response = agent.chat("我的信息是什么？")
    print(f"响应: {response[:100]}...")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_agent()
