import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

def test_case_1():
    """测试用例1：基本信息收集和事业问题"""
    print("\n=== 测试用例1：基本信息收集和事业问题 ===")
    agent = FortuneTellingAgent()
    
    # 测试问候
    response = agent.process_input("你好")
    print(f"Agent: {response}")
    
    # 测试信息提供
    response = agent.process_input("1990-01-01 08:30 男")
    print(f"Agent: {response}")
    
    # 测试事业问题
    response = agent.process_input("事业")
    print(f"Agent: {response}")

def test_case_2():
    """测试用例2：感情问题"""
    print("\n=== 测试用例2：感情问题 ===")
    agent = FortuneTellingAgent()
    
    # 跳过问候，直接提供信息
    response = agent.process_input("1992-03-15 14:20 女")
    print(f"Agent: {response}")
    
    # 测试感情问题
    response = agent.process_input("感情")
    print(f"Agent: {response}")

def test_case_3():
    """测试用例3：健康问题"""
    print("\n=== 测试用例3：健康问题 ===")
    agent = FortuneTellingAgent()
    
    # 跳过问候，直接提供信息
    response = agent.process_input("1988-06-20 09:15 男")
    print(f"Agent: {response}")
    
    # 测试健康问题
    response = agent.process_input("健康")
    print(f"Agent: {response}")

def test_case_4():
    """测试用例4：财运问题"""
    print("\n=== 测试用例4：财运问题 ===")
    agent = FortuneTellingAgent()
    
    # 跳过问候，直接提供信息
    response = agent.process_input("1995-11-05 18:45 女")
    print(f"Agent: {response}")
    
    # 测试财运问题
    response = agent.process_input("财运")
    print(f"Agent: {response}")

def test_case_5():
    """测试用例5：多轮对话"""
    print("\n=== 测试用例5：多轮对话 ===")
    agent = FortuneTellingAgent()
    
    # 问候
    response = agent.process_input("你好")
    print(f"Agent: {response}")
    
    # 提供信息
    response = agent.process_input("1991-08-10 10:30 男")
    print(f"Agent: {response}")
    
    # 第一个问题：事业
    response = agent.process_input("事业")
    print(f"Agent: {response}")
    
    # 第二个问题：感情
    response = agent.process_input("感情")
    print(f"Agent: {response}")
    
    # 第三个问题：健康
    response = agent.process_input("健康")
    print(f"Agent: {response}")

def test_case_6():
    """测试用例6：不完整信息"""
    print("\n=== 测试用例6：不完整信息 ===")
    agent = FortuneTellingAgent()
    
    # 问候
    response = agent.process_input("你好")
    print(f"Agent: {response}")
    
    # 提供不完整信息
    response = agent.process_input("1990-01-01 男")
    print(f"Agent: {response}")

def test_case_7():
    """测试用例7：特殊输入"""
    print("\n=== 测试用例7：特殊输入 ===")
    agent = FortuneTellingAgent()
    
    # 问候
    response = agent.process_input("你好")
    print(f"Agent: {response}")
    
    # 提供特殊格式的信息
    response = agent.process_input("1990年1月1日 早上8点30分 男性")
    print(f"Agent: {response}")

def run_all_tests():
    """运行所有测试用例"""
    print("开始运行算命Agent测试用例...")
    print("=" * 60)
    
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    test_case_7()
    
    print("=" * 60)
    print("所有测试用例运行完成！")
    print("请查看logs目录下的日志文件以分析测试结果。")

if __name__ == "__main__":
    run_all_tests()