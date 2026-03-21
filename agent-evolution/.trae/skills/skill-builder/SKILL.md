---
name: "skill-builder"
description: "构建和进化Skills，与memory系统配合。当用户提到创建skill、优化skill、skill进化、添加新能力时调用。"
---

# Skill构建器

这个Skill用于构建、管理和进化Skills系统。

## 何时调用

在以下情况下调用此Skill：
- 用户要求"创建新skill"
- 用户要求"优化skill"
- 用户要求"skill进化"
- 用户要求"添加新能力"
- 用户提到skill相关的工作

## 核心功能

### 1. Skill构建

**创建新Skill的流程：**

1. **需求分析**
   - 理解用户需求
   - 确定Skill功能范围
   - 设计触发条件

2. **结构设计**
   - 创建`.trae/skills/<skill-name>/`目录
   - 编写SKILL.md文件
   - 定义frontmatter（name, description）
   - 编写详细说明

3. **进化机制**
   - 集成memory系统
   - 记录使用反馈
   - 自动优化建议

### 2. Skill进化机制

**自我迭代流程：**

```python
# 伪代码示例
class SkillEvolution:
    def __init__(self):
        self.memory = Memory()  # 与memory系统配合
        self.feedback_store = []
    
    def record_usage(self, skill_name, context, result):
        """记录Skill使用情况"""
        self.memory.add({
            "skill": skill_name,
            "context": context,
            "result": result,
            "timestamp": now()
        })
    
    def analyze_performance(self):
        """分析Skill性能"""
        # 分析成功率
        # 分析失败原因
        # 生成优化建议
    
    def evolve(self):
        """进化Skill"""
        # 根据分析结果优化
        # 更新SKILL.md
        # 记录进化历史
```

### 3. Memory集成

**与memory系统配合：**

- **使用记录**：记录每次Skill调用的上下文和结果
- **效果追踪**：追踪Skill的效果变化
- **问题诊断**：诊断Skill使用中的问题
- **优化建议**：基于历史数据生成优化建议

## Skill模板

### 标准模板

```markdown
---
name: "<skill-name>"
description: "<功能描述>。当<触发条件>时调用。"
---

# <Skill标题>

## 何时调用

<触发条件说明>

## 功能说明

<详细功能描述>

## 使用方法

<使用步骤>

## 注意事项

<重要提示>

## 进化记录

<记录Skill的迭代历史>
```

### 进化记录模板

```markdown
## 进化记录

### v1.0 - 2026-03-21
- 初始版本
- 基础功能实现

### v1.1 - 2026-03-22
- 优化：根据使用反馈优化了XXX
- 新增：添加了YYY功能
- 修复：修复了ZZZ问题
```

## 构建流程

### 步骤1：需求收集

```
1. 与用户沟通，理解需求
2. 确定Skill的核心功能
3. 定义触发条件
4. 设计输出格式
```

### 步骤2：结构创建

```bash
# 创建目录
mkdir -p .trae/skills/<skill-name>

# 创建SKILL.md
touch .trae/skills/<skill-name>/SKILL.md
```

### 步骤3：内容编写

```
1. 编写frontmatter
2. 编写功能说明
3. 添加使用示例
4. 设计进化机制
```

### 步骤4：测试验证

```
1. 测试触发条件
2. 验证功能正确性
3. 检查输出格式
4. 记录初始版本
```

## 最佳实践

### 1. 描述清晰

- description必须包含功能和触发条件
- 保持简洁（< 200字符）
- 使用清晰的语言

### 2. 功能聚焦

- 每个Skill专注一个功能
- 避免功能过于复杂
- 易于理解和维护

### 3. 进化友好

- 设计进化机制
- 记录使用反馈
- 定期优化更新

### 4. Memory集成

- 与memory系统配合
- 记录使用历史
- 基于数据优化

## 示例

### 示例1：创建新Skill

用户："创建一个代码审查的skill"

操作：
1. 分析需求：代码审查功能
2. 创建目录：`.trae/skills/code-reviewer/`
3. 编写SKILL.md
4. 设计进化机制
5. 集成memory系统

### 示例2：优化现有Skill

用户："优化readme-generator skill"

操作：
1. 分析使用历史
2. 识别问题点
3. 设计优化方案
4. 更新SKILL.md
5. 记录进化历史

## 输出内容

此Skill将生成：
- `.trae/skills/<skill-name>/SKILL.md` - Skill定义文件
- 进化记录 - 记录Skill迭代历史
- 使用报告 - Skill使用情况分析

## 注意事项

- **不要设限**：优化方案可以包括任何改进
- **记录历史**：所有进化都要记录
- **数据驱动**：基于使用数据优化
- **持续迭代**：定期review和优化

## 权限说明

作为Skill构建器，我有权限：
- 创建新的Skills
- 修改现有Skills
- 设计进化机制
- 集成memory系统
- 重构Skill结构
