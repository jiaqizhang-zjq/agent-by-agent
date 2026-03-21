#!/usr/bin/env python
"""效果测试 - 测试记忆功能"""

import sys
import os
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.fortune_telling.intelligent_agent import IntelligentAgent

def test_memory_effect():
    """测试记忆功能的效果"""
    print("=" * 60)
    print("效果测试 - 记忆功能")
    print("=" * 60)
    
    # 检查记忆文件是否存在
    memory_file = Path(__file__).parent.parent / "data" / "memory_store.json"
    print(f"\n记忆文件位置: {memory_file}")
    
    # 测试1: 创建新Agent，检查是否加载了之前的记忆
    print("\n【测试1】加载之前的记忆")
    print("-" * 40)
    agent1 = IntelligentAgent()
    print(f"记忆存储中的用户数: {len(agent1.memory_store)}")
    if agent1.memory_store:
        for user_id, memories in agent1.memory_store.items():
            print(f"用户 {user_id} 的记忆:")
            for memory in memories:
                print(f"  - {memory}")
    else:
        print("没有之前的记忆")
    
    # 测试2: 添加新的记忆
    print("\n【测试2】添加新的记忆")
    print("-" * 40)
    response = agent1.chat("我是1990年5月15日下午2点出生的，男")
    print(f"响应: {response[:100]}...")
    print(f"Context: {agent1.get_context()}")
    print(f"记忆存储: {agent1.memory_store}")
    
    # 测试3: 检查记忆是否保存到文件
    print("\n【测试3】检查记忆是否保存到文件")
    print("-" * 40)
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            saved_memory = json.load(f)
        print(f"文件中的记忆: {saved_memory}")
    else:
        print("记忆文件不存在")
    
    # 测试4: 创建新Agent，检查是否加载了刚才保存的记忆
    print("\n【测试4】创建新Agent，检查记忆是否持久化")
    print("-" * 40)
    agent2 = IntelligentAgent()
    print(f"新Agent的记忆存储: {agent2.memory_store}")
    
    # 测试5: 使用记忆回答问题
    print("\n【测试5】使用记忆回答问题")
    print("-" * 40)
    response = agent2.chat("你还记得我的出生信息吗？")
    print(f"响应: {response}")
    
    print("\n" + "=" * 60)
    print("效果测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_memory_effect()
