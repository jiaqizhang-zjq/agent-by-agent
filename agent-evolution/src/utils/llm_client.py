import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)


class LLMClient:
    """统一的LLM调用客户端，封装日志记录"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
        )
    
    def call(self, messages, purpose="LLM调用"):
        # 转换messages格式
        api_messages = []
        for msg in messages:
            role = "system" if "SystemMessage" in str(type(msg)) else ("assistant" if "AIMessage" in str(type(msg)) else "user")
            api_messages.append({"role": role, "content": msg.content})
        
        # 使用非流式API
        response = self.client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            messages=api_messages,
            temperature=0.7,
            max_tokens=8000,
            response_format={"type": "json_object"}
        )
        
        # 提取内容
        content = response.choices[0].message.content if response.choices else ""
        reasoning = ""
        if hasattr(response.choices[0].message, 'reasoning') and response.choices[0].message.reasoning:
            reasoning = response.choices[0].message.reasoning
        
        # 输出原始响应
        print(f"\n{'█'*60}", file=sys.stderr)
        print(f"█ [{purpose}]", file=sys.stderr)
        print(f"{'█'*60}", file=sys.stderr)
        print(f"█ Prompt:", file=sys.stderr)
        for i, msg in enumerate(messages):
            print(f"█ [{i}] {type(msg).__name__}:", file=sys.stderr)
            for line in msg.content.split('\n'):
                print(f"█   {line}", file=sys.stderr)
        print(f"{'─'*60}", file=sys.stderr)
        print(f"█ Response:", file=sys.stderr)
        if reasoning:
            print(f"█ 【思考过程】:", file=sys.stderr)
            for line in reasoning.split('\n'):
                print(f"█   {line}", file=sys.stderr)
            print(f"{'─'*40}", file=sys.stderr)
        print(f"█ 【回复内容】:", file=sys.stderr)
        for line in content.split('\n'):
            print(f"█   {line}", file=sys.stderr)
        print(f"{'█'*60}\n", file=sys.stderr)
        
        # 写入文件
        try:
            log_file = "logs/llm_calls.log"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"[{purpose}] - {datetime.now().isoformat()}\n")
                f.write(f"{'='*60}\n")
                f.write(f"Prompt:\n")
                for i, msg in enumerate(messages):
                    f.write(f"[{i}] {type(msg).__name__}:\n{msg.content}\n\n")
                if reasoning:
                    f.write(f"\n【思考过程】:\n{reasoning}\n")
                f.write(f"\n【回复内容】:\n{content}\n")
        except Exception as e:
            pass
        
        # 返回兼容的响应对象
        from langchain_core.messages import AIMessage
        return AIMessage(content=content)
    
    def invoke(self, messages, purpose="LLM调用"):
        """call方法的别名"""
        return self.call(messages, purpose)


llm_client = LLMClient()
