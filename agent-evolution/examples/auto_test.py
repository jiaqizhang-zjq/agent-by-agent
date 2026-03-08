import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

print("=" * 60)
print("自动化测试开始")
print("=" * 60)

agent = FortuneTellingAgent()

# 创建会话
session_id = agent.create_session()
print(f"会话ID: {session_id}\n")

# 测试1: 问候
print("-" * 60)
print("测试1: 问候")
user_input = "你好"
print(f"用户: {user_input}")
response = agent.process_input(user_input, session_id)
print(f"Agent: {response}\n")

# 测试2: 提供信息
print("-" * 60)
print("测试2: 提供出生信息")
user_input = "1990-05-15 14:30 男"
print(f"用户: {user_input}")
response = agent.process_input(user_input, session_id)
print(f"Agent: {response}\n")

# 测试3: 提问
print("-" * 60)
print("测试3: 提问事业")
user_input = "事业"
print(f"用户: {user_input}")
response = agent.process_input(user_input, session_id)
print(f"Agent: {response}\n")

print("=" * 60)
print("测试完成!")
print("=" * 60)
