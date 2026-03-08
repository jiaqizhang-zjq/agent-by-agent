import os
import json
import logging
import subprocess
from typing import Optional
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.utils.function_calling import convert_to_openai_function

load_dotenv()

logger = logging.getLogger(__name__)


@tool
def bazi_analysis(birth_date: str, birth_time: str, gender: str) -> str:
    """
    分析用户的八字命盘。
    
    Args:
        birth_date: 出生日期，格式为YYYY-MM-DD
        birth_time: 出生时间，格式为HH:MM
        gender: 性别，"男"或"女"
    
    Returns:
        八字分析结果的JSON字符串
    """
    try:
        cmd = [
            "python",
            ".agents/skills/bazi-analysis/bazi_analyzer.py",
            birth_date,
            birth_time,
            gender,
            "--format", "json"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout
        else:
            return json.dumps({"error": result.stderr})
    except Exception as e:
        return json.dumps({"error": str(e)})


class DialogueManager:
    """智能对话管理器 - 使用LangChain Tool Calling"""
    
    def __init__(self):
        self.context = {}
        self.message_history = []
        self.tools = [bazi_analysis]
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
            model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            temperature=0.7
        ).bind_tools(self.tools)
    
    def process_input(self, user_input):
        # 构建消息
        messages = [
            SystemMessage(content=f"""你是一个智能命理分析助手。

当前已收集的用户信息：
{json.dumps(self.context, ensure_ascii=False, indent=2) if self.context else "暂无"}

你的能力：
1. 可以和用户自然对话
2. 可以从对话中提取用户信息（出生日期、时间、性别等）
3. 可以使用bazi_analysis工具进行八字分析

规则：
- 自然对话，不要强制要求用户提供信息
- 如果用户提供了出生信息，记住它
- 如果用户要求分析且有完整信息（birth_date, birth_time, gender），调用bazi_analysis工具
- 如果信息不足，友好询问""")
        ]
        
        # 添加历史
        for msg in self.message_history[-20:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # 添加当前输入
        messages.append(HumanMessage(content=user_input))
        self.message_history.append({"role": "user", "content": user_input})
        
        # 调用LLM
        response = self.llm.invoke(messages)
        
        # 检查是否有工具调用
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "bazi_analysis":
                    args = tool_call["args"]
                    # 更新context
                    self.context["birth_date"] = args["birth_date"]
                    self.context["birth_time"] = args["birth_time"]
                    self.context["gender"] = args["gender"]
                    
                    # 执行工具
                    result = bazi_analysis.invoke(args)
                    self.context["skill_result"] = json.loads(result)
                    
                    # 生成分析报告
                    analysis = self._generate_analysis(response.content or "")
                    self.message_history.append({"role": "assistant", "content": analysis})
                    return analysis
        
        # 没有工具调用，直接返回回复
        content = response.content or "好的"
        self.message_history.append({"role": "assistant", "content": content})
        return content
    
    def _generate_analysis(self, question):
        """生成分析报告"""
        try:
            skill_result = self.context.get("skill_result", {})
            
            prompt = f"""根据以下八字信息，回答用户的问题。

八字信息：
{json.dumps(skill_result, ensure_ascii=False, indent=2)}

用户问题：{question}

请给出详细、专业的分析。"""

            messages = [HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content if response.content else "分析完成"
        except Exception as e:
            logger.error(f"生成分析失败: {e}")
            return "分析完成"
