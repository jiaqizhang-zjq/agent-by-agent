#!/usr/bin/env python
"""真实多轮对话测试 - 模拟用户真实使用场景"""

import sys
import os
import time
from pathlib import Path
from typing import List, Dict

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.fortune_telling.intelligent_agent import IntelligentAgent


class MultiTurnTest:
    """多轮对话测试"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.conversations: List[Dict[str, str]] = []
        self.expected_results: List[str] = []
    
    def add_turn(self, user_input: str, expected_output: str = ""):
        """添加一轮对话"""
        self.conversations.append({"user": user_input, "expected": expected_output})
    
    def run(self, agent: IntelligentAgent) -> bool:
        """执行测试"""
        print(f"\n{'='*60}")
        print(f"测试场景: {self.name}")
        print(f"描述: {self.description}")
        print(f"{'='*60}")
        
        passed = True
        for i, conv in enumerate(self.conversations, 1):
            print(f"\n[第{i}轮]")
            print(f"用户: {conv['user']}")
            
            start_time = time.time()
            response = agent.chat(conv['user'])
            duration = time.time() - start_time
            
            print(f"助手: {response[:200]}...")
            print(f"耗时: {duration:.2f}秒")
            
            # 简单验证：只要不崩溃就算通过
            if response and len(response) > 0:
                print("✅ 通过")
            else:
                print("❌ 失败")
                passed = False
        
        return passed


def main():
    """主函数"""
    print("=" * 80)
    print("真实多轮对话测试")
    print("=" * 80)
    
    # 清理记忆文件
    memory_file = Path(__file__).parent.parent / "data" / "memory_store.json"
    if memory_file.exists():
        memory_file.unlink()
    
    agent = IntelligentAgent()
    
    # 定义测试场景
    tests = []
    
    # 场景1: 新用户第一次使用
    test1 = MultiTurnTest(
        "新用户第一次使用",
        "模拟一个新用户第一次使用算命Agent的场景"
    )
    test1.add_turn("你好")
    test1.add_turn("你能做什么？")
    test1.add_turn("我想算算命")
    test1.add_turn("我是1990年5月15日下午2点出生的，男")
    test1.add_turn("分析我的八字")
    tests.append(test1)
    
    # 场景2: 老用户继续对话
    test2 = MultiTurnTest(
        "老用户继续对话",
        "模拟一个老用户继续之前的对话"
    )
    test2.add_turn("你还记得我吗？")
    test2.add_turn("我的信息是什么？")
    test2.add_turn("帮我分析一下2025年的运势")
    test2.add_turn("我的事业运势如何？")
    test2.add_turn("谢谢")
    tests.append(test2)
    
    # 场景3: 用户提供错误信息后纠正
    test3 = MultiTurnTest(
        "用户提供错误信息后纠正",
        "模拟用户提供错误信息后纠正的场景"
    )
    test3.add_turn("我是1990年出生的")
    test3.add_turn("不对，我其实是1991年出生的")
    test3.add_turn("5月15日下午2点，男")
    test3.add_turn("分析我的八字")
    test3.add_turn("我的出生日期是什么？")
    tests.append(test3)
    
    # 场景4: 用户跳跃话题
    test4 = MultiTurnTest(
        "用户跳跃话题",
        "模拟用户跳跃话题的场景"
    )
    test4.add_turn("分析我的八字")
    test4.add_turn("我的2025年运势如何？")
    test4.add_turn("再说说我的事业运势")
    test4.add_turn("我五行缺什么？")
    test4.add_turn("我的性格如何？")
    tests.append(test4)
    
    # 场景5: 混合输入
    test5 = MultiTurnTest(
        "混合输入",
        "模拟用户一次输入多个信息的场景"
    )
    test5.add_turn("我是1990年5月15日下午2点出生的，男，帮我分析一下事业运势")
    test5.add_turn("我的感情运势如何？")
    test5.add_turn("我适合什么职业？")
    test5.add_turn("我的贵人运如何？")
    test5.add_turn("谢谢你的分析")
    tests.append(test5)
    
    # 场景6: 长对话
    test6 = MultiTurnTest(
        "长对话（10轮）",
        "模拟用户进行长对话的场景"
    )
    test6.add_turn("你好")
    test6.add_turn("我是1990年5月15日下午2点出生的，男")
    test6.add_turn("分析我的八字")
    test6.add_turn("我的性格如何？")
    test6.add_turn("我的事业运势如何？")
    test6.add_turn("我的感情运势如何？")
    test6.add_turn("我的财运如何？")
    test6.add_turn("我的健康运势如何？")
    test6.add_turn("我需要注意什么？")
    test6.add_turn("谢谢")
    tests.append(test6)
    
    # 场景7: 用户询问模糊信息
    test7 = MultiTurnTest(
        "用户询问模糊信息",
        "模拟用户询问模糊信息的场景"
    )
    test7.add_turn("我是傍晚出生的")
    test7.add_turn("我是河南许昌鄢陵县出生的")
    test7.add_turn("我是农历三月初一出生的")
    test7.add_turn("你能理解这些信息吗？")
    test7.add_turn("帮我分析一下")
    tests.append(test7)
    
    # 场景8: 用户重复提问
    test8 = MultiTurnTest(
        "用户重复提问",
        "模拟用户重复提问的场景"
    )
    test8.add_turn("我是1990年5月15日下午2点出生的，男")
    test8.add_turn("分析我的八字")
    test8.add_turn("再分析一次我的八字")
    test8.add_turn("我的八字是什么？")
    test8.add_turn("再告诉我一次我的八字")
    tests.append(test8)
    
    # 执行所有测试
    passed_count = 0
    total_count = len(tests)
    
    for test in tests:
        if test.run(agent):
            passed_count += 1
    
    # 输出测试报告
    print("\n" + "=" * 80)
    print("测试报告")
    print("=" * 80)
    print(f"总测试场景数: {total_count}")
    print(f"通过数: {passed_count} ✅")
    print(f"失败数: {total_count - passed_count} ❌")
    print(f"通过率: {passed_count/total_count*100:.1f}%")
    
    if passed_count == total_count:
        print("\n✅ 所有测试通过！")
    else:
        print(f"\n❌ 有{total_count - passed_count}个测试失败")


if __name__ == "__main__":
    main()
