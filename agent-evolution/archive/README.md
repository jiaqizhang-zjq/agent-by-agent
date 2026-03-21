# 项目归档说明

## 归档时间

2026-03-21

## 归档原因

本项目是一个Demo项目，已完成算命Agent的开发和测试验证。为了保持项目结构清晰，将除third_party之外的产物归档。

## 归档内容

### 1. 源代码 (src/)
- `src/agents/fortune_telling/` - 算命Agent实现
  - `fortune_agent.py` - 包装类
  - `intelligent_agent.py` - 主要实现
  - `langgraph_agent.py` - LangGraph版本（开发中）
  - `components/` - 组件
    - `session_manager.py` - 会话管理

### 2. 文档 (docs/)
- `docs/architecture/` - 架构设计
  - `agent_design.md` - Agent设计文档
  - `agent_versions.md` - Agent版本历史
- `docs/guides/` - 使用指南
  - `evaluation.md` - 评估方法
- `docs/iterations/` - 迭代记录
  - `2026-03-08.md` - 迭代记录
  - `README.md` - 迭代记录总览
- `docs/development/` - 开发文档
  - `iteration_process.md` - 迭代过程规范
- `docs/README.md` - 文档总览

### 3. 测试代码 (tests/)
- `test_agent_full.py` - 完整测试
- `test_multi_turn.py` - 多轮对话测试
- `test_memory_effect.py` - 记忆效果测试
- `test_real_multi_turn.py` - 真实多轮对话测试
- `test_agent_auto.py` - 自动测试
- `test_fortune_agent_e2e.py` - 端到端测试
- `test_llm_raw.py` - LLM原始测试
- `test_cases.md` - 测试用例

### 4. 示例代码 (examples/)
- `fortune_interactive_test.py` - 交互式测试
- `fortune_telling_example.py` - 示例代码
- `fortune_telling_test.py` - 测试代码
- `fortune_llm_test.py` - LLM测试
- `auto_test.py` - 自动测试
- `test_llm.py` - LLM测试

### 5. 数据文件 (data/)
- `memory_store.json` - 记忆存储
- `test_report.json` - 测试报告

### 6. API代码 (api/)
- `app.py` - API应用

### 7. 经验池 (experience/)
- `experience_pool.md` - 经验池

### 8. 配置文件 (config/)
- 配置文件

### 9. 备忘录 (memos/)
- 备忘录文件

### 10. 脚本 (scripts/)
- 脚本文件

### 11. 日志 (logs/)
- 日志文件

### 12. 会话 (sessions/)
- 会话文件

## 保留内容

### 1. 第三方库 (third-party/)
- `langchain/` - LangChain库
- `langgraph/` - LangGraph库
- `mem0/` - Mem0库
- `deepagents/` - DeepAgents库

### 2. 项目配置文件
- `.gitignore` - Git忽略文件
- `.env.example` - 环境变量示例
- `requirements.txt` - 依赖文件
- `setup.py` - 安装脚本
- `install.sh` - 安装脚本
- `setup-env.sh` - 环境设置脚本

### 3. 项目文档
- `README.md` - 项目说明
- `project.md` - 项目概述
- `project_ai.md` - AI项目设计
- `heartbeat.md` - 心跳文件

### 4. Skills系统
- `.agents/skills/` - Skills目录
  - `bazi-analysis/` - 八字分析Skill
  - `fortune-telling/` - 算命Skill

## 项目成果

### 测试结果
- 测试时间: 2026-03-08 19:50:00
- 测试环境: Python 3.13.12
- 测试模型: stepfun/step-3.5-flash:free
- 总用例数: 65
- 通过数: 65 ✅
- 失败数: 0 ❌
- 通过率: **100.0%** 🎉

### 主要功能
1. ✅ 多轮对话支持
2. ✅ 用户信息自动提取
3. ✅ 记忆系统（mem0）
4. ✅ Skills系统集成
5. ✅ 会话管理
6. ✅ 日志记录

### Agent版本
- v1: `fortune_agent.py` - 包装类（当前使用）
- v3: `intelligent_agent.py` - 主要实现（当前使用）
- v4: `langgraph_agent.py` - LangGraph版本（开发中）

## 后续计划

1. 完善LangGraph版本Agent
2. 添加更多Skills
3. 优化记忆系统
4. 提升用户体验

## 联系方式

如有问题，请联系项目负责人。
