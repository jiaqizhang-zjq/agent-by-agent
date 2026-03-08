import os
import json
import uuid
import logging
from datetime import datetime, timedelta

# 配置日志
logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, storage_dir="sessions"):
        self.storage_dir = storage_dir
        self.sessions = {}
        self.expiry_time = timedelta(hours=24)  # 会话有效期24小时
        
        try:
            # 创建会话存储目录
            if not os.path.exists(self.storage_dir):
                os.makedirs(self.storage_dir)
            
            # 加载已有的会话
            self._load_sessions()
        except Exception as e:
            logger.error(f"初始化会话管理器失败: {e}")
    
    def create_session(self):
        """创建新会话并返回会话ID"""
        try:
            session_id = str(uuid.uuid4())
            session_data = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
                "context": {},
                "state": "greeting"
            }
            self.sessions[session_id] = session_data
            self._save_session(session_id)
            logger.info(f"创建新会话: {session_id}")
            return session_id
        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            return None
    
    def get_session(self, session_id):
        """获取会话信息"""
        try:
            if session_id not in self.sessions:
                # 尝试从文件加载
                session_file = os.path.join(self.storage_dir, f"{session_id}.json")
                if os.path.exists(session_file):
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                        self.sessions[session_id] = session_data
                else:
                    logger.warning(f"会话文件不存在: {session_id}")
                    return None
            
            # 检查会话是否过期
            last_activity = datetime.fromisoformat(self.sessions[session_id]["last_activity"])
            if datetime.now() - last_activity > self.expiry_time:
                logger.info(f"会话已过期: {session_id}")
                self.delete_session(session_id)
                return None
            
            # 更新最后活动时间
            self.sessions[session_id]["last_activity"] = datetime.now().isoformat()
            self._save_session(session_id)
            
            return self.sessions[session_id]
        except Exception as e:
            logger.error(f"获取会话失败: {session_id}, 错误: {e}")
            return None
    
    def update_session(self, session_id, data):
        """更新会话信息"""
        try:
            if session_id in self.sessions:
                self.sessions[session_id].update(data)
                self.sessions[session_id]["last_activity"] = datetime.now().isoformat()
                self._save_session(session_id)
                return True
            logger.warning(f"会话不存在: {session_id}")
            return False
        except Exception as e:
            logger.error(f"更新会话失败: {session_id}, 错误: {e}")
            return False
    
    def delete_session(self, session_id):
        """删除会话"""
        try:
            if session_id in self.sessions:
                del self.sessions[session_id]
            
            # 删除会话文件
            session_file = os.path.join(self.storage_dir, f"{session_id}.json")
            if os.path.exists(session_file):
                os.remove(session_file)
            logger.info(f"删除会话: {session_id}")
        except Exception as e:
            logger.error(f"删除会话失败: {session_id}, 错误: {e}")
    
    def _save_session(self, session_id):
        """保存会话到文件"""
        try:
            session_file = os.path.join(self.storage_dir, f"{session_id}.json")
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions[session_id], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存会话失败: {session_id}, 错误: {e}")
    
    def _load_sessions(self):
        """加载所有会话"""
        try:
            if os.path.exists(self.storage_dir):
                for filename in os.listdir(self.storage_dir):
                    if filename.endswith(".json"):
                        session_id = filename[:-5]  # 移除.json后缀
                        session_file = os.path.join(self.storage_dir, filename)
                        try:
                            with open(session_file, 'r', encoding='utf-8') as f:
                                session_data = json.load(f)
                                # 检查会话是否过期
                                last_activity = datetime.fromisoformat(session_data["last_activity"])
                                if datetime.now() - last_activity <= self.expiry_time:
                                    self.sessions[session_id] = session_data
                                else:
                                    # 删除过期会话
                                    os.remove(session_file)
                                    logger.info(f"删除过期会话: {session_id}")
                        except Exception as e:
                            logger.error(f"加载会话 {session_id} 失败: {e}")
        except Exception as e:
            logger.error(f"加载会话失败: {e}")
    
    def cleanup_expired_sessions(self):
        """清理过期会话"""
        try:
            expired_sessions = []
            for session_id, session_data in self.sessions.items():
                last_activity = datetime.fromisoformat(session_data["last_activity"])
                if datetime.now() - last_activity > self.expiry_time:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                self.delete_session(session_id)
            logger.info(f"清理了 {len(expired_sessions)} 个过期会话")
        except Exception as e:
            logger.error(f"清理过期会话失败: {e}")