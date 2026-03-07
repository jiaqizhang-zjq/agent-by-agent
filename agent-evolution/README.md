# Agent自我进化项目

## 项目概述

本项目旨在构建一个Agent自我进化系统，利用Agent生成和优化完成特定目标任务的Agent。通过自动化的生成、执行和评估流程，实现Agent的持续进化和性能提升。

## 重要文档导航

### 项目规划文档
- **project.md**：给人看的项目规划文档，包含详细的设计思想和规划
- **project_ai.md**：给AI看的项目规划文档，包含结构化的项目信息

### 流程文档
- **docs/iteration_process.md**：迭代过程文档，记录迭代过程和经验提取
- **heartbeat.md**：心跳提醒文档，定时提醒AI关于Agent的进化计划

### 技术文档
- **third-party/README.md**：第三方开源工具说明，包含依赖的开源框架和库

## 目录结构

```
agent-evolution/
├── src/                  # 源代码目录
│   ├── core/             # 核心引擎
│   ├── agents/           # Agent管理
│   ├── tasks/            # 任务管理
│   ├── evaluation/       # 评估系统
│   ├── tools/            # 工具库
│   ├── utils/            # 通用工具
│   └── api/              # API接口
├── config/               # 配置文件
├── tests/                # 测试目录
├── docs/                 # 文档目录
├── examples/             # 示例目录
├── scripts/              # 脚本目录
├── experience/           # 经验池目录
│   ├── raw/              # 原始经验数据
│   ├── processed/        # 处理后的经验
│   ├── patterns/         # 识别的模式
│   └── solutions/        # 解决方案库
├── memos/                # 项目备忘录目录
│   ├── daily/            # 每日记录
│   ├── weekly/           # 每周记录
│   ├── monthly/          # 每月记录
│   └── quarterly/        # 季度记录
├── third-party/          # 第三方开源工具
├── project.md            # 项目规划文档（给人看）
├── project_ai.md         # 项目规划文档（给AI看）
├── heartbeat.md          # 心跳提醒文档
├── requirements.txt      # 项目依赖
└── README.md             # 项目导航文档
```

## 依赖说明

### 核心依赖
- **Python**：3.8+
- **Agent框架**：LangChain、LangGraph、DeepAgent等
- **Memory**：Mem0
- **Skill**：技能管理系统
- **MCP**：多通道协议

### 安装方法

```bash
pip install -r requirements.txt
```

## 快速开始

1. **安装依赖**：`pip install -r requirements.txt`
2. **配置项目**：修改 `config/` 目录下的配置文件
3. **启动核心引擎**：`python src/core/engine.py`
4. **运行示例**：`python examples/basic/example.py`
5. **访问API**：默认地址 `http://localhost:8000`

## 项目流程

1. **任务定义**：Boss给出具体任务目标和评估指标
2. **Agent搭建**：AI负责基于开源项目或自主生成的方式搭建Agent
3. **测试管理**：负责测试case的编造、执行、收集反馈、记录和分析优化方案
4. **迭代优化**：基于测试结果和反馈信息，形成迭代计划，持续优化Agent

## 经验池管理

经验池用于存储和管理项目经验，包括：
- **原始记录**：完整的迭代记录
- **经验提取**：提取的经验教训和知识
- **模式识别**：识别的模式和最佳实践
- **解决方案**：可直接应用的解决方案和建议

## 心跳提醒机制

为确保Agent进化计划的持续推进，项目采用心跳提醒机制：
- **每日提醒**：每天上午9:00
- **每周提醒**：每周一上午9:00
- **每月提醒**：每月1日上午9:00
- **每季度提醒**：每季度首月1日上午9:00

## 贡献指南

1. **代码规范**：遵循PEP 8规范
2. **提交信息**：清晰、简洁的提交信息
3. **测试**：确保代码通过所有测试
4. **文档**：更新相关文档

## 许可证

[MIT License](LICENSE)
