"""
智能Agent - 使用LangChain和deepagents中间件

使用LangChain的ChatOpenAI模型和deepagents的中间件
"""

import os
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool

# 设置mem0目录到项目目录
os.environ["MEM0_DIR"] = str(Path(__file__).parent.parent.parent.parent / ".mem0")

from mem0 import Memory

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class AgentState:
    """Agent状态"""
    context: Dict[str, Any] = field(default_factory=dict)
    message_history: List[Dict[str, str]] = field(default_factory=list)
    skills_metadata: List = field(default_factory=list)


class SkillsLoader:
    """Skills加载器 - 加载Skills元数据"""
    
    def __init__(self, skills_dir: str = ".agents/skills"):
        self.skills_dir = Path(skills_dir)
        self.skills: List[Dict[str, Any]] = []
        self._load_skills()
    
    def _load_skills(self):
        """加载所有Skills"""
        if not self.skills_dir.exists():
            logger.warning(f"Skills目录不存在: {self.skills_dir}")
            return
        
        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir():
                skill_md = skill_path / "SKILL.md"
                if skill_md.exists():
                    skill = self._parse_skill_md(skill_md)
                    if skill:
                        self.skills.append(skill)
                        logger.info(f"加载Skill: {skill['name']} - {skill['description']}")
    
    def _parse_skill_md(self, skill_md: Path) -> Optional[Dict[str, Any]]:
        """解析SKILL.md文件"""
        content = skill_md.read_text(encoding="utf-8")
        
        # 解析YAML frontmatter
        if not content.startswith("---"):
            return None
        
        try:
            end_idx = content.find("---", 3)
            if end_idx == -1:
                return None
            
            import yaml
            frontmatter_str = content[3:end_idx].strip()
            frontmatter_data = yaml.safe_load(frontmatter_str)
            
            return {
                "name": frontmatter_data.get("name", skill_md.parent.name),
                "description": frontmatter_data.get("description", ""),
                "path": str(skill_md),
                "content": content
            }
        except Exception as e:
            logger.error(f"解析SKILL.md失败: {e}")
            return None
    
    def get_skills_prompt(self) -> str:
        """生成Skills的system prompt"""
        if not self.skills:
            return ""
        
        prompt = "\n## Skills System\n\n"
        prompt += "You have access to a skills library that provides specialized capabilities.\n\n"
        prompt += "**Available Skills:**\n\n"
        
        for skill in self.skills:
            prompt += f"- **{skill['name']}**: {skill['description']}\n"
            prompt += f"  -> Path: `{skill['path']}`\n\n"
        
        prompt += """
**How to Use Skills (Progressive Disclosure):**

1. **Recognize when a skill applies**: Check if the user's task matches a skill's description
2. **Read the skill's full instructions**: Use the `read_file` tool with the path shown above
3. **Follow the skill's instructions**: SKILL.md contains step-by-step workflows
4. **Execute skill scripts**: Skills may contain Python scripts - use `execute` tool to run them

**Example Workflow:**

User: "分析我的八字"

1. Check available skills -> See "bazi-analysis" skill
2. Use `read_file` tool to read the skill: read_file(file_path="/path/to/bazi-analysis/SKILL.md")
3. Follow the skill's instructions
4. Execute any helper scripts if needed
"""
        return prompt


@tool
def read_file(file_path: str) -> str:
    """
    读取文件内容。
    
    Args:
        file_path: 文件的绝对路径
    
    Returns:
        文件内容
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"Error: File not found: {file_path}"
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"


@tool
def execute(command: str) -> str:
    """
    执行shell命令。
    
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
            timeout=30
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error executing command: {e}"


@tool
def update_user_info(birth_date: str = None, birth_time: str = None, gender: str = None, location: str = None) -> str:
    """
    更新用户信息。当用户提供了出生日期、时间、性别等信息时，使用此工具保存。
    
    Args:
        birth_date: 出生日期，格式YYYY-MM-DD
        birth_time: 出生时间，格式HH:MM
        gender: 性别，"男"或"女"
        location: 出生地点
    
    Returns:
        更新结果
    """
    global _user_context
    if birth_date:
        _user_context["birth_date"] = birth_date
    if birth_time:
        _user_context["birth_time"] = birth_time
    if gender:
        _user_context["gender"] = gender
    if location:
        _user_context["location"] = location
    return f"已更新用户信息: {_user_context}"


