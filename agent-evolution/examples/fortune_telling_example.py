import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

def main():
    agent = FortuneTellingAgent()
    print("欢迎使用命理分析助手！")
    print("我可以为您提供八字分析、性格解读和运势预测。")
    print("输入'退出'或'结束'可以退出对话。")
    print("=" * 50)
    
    while True:
        user_input = input("您：")
        if user_input.lower() in ["退出", "结束", "bye"]:
            print("命理助手：再见！祝您一切顺利！")
            break
        
        response = agent.process_input(user_input)
        print(f"命理助手：{response}")

if __name__ == "__main__":
    main()