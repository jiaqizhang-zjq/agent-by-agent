import sys
import os
import threading
import time
import itertools

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

class LoadingIndicator:
    """加载动画指示器"""
    
    def __init__(self):
        self._running = False
        self._thread = None
    
    def _animate(self):
        for c in itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']):
            if not self._running:
                break
            sys.stdout.write(f'\r{c} 处理中...')
            sys.stdout.flush()
            time.sleep(0.1)
    
    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._animate)
        self._thread.start()
    
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        sys.stdout.write('\r' + ' ' * 20 + '\r')
        sys.stdout.flush()

agent = FortuneTellingAgent()
loading = LoadingIndicator()

print("=" * 50)
print("算命Agent测试")
print("=" * 50)

import glob
session_files = glob.glob("sessions/*.json")
session_id = None

if session_files:
    latest_session = max(session_files, key=os.path.getmtime)
    session_id = os.path.basename(latest_session).replace(".json", "")
    print(f"[继续会话: {session_id[:8]}...]")
else:
    session_id = agent.create_session()
    print(f"[新会话: {session_id[:8]}...]")

print("\n命令:")
print("  - 直接输入消息进行对话")
print("  - 输入 'new' 创建新会话")
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
        
        if user_input.lower() in ["new", "新会话"]:
            session_id = agent.create_session()
            print(f"\n[新会话: {session_id[:8]}...]\n")
            continue
        
        # 显示加载动画
        loading.start()
        
        try:
            response = agent.process_input(user_input, session_id)
        finally:
            loading.stop()
        
        print(f"\nAgent: {response}\n")
        
    except KeyboardInterrupt:
        loading.stop()
        print("\n\n再见！")
        break
    except Exception as e:
        loading.stop()
        print(f"\n[错误: {e}]\n")
