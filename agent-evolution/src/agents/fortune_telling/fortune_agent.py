import os
import sys
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGSMITH_TRACING"] = "false"

load_dotenv()

from src.agents.fortune_telling.intelligent_agent import IntelligentAgent
from src.agents.fortune_telling.components.session_manager import SessionManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '../../../logs/fortune_telling.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class FortuneTellingAgent:
    """算命Agent - 使用IntelligentAgent"""
    
    def __init__(self):
        try:
            self.session_manager = SessionManager(os.path.join(os.path.dirname(__file__), '../../../sessions'))
            logger.info("算命Agent初始化成功")
        except Exception as e:
            logger.error(f"算命Agent初始化失败: {e}")
            raise
    
    def create_session(self):
        try:
            session_id = self.session_manager.create_session()
            if session_id:
                logger.info(f"创建会话成功: {session_id}")
                return session_id
            else:
                logger.error("创建会话失败")
                return None
        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            return None
    
    def process_input(self, user_input, session_id):
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                logger.warning(f"会话不存在或已过期: {session_id}")
                return "会话已过期或不存在，请重新开始对话。"
            
            timestamp = datetime.now().isoformat()
            
            # 创建IntelligentAgent并恢复状态
            agent = IntelligentAgent()
            agent.set_context(session.get("context", {}))
            agent.set_history(session.get("message_history", []))
            
            logger.info(f"恢复会话: context={agent.get_context()}, history_count={len(agent.get_history())}")
            
            # 处理用户输入
            response = agent.chat(user_input)
            
            # 保存状态
            session_data = {
                "context": agent.get_context(),
                "message_history": agent.get_history()
            }
            self.session_manager.update_session(session_id, session_data)
            
            # 记录日志
            log_entry = {
                "timestamp": timestamp,
                "session_id": session_id,
                "user_input": user_input,
                "agent_output": response,
                "context": agent.get_context()
            }
            
            try:
                log_file = os.path.join(os.path.dirname(__file__), '../../../logs/fortune_telling.jsonl')
                with open(log_file, 'a', encoding='utf-8') as f:
                    json.dump(log_entry, f, ensure_ascii=False)
                    f.write('\n')
            except Exception as e:
                logger.error(f"写入日志失败: {e}")
            
            logger.info(f"Session {session_id} - User input: {user_input}")
            logger.info(f"Session {session_id} - Agent output: {response[:100]}...")
            
            return response
        except Exception as e:
            logger.error(f"处理输入失败: {e}")
            return "抱歉，处理您的请求时出现错误，请稍后再试。"
    
    def delete_session(self, session_id):
        try:
            self.session_manager.delete_session(session_id)
            logger.info(f"删除会话成功: {session_id}")
        except Exception as e:
            logger.error(f"删除会话失败: {e}")
