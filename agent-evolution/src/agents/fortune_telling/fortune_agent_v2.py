import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# 禁用LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

# 加载环境变量
load_dotenv()

from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
from deepagents.backends import StateBackend

# 配置日志 - 输出到文件和控制台，使用[DEBUG]前缀区分
class DebugFormatter(logging.Formatter):
    def format(self, record):
        return f"[DEBUG] {super().format(record)}"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '../../../logs/fortune_telling.log')),
        logging.StreamHandler()
    ]
)
# 为控制台handler设置自定义formatter
for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(DebugFormatter('%(asctime)s - %(message)s'))

logger = logging.getLogger(__name__)


FORTUNE_AGENT_PROMPT = """你是一位专业的命理大师，精通八字命理、周易预测。

## 核心行为

- 专业、详细、有理有据地回答用户问题
- 使用Skills系统进行分析
- 保持专业但易懂的语言风格

## 工作流程

1. **收集信息** - 收集用户的出生日期、时间、性别
2. **调用Skill** - 使用bazi-analysis skill进行八字分析
3. **生成回复** - 基于分析结果生成详细的命理分析

## Skills使用

当用户提供了出生信息后，使用bazi-analysis skill进行分析：

```bash
python .agents/skills/bazi-analysis/bazi_analyzer.py "出生日期" "出生时间" "性别" --format json
```

## 输出格式

1. 八字排盘
2. 五行分析
3. 性格特点
4. 运势解读
5. 具体建议
6. 开运指南

## 注意事项

- 命理分析仅供娱乐参考
- 命运掌握在自己手中
- 积极行动方能创造美好人生
"""


def create_fortune_agent():
    """创建算命Agent
    
    Returns:
        CompiledStateGraph: 配置好的算命Agent
    """
    # 配置模型
    model = init_chat_model(
        "openai:stepfun/step-3.5-flash:free",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
        temperature=0.7,
        max_tokens=8000
    )
    
    # 配置skills目录
    skills_dir = Path(".agents/skills")
    skills_sources = [str(skills_dir)]
    
    # 创建agent
    agent = create_deep_agent(
        model=model,
        system_prompt=FORTUNE_AGENT_PROMPT,
        skills=skills_sources,
        backend=StateBackend,
        debug=False
    )
    
    logger.info("算命Agent创建成功")
    return agent


class FortuneTellingAgent:
    """算命Agent - 使用deepagents框架"""
    
    def __init__(self):
        self.agent = create_fortune_agent()
        self.sessions = {}
        logger.info("算命Agent初始化成功")
    
    def create_session(self):
        """创建新会话"""
        import uuid
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "messages": [],
            "context": {}
        }
        logger.info(f"创建会话: {session_id}")
        return session_id
    
    def process_input(self, user_input, session_id):
        """处理用户输入"""
        if session_id not in self.sessions:
            return "会话不存在，请重新开始"
        
        session = self.sessions[session_id]
        
        # 调用agent
        from langchain_core.messages import HumanMessage
        result = self.agent.invoke({
            "messages": session["messages"] + [HumanMessage(content=user_input)]
        })
        
        # 更新会话
        session["messages"] = result["messages"]
        
        # 返回最后一条AI消息
        for msg in reversed(result["messages"]):
            if hasattr(msg, 'type') and msg.type == 'ai':
                return msg.content
        
        return "抱歉，我无法处理您的请求"
    
    def delete_session(self, session_id):
        """删除会话"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"删除会话: {session_id}")
