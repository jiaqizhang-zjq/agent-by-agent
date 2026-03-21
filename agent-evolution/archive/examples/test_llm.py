import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

agent = FortuneTellingAgent()
session_id = agent.create_session()

print("=" * 60)
print("测试LLM调用")
print("=" * 60)

# 测试1
response = agent.process_input('你好', session_id)
print(f"\n测试1: {response[:100]}")

# 测试2
response = agent.process_input('1990-05-15 14:30 男', session_id)
print(f"\n测试2: {response[:100]}")

# 测试3
response = agent.process_input('事业', session_id)
print(f"\n测试3: {response[:200]}")

print("\n" + "=" * 60)