# 全局用户context
_user_context = {}


class IntelligentAgent:
    """
    智能Agent - 使用LangChain和工具
    
    使用LangChain的ChatOpenAI模型和工具
    """
    
    def __init__(self):
        # 初始化LLM - 使用ChatOpenRouter
        self.llm = ChatOpenRouter(
            model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            temperature=0.7
        )
        
        # 绑定工具
        self.tools = [read_file, execute, update_user_info]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # 初始化Skills加载器
        skills_dir = Path(__file__).parent.parent.parent.parent / ".agents/skills"
        self.skills_loader = SkillsLoader(str(skills_dir))
        
        # 初始化mem0记忆系统（暂时禁用，需要torch依赖）
        # from mem0 import Memory
        # from mem0.configs.base import MemoryConfig
        # 
        # config = MemoryConfig()
        # config.llm.provider = "openai"
        # config.llm.config = {
        #     "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        #     "openai_api_key": os.getenv("OPENROUTER_API_KEY"),
        #     "openai_base_url": os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
        # }
        # config.embedder.provider = "huggingface"
        # config.embedder.config = {
        #     "model": "sentence-transformers/all-MiniLM-L6-v2",
        # }
        # self.memory = Memory(config)
        
        # 使用简单的记忆存储（临时方案）
        self.memory_store = {}
        self.memory_file = Path(__file__).parent.parent.parent.parent / "data" / "memory_store.json"
        self._load_memory()
        
        # 初始化状态
        self.state: AgentState = AgentState()
    
    def _load_memory(self):
        """从文件加载记忆"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory_store = json.load(f)
                logger.info(f"已加载记忆：{len(self.memory_store)}个用户")
            except Exception as e:
                logger.error(f"加载记忆失败：{e}")
                self.memory_store = {}
    
    def _save_memory(self):
        """保存记忆到文件"""
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_store, f, ensure_ascii=False, indent=2)
            logger.info(f"已保存记忆：{len(self.memory_store)}个用户")
        except Exception as e:
            logger.error(f"保存记忆失败：{e}")
    
    def chat(self, user_input: str, user_id: str = "default_user") -> str:
        """处理用户输入"""
        # 简单的记忆搜索（临时方案）
        relevant_memories = []
        if user_id in self.memory_store:
            for memory in self.memory_store[user_id]:
                if any(keyword in memory.lower() for keyword in user_input.lower().split()):
                    relevant_memories.append(memory)
        
        memories_str = "\n".join(f"- {memory}" for memory in relevant_memories[:3])
        
        # 添加用户消息到历史
        self.state.message_history.append({"role": "user", "content": user_input})
        
        # 构建system prompt
        system_prompt = self._build_system_prompt()
        
        # 如果有相关记忆，添加到system prompt
        if memories_str:
            system_prompt += f"\n\n## Relevant Memories\n\n{memories_str}"
        
        # 将所有记忆也注入到system prompt（不仅仅是相关的）
        if user_id in self.memory_store and self.memory_store[user_id]:
            all_memories = "\n".join(f"- {memory}" for memory in self.memory_store[user_id])
            system_prompt += f"\n\n## All User Memories\n\n{all_memories}"
        
        # 构建messages
        messages = [SystemMessage(content=system_prompt)]
        for msg in self.state.message_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # 记录请求
        self._log_request(messages, purpose="对话")
        
        # 调用LLM
        response = self.llm_with_tools.invoke(messages)
        
        # 记录原始响应
        self._log_raw_response(response)
        
        # 处理工具调用
        while response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                # 打印工具调用日志
                print(f"\n[工具调用] {tool_name}({tool_args})", file=sys.stderr)
                
                # 执行工具
                if tool_name == "read_file":
                    result = read_file.invoke(tool_args)
                elif tool_name == "execute":
                    result = execute.invoke(tool_args)
                elif tool_name == "update_user_info":
                    result = update_user_info.invoke(tool_args)
                    # 更新state.context
                    if "birth_date" in tool_args and tool_args["birth_date"]:
                        self.state.context["birth_date"] = tool_args["birth_date"]
                    if "birth_time" in tool_args and tool_args["birth_time"]:
                        self.state.context["birth_time"] = tool_args["birth_time"]
                    if "gender" in tool_args and tool_args["gender"]:
                        self.state.context["gender"] = tool_args["gender"]
                    if "location" in tool_args and tool_args["location"]:
                        self.state.context["location"] = tool_args["location"]
                else:
                    result = f"Unknown tool: {tool_name}"
                
                # 打印工具结果日志（截断）
                result_preview = result[:200] + "..." if len(result) > 200 else result
                print(f"[工具结果] {result_preview}\n", file=sys.stderr)
                
                # 添加工具结果到消息
                from langchain_core.messages import ToolMessage
                messages.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
            
            # 继续调用LLM
            response = self.llm_with_tools.invoke(messages)
            
            # 记录原始响应
            self._log_raw_response(response)
        
        # 提取响应
        content = response.content if response.content else "好的"
        
        # 从additional_kwargs中获取reasoning_content
        reasoning = response.additional_kwargs.get("reasoning_content", "")
        
        # 添加助手消息到历史
        self.state.message_history.append({"role": "assistant", "content": content})
        
        # 将对话添加到记忆存储（临时方案）
        if user_id not in self.memory_store:
            self.memory_store[user_id] = []
        
        # 简单的记忆提取：存储用户的关键信息
        if "出生" in user_input or "生日" in user_input or "性别" in user_input:
            self.memory_store[user_id].append(f"用户说：{user_input}")
            # 保存记忆到文件
            self._save_memory()
        
        return content
    
    def _build_system_prompt(self) -> str:
        """构建system prompt"""
        prompt = """你是一个智能命理分析助手。

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
        
        # 注入Skills
        prompt += self.skills_loader.get_skills_prompt()
        
        # 注入用户信息
        if self.state.context:
            prompt += f"\n## Current User Information\n\n{json.dumps(self.state.context, ensure_ascii=False, indent=2)}\n"
        else:
            prompt += "\n## Current User Information\n\nNo user information collected yet.\n"
        
        return prompt
    
    def _log_request(self, messages, purpose: str = "LLM调用"):
        """记录请求"""
        print(f"\n{'█'*60}", file=sys.stderr)
        print(f"█ [{purpose}]", file=sys.stderr)
        print(f"{'█'*60}", file=sys.stderr)
        print(f"█ Prompt:", file=sys.stderr)
        for i, msg in enumerate(messages):
            role = type(msg).__name__
            content = msg.content if hasattr(msg, 'content') else str(msg)
            print(f"█ [{i}] {role}:", file=sys.stderr)
            for line in str(content).split('\n')[:50]:  # 限制行数
                print(f"█   {line}", file=sys.stderr)
    
    def _log_raw_response(self, response):
        """记录原始响应到文件和控制台"""
        import json
        
        # 构建原始响应的完整JSON
        raw_response = {
            "id": response.response_metadata.get("id", ""),
            "object": response.response_metadata.get("object", ""),
            "created": response.response_metadata.get("created", 0),
            "model": response.response_metadata.get("model_name", ""),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response.content,
                    "reasoning": response.additional_kwargs.get("reasoning_content", ""),
                    "tool_calls": response.tool_calls if response.tool_calls else None
                },
                "finish_reason": response.response_metadata.get("finish_reason", "")
            }],
            "usage": {
                "prompt_tokens": response.usage_metadata.get("input_tokens", 0),
                "completion_tokens": response.usage_metadata.get("output_tokens", 0),
                "total_tokens": response.usage_metadata.get("total_tokens", 0),
                "completion_tokens_details": {
                    "reasoning_tokens": response.usage_metadata.get("output_token_details", {}).get("reasoning", 0)
                }
            }
        }
        
        # 输出到控制台 - 完整原始JSON
        print("\n" + "="*60, file=sys.stderr)
        print("【LLM原始响应】", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(json.dumps(raw_response, ensure_ascii=False, indent=2), file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)
        
        # 同时写入文件
        log_file = Path(__file__).parent.parent.parent.parent / "logs" / "llm_raw.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(raw_response, ensure_ascii=False) + '\n')
    
    def _log_response(self, content: str, reasoning: str = ""):
        """记录响应"""
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
    
    def get_context(self) -> Dict[str, Any]:
        """获取当前context"""
        return self.state.context
    
    def set_context(self, context: Dict[str, Any]):
        """设置context"""
        self.state.context = context
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.state.message_history
    
    def set_history(self, history: List[Dict[str, str]]):
        """设置对话历史"""
        self.state.message_history = history
