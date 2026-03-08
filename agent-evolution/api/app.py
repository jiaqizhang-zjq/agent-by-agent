from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from src.agents.fortune_telling.fortune_agent import FortuneTellingAgent

app = FastAPI(
    title="算命Agent API",
    description="支持多用户并发访问的算命Agent API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建全局Agent实例
agent = FortuneTellingAgent()

# 请求和响应模型
class MessageRequest(BaseModel):
    message: str

class SessionResponse(BaseModel):
    session_id: str

class MessageResponse(BaseModel):
    response: str

@app.post("/api/sessions", response_model=SessionResponse)
async def create_session():
    """创建新会话"""
    try:
        session_id = agent.create_session()
        return SessionResponse(session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建会话失败: {str(e)}")

@app.post("/api/sessions/{session_id}/message", response_model=MessageResponse)
async def send_message(session_id: str, request: MessageRequest):
    """发送消息到会话"""
    try:
        response = agent.process_input(request.message, session_id)
        return MessageResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理消息失败: {str(e)}")

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    try:
        agent.delete_session(session_id)
        return {"message": "会话已删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除会话失败: {str(e)}")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用算命Agent API",
        "endpoints": {
            "create_session": "POST /api/sessions",
            "send_message": "POST /api/sessions/{session_id}/message",
            "delete_session": "DELETE /api/sessions/{session_id}"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)