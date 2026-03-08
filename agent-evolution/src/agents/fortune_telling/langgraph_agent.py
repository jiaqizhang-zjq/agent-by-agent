"""LangGraph版本的算命Agent"""

import os
from typing import Annotated
from pathlib import Path

from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

# 设置mem0目录
os.environ["MEM0_DIR"] = str(Path(__file__).parent.parent.parent.parent / ".mem0")


# 定义工具
@tool
def update_user_info(birth_date: str = "", birth_time: str = "", gender: str = "", location: str = "") -> str:
    """更新用户信息
    
    Args:
        birth_date: 出生日期，格式：YYYY-MM-DD
        birth_time: 出生时间，格式：HH:MM
        gender: 性别，男/女
        location: 出生地点
    
    Returns:
        更新结果
    """
    import json
    from pathlib import Path
    
    # 读取现有context
    context_file = Path(__file__).parent.parent.parent.parent / "data" / "user_context.json"
    context_file.parent.mkdir(parents=True, exist_ok=True)
    
    if context_file.exists():
        with open(context_file, 'r', encoding='utf-8') as f:
            context = json.load(f)
    else:
        context = {}
    
    # 更新context
    if birth_date:
        context["birth_date"] = birth_date
    if birth_time:
        context["birth_time"] = birth_time
    if gender:
        context["gender"] = gender
    if location:
        context["location"] = location
    
    # 保存context
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    
    return f"用户信息已更新：{context}"


@tool
def read_file(path: str) -> str:
    """读取文件内容
    
    Args:
        path: 文件路径
    
    Returns:
        文件内容
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败：{str(e)}"


@tool
def execute(command: str) -> str:
    """执行shell命令
    
    Args:
        command: 要执行的命令
    
    Returns:
        命令输出
    """
    import subprocess
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout or result.stderr
    except Exception as e:
        return f"执行失败：{str(e)}"


# 定义工具列表
tools = [update_user_info, read_file, execute]


# 创建模型
model = ChatOpenRouter(
    model=os.getenv("OPENROUTER_MODEL", "stepfun/step-3.5-flash:free"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
    temperature=0.7,
    max_tokens=8000
)


# 绑定工具到模型
model_with_tools = model.bind_tools(tools)


# 定义Agent状态
class AgentState(MessagesState):
    """Agent状态，包含消息历史"""
    pass


# 定义Agent节点
def agent_node(state: AgentState) -> AgentState:
    """Agent节点：调用LLM"""
    # 构建system prompt
    system_prompt = """你是一个智能命理分析助手。

你的能力：
1. 可以和用户自然对话
2. 可以从对话中提取用户信息（出生日期、时间、性别等）
3. 可以进行八字命理分析

规则：
- 自然对话，不要强制要求用户提供信息
- 如果用户提供了出生信息，**必须**调用 update_user_info 工具保存信息
- 如果用户要求分析，检查是否有足够信息
- 如果信息不足，友好询问
- 如果信息足够，使用Skills进行分析
- **简洁回复**：简单问候时回复要简短（1-2句话），不要重复之前的信息

工具使用：
- **update_user_info**: 当用户提供出生信息时，**必须**调用此工具保存信息
- **read_file**: 读取SKILL.md文件
- **execute**: 执行Python脚本
"""
    
    # 构建消息列表
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    # 调用模型
    response = model_with_tools.invoke(messages)
    
    # 返回更新后的状态
    return {"messages": [response]}


# 定义条件函数
def should_continue(state: AgentState) -> str:
    """判断是否继续执行工具"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # 如果最后一条消息有工具调用，继续执行工具
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # 否则结束
    return END


# 创建图
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

# 添加边
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

# 编译图（不使用checkpointer，LangGraph API会自动处理）
graph = workflow.compile()
