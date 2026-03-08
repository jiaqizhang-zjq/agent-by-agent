#!/usr/bin/env python
"""多轮对话测试 - 真实场景测试"""

import sys
import os
import time
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.fortune_telling.intelligent_agent import IntelligentAgent


def test_multi_turn_conversation():
    """测试多轮对话场景"""
    print("=" * 80)
    print("多轮对话测试 - 真实场景")
    print("=" * 80)
    
    # 清理记忆文件
    memory_file = Path(__file__).parent.parent / "data" / "memory_store.json"
    if memory_file.exists():
        memory_file.unlink()
    
    agent = IntelligentAgent()
    
    # 测试场景1: 分步提供信息
    print("\n【场景1】分步提供信息")
    print("-" * 40)
    
    print("\n第1轮：")
    print("用户: 我是1990年出生的")
    response = agent.chat("我是1990年出生的")
    print(f"助手: {response}")
    
    print("\n第2轮：")
    print("用户: 5月15日下午2点")
    response = agent.chat("5月15日下午2点")
    print(f"助手: {response}")
    
    print("\n第3轮：")
    print("用户: 男")
    response = agent.chat("男")
    print(f"助手: {response}")
    
    print("\n第4轮：")
    print("用户: 帮我分析一下八字")
    response = agent.chat("帮我分析一下八字")
    print(f"助手: {response}")
    
    # 测试场景2: 信息更新
    print("\n\n【场景2】信息更新")
    print("-" * 40)
    
    print("\n第1轮：")
    print("用户: 我是1990年出生的")
    response = agent.chat("我是1990年出生的")
    print(f"助手: {response}")
    
    print("\n第2轮：")
    print("用户: 不对，我其实是1991年出生的")
    response = agent.chat("不对，我其实是1991年出生的")
    print(f"助手: {response}")
    
    # 测试场景3: 跳跃话题
    print("\n\n【场景3】跳跃话题")
    print("-" * 40)
    
    print("\n第1轮：")
    print("用户: 分析我的八字")
    response = agent.chat("分析我的八字")
    print(f"助手: {response}")
    
    print("\n第2轮：")
    print("用户: 我的2025年运势如何？")
    response = agent.chat("我的2025年运势如何？")
    print(f"助手: {response}")
    
    print("\n第3轮：")
    print("用户: 再说说我的事业运势")
    response = agent.chat("再说说我的事业运势")
    print(f"助手: {response}")
    
    # 测试场景4: 混合输入
    print("\n\n【场景4】混合输入")
    print("-" * 40)
    
    print("\n第1轮：")
    print("用户: 我是1990年5月15日下午2点出生的，男，帮我分析一下事业运势")
    response = agent.chat("我是1990年5月15日下午2点出生的，男，帮我分析一下事业运势")
    print(f"助手: {response}")
    
    # 测试场景5: 长对话
    print("\n\n【场景5】长对话（20轮）")
    print("-" * 40)
    
    for i in range(1, 21):
        print(f"\n第{i}轮：")
        if i == 1:
            user_input = "你好"
        elif i == 2:
            user_input = "我是1990年5月15日下午2点出生的，男"
        elif i == 3:
            user_input = "帮我分析一下八字"
        elif i == 4:
            user_input = "我的性格怎么样？"
        elif i == 5:
            user_input = "我的事业运势如何？"
        elif i == 6:
            user_input = "我的感情运势如何？"
        elif i == 7:
            user_input = "我五行缺什么？"
        elif i == 8:
            user_input = "我的2025年运势如何？"
        elif i == 9:
            user_input = "我的财运如何？"
        elif i == 10:
            user_input = "我的健康运势如何？"
        elif i == 11:
            user_input = "我适合什么职业？"
        elif i == 12:
            user_input = "我的贵人运如何？"
        elif i == 13:
            user_input = "我的桃花运如何？"
        elif i == 14:
            user_input = "我什么时候结婚？"
        elif i == 15:
            user_input = "我的子女运如何？"
        elif i == 16:
            user_input = "我的晚年运势如何？"
        elif i == 17:
            user_input = "我需要注意什么？"
        elif i == 18:
            user_input = "有什么建议给我？"
        elif i == 19:
            user_input = "谢谢你的分析"
        else:
            user_input = "再见"
        
        print(f"用户: {user_input}")
        response = agent.chat(user_input)
        print(f"助手: {response[:100]}...")
    
    print("\n" + "=" * 80)
    print("多轮对话测试完成")
    print("=" * 80)


if __name__ == "__main__":
    test_multi_turn_conversation()
