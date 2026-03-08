#!/usr/bin/env python3
"""端到端测试脚本 - 测试完整的算命Agent流程"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

def test_complete_flow():
    """测试完整流程"""
    print("=" * 60)
    print("端到端测试 - 算命Agent完整流程")
    print("=" * 60)
    
    agent = FortuneTellingAgent()
    session_id = agent.create_session()
    print(f"✓ 创建会话: {session_id[:8]}...")
    
    print("\n测试1: 提供完整信息")
    response = agent.process_input("我1990年5月15日下午2点半出生，男的", session_id)
    print(f"Agent: {response}")
    
    print("\n测试2: 提问事业")
    response = agent.process_input("事业", session_id)
    print(f"Agent: {response[:200]}...")
    
    print("\n测试3: 记住用户信息")
    response = agent.process_input("你还记得我是谁吗", session_id)
    print(f"Agent: {response}")
    
    print("\n测试4: 继续提问")
    response = agent.process_input("感情", session_id)
    print(f"Agent: {response[:200]}...")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_complete_flow()
