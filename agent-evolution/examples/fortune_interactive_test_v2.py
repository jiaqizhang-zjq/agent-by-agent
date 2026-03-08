import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent_v2 import FortuneTellingAgent

agent = FortuneTellingAgent()

print("=" * 50)
print("算命Agent测试 v2 (使用deepagents框架)")
print("=" * 50)

session_id = agent.create_session()
print(f"[新会话: {session_id[:8]}...]")

print("\n命令:")
print("  - 直接输入消息进行对话")
print("  - 输入 'exit' 退出")
print()

while True:
    try:
        user_input = input("您: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("\n再见！")
            break
        
        response = agent.process_input(user_input, session_id)
        print(f"\nAgent: {response}\n")
        
    except KeyboardInterrupt:
        print("\n\n再见！")
        break
    except Exception as e:
        print(f"\n[错误: {e}]\n")
