# 第三方开源工具

本目录用于存放项目依赖的开源工具。由于网络限制，我们使用pip安装方式引入这些工具，而不是直接克隆仓库。

## 依赖的开源工具

### Agent框架

1. **LangChain**
   - 用途：提供Agent开发的核心框架
   - 安装：`pip install langchain`
   - 文档：https://docs.langchain.com/

2. **LangGraph**
   - 用途：提供Agent工作流管理
   - 安装：`pip install langgraph`
   - 文档：https://docs.langchain.com/langgraph/

3. **DeepAgent**
   - 用途：提供深度强化学习Agent能力
   - 安装：`pip install deepagent`
   - 文档：https://github.com/your-username/deepagent

### Memory

1. **Mem0**
   - 用途：提供Agent记忆管理
   - 安装：`pip install mem0`
   - 文档：https://github.com/mem0ai/mem0

### 其他工具

1. **Skill**
   - 用途：技能管理系统
   - 安装：根据具体实现选择合适的技能管理库

2. **MCP**
   - 用途：多通道协议
   - 安装：根据具体实现选择合适的MCP库

## 安装方法

使用项目根目录的requirements.txt文件安装所有依赖：

```bash
pip install -r requirements.txt
```

## 使用说明

1. **Agent框架**：在src/core/generators/和src/core/executors/中使用
2. **Memory**：在src/agents/storage/中使用
3. **Skill**：在src/tools/中使用
4. **MCP**：在src/api/中使用

## 版本管理

依赖版本在requirements.txt文件中指定，确保项目的一致性和可重现性。
