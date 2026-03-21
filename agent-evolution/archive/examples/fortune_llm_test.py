import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

agent = FortuneTellingAgent()

session_id = agent.create_session()
print(f"会话ID: {session_id}")

response = agent.process_input("你好", session_id)
print(f"\n1. Agent: {response}\n")

response = agent.process_input("1990-01-01 08:30 男", session_id)
print(f"\n2. Agent: {response[:200]}...\n")

response = agent.process_input("事业", session_id)
print(f"\n3. Agent: {response}\n")
