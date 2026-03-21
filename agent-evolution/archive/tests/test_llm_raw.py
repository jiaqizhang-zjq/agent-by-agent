#!/usr/bin/env python3
"""最简单的LLM请求测试"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
)

print("测试1: 非流式请求")
print("=" * 60)

response = client.chat.completions.create(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    messages=[
        {"role": "user", "content": "你好"}
    ],
    temperature=0.7,
    max_tokens=100
)

print(f"Response type: {type(response)}")
print(f"Response: {response}")
print()

print("测试2: 流式请求")
print("=" * 60)

stream = client.chat.completions.create(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    messages=[
        {"role": "user", "content": "你好"}
    ],
    stream=True,
    temperature=0.7,
    max_tokens=100
)

print("Streaming chunks:")
for i, chunk in enumerate(stream):
    print(f"\nChunk {i}:")
    print(f"  Type: {type(chunk)}")
    print(f"  Raw: {chunk}")
    if chunk.choices and chunk.choices[0]:
        delta = chunk.choices[0].delta
        print(f"  Delta: {delta}")
        if hasattr(delta, '__dict__'):
            print(f"  Delta.__dict__: {delta.__dict__}")
