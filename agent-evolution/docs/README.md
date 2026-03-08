# 项目文档总览

本文件提供项目所有重要文档的总览，帮助快速找到所需的知识和信息。

## 文档结构

```
docs/
├── README.md                    # 本文件
├── architecture/                # 架构设计
│   ├── agent_design.md         # Agent设计文档
│   └── agent_versions.md       # Agent版本历史
├── guides/                      # 使用指南
│   └── evaluation.md           # 评估方法
├── iterations/                  # 迭代记录
│   ├── README.md               # 迭代记录总览
│   └── 2026-03-08.md           # 具体迭代记录
└── development/                 # 开发文档
    └── iteration_process.md    # 迭代过程规范
```

## 核心文档

### 1. 架构设计

- **[Agent设计文档](./architecture/agent_design.md)**
  - Agent的架构设计和实现方案
  - 核心组件、数据流、技术栈
  - 对话流程、知识库设计

- **[Agent版本历史](./architecture/agent_versions.md)**
  - Agent的版本演进历史
  - 当前版本和过期版本
  - 版本对比和使用建议

### 2. 使用指南

- **[评估方法](./guides/evaluation.md)**
  - Agent的评估指标和方法
  - 测试用例分类
  - 测试报告格式

### 3. 迭代记录

- **[迭代记录总览](./iterations/README.md)**
  - 所有迭代记录的列表
  - 迭代统计信息
  - 如何创建新的迭代记录

- **[2026-03-08迭代记录](./iterations/2026-03-08.md)**
  - 完成算命Agent的基础功能实现和测试验证
  - 测试通过率100%（65个测试用例）

### 4. 开发文档

- **[迭代过程规范](./development/iteration_process.md)**
  - 迭代周期定义
  - 迭代阶段划分
  - 迭代记录模板

## 快速导航

### 我想了解Agent的设计

→ 查看 [Agent设计文档](./architecture/agent_design.md)

### 我想了解Agent的版本历史

→ 查看 [Agent版本历史](./architecture/agent_versions.md)

### 我想了解如何评估Agent

→ 查看 [评估方法](./guides/evaluation.md)

### 我想查看迭代记录

→ 查看 [迭代记录总览](./iterations/README.md)

### 我想了解迭代过程规范

→ 查看 [迭代过程规范](./development/iteration_process.md)

## 其他重要文档

### 项目规划文档

- **project.md**
  - 路径：`/agent-evolution/project.md`
  - 用途：给人看的项目规划文档，包含详细的项目设计、架构和流程
  - 内容：项目概述、设计目标、框架设计思想、核心模块、任务规划、评估标准等

### 经验池

- **experience_pool.md**
  - 路径：`/agent-evolution/experience/experience_pool.md`
  - 用途：记录开发过程中的经验教训，为后续开发提供参考
  - 内容：成功经验、失败教训、最佳实践、常见问题等

## 文档维护

### 如何添加新文档

1. 确定文档类型（架构设计、使用指南、迭代记录、开发文档）
2. 在对应的目录下创建新文件
3. 更新本README.md文件，添加新文档的链接

### 如何更新文档

1. 修改对应的文档文件
2. 如果文档结构发生变化，更新本README.md文件

## 文档规范

### 文档命名规范

- 使用小写字母和下划线
- 文件名要有意义，能反映文档内容
- 例如：`agent_design.md`、`evaluation.md`

### 文档内容规范

- 每个文档开头要有简短的描述
- 使用清晰的标题层级
- 使用列表、表格等格式提高可读性
- 添加相关文档的链接

## 联系方式

如有问题，请联系项目负责人。

---

最后更新时间：2026-03-08
