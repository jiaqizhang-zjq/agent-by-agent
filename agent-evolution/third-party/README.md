# 第三方开源工具

本目录用于存放项目依赖的开源工具源码。

## 依赖的开源工具

### Agent框架

1. **LangChain**
   - 用途：提供Agent开发的核心框架
   - 源码：`./langchain`
   - 文档：https://docs.langchain.com/

2. **LangGraph**
   - 用途：提供Agent工作流管理
   - 源码：`./langgraph`
   - 文档：https://docs.langchain.com/langgraph/

3. **DeepAgents**
   - 用途：提供深度Agent能力，包括Skills系统
   - 源码：`./deepagents`
   - 文档：https://github.com/langchain-ai/deepagents

### Memory

1. **Mem0**
   - 用途：提供Agent记忆管理
   - 源码：`./mem0`
   - 文档：https://github.com/mem0ai/mem0

### Skills系统

DeepAgents提供了Skills系统，用于定义和管理Agent的技能。

#### Skill结构

每个skill是一个目录，包含SKILL.md文件：

```
/skills/
└── skill-name/
    ├── SKILL.md          # Required: YAML frontmatter + markdown instructions
    └── helper.py         # Optional: supporting files
```

#### SKILL.md格式

```markdown
---
name: skill-name
description: What the skill does
license: MIT
---

# Skill Title

Instructions for using this skill...
```

#### 示例Skills

- `./deepagents/examples/content-builder-agent/skills/`
- `./deepagents/examples/text-to-sql-agent/skills/`

## 安装方法

使用项目根目录的requirements.txt文件安装所有依赖：

```bash
pip install -r requirements.txt
```

## 使用说明

1. **Agent框架**：在src/core/generators/和src/core/executors/中使用
2. **Memory**：在src/agents/storage/中使用
3. **Skill**：在.agents/skills/中使用（遵循deepagents规范）
4. **MCP**：在src/api/中使用

## 版本管理

依赖版本在requirements.txt文件中指定，确保项目的一致性和可重现性。
