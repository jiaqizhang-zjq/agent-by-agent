---
name: "agent-optimize"
description: "对Agent执行具体优化。当用户提到优化Agent、改Prompt、改代码、改配置、修复问题、提升质量、提升速度时调用。"
---

# Agent优化器

这个Skill用于对Agent执行具体优化。

## 何时调用

在以下情况下调用此Skill：
- 用户要求"优化Agent"
- 用户要求"改Prompt"
- 用户要求"改代码"
- 用户要求"改配置"
- 用户要求"修复问题"
- 用户要求"提升质量"
- 用户要求"提升速度"

## 核心功能

### 1. 优化方案设计

**根据issue-tracker中的问题和方案，设计具体优化方案：**

**注意：我有很高的权限，可以采用任何优化手段，不要给自己设限！**

#### Agent编排优化
```python
# 优化Agent编排
class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self.routing_strategy = "dynamic"
    
    def optimize_routing(self):
        """优化路由策略"""
        # 根据问题类型动态路由
        # 添加负载均衡
        # 优化并发处理
        pass
    
    def add_agent(self, agent_type, agent_instance):
        """添加新Agent"""
        self.agents[agent_type] = agent_instance
    
    def remove_agent(self, agent_type):
        """移除Agent"""
        if agent_type in self.agents:
            del self.agents[agent_type]
```

#### 模型切换优化
```python
# 切换LLM模型
class ModelSwitcher:
    def __init__(self):
        self.models = {
            "fast": "gpt-3.5-turbo",
            "quality": "gpt-4",
            "balanced": "gpt-3.5-turbo-16k"
        }
        self.current_model = "balanced"
    
    def switch_model(self, model_type):
        """切换模型"""
        if model_type in self.models:
            self.current_model = model_type
            return True
        return False
    
    def get_model_for_task(self, task_type):
        """根据任务类型选择模型"""
        if task_type == "simple":
            return self.models["fast"]
        elif task_type == "complex":
            return self.models["quality"]
        else:
            return self.models["balanced"]
```

#### Prompt优化
```python
# 优化Prompt模板
class PromptOptimizer:
    def __init__(self):
        self.templates = {}
    
    def optimize_prompt(self, prompt_type, feedback):
        """根据反馈优化Prompt"""
        current_prompt = self.templates.get(prompt_type)
        
        # 分析反馈
        issues = analyze_feedback(feedback)
        
        # 生成优化后的Prompt
        optimized_prompt = self._generate_optimized_prompt(
            current_prompt, 
            issues
        )
        
        # 更新模板
        self.templates[prompt_type] = optimized_prompt
        
        return optimized_prompt
    
    def _generate_optimized_prompt(self, prompt, issues):
        """生成优化后的Prompt"""
        # 根据问题类型优化
        # 添加约束条件
        # 改进指令清晰度
        pass
```

#### Skill/MCP整合优化
```python
# 整合Skills和MCP工具
class IntegrationOptimizer:
    def __init__(self):
        self.skills = {}
        self.mcp_tools = {}
    
    def integrate_skill(self, skill_name, skill_instance):
        """整合Skill"""
        self.skills[skill_name] = skill_instance
    
    def integrate_mcp_tool(self, tool_name, tool_instance):
        """整合MCP工具"""
        self.mcp_tools[tool_name] = tool_instance
    
    def optimize_integration(self):
        """优化整合策略"""
        # 分析使用频率
        # 优化调用顺序
        # 添加缓存机制
        pass
```

### 2. 代码修改

**落地代码修改：**

```python
# 示例：优化检索性能
def optimize_retrieval(query, knowledge_base):
    """优化检索性能"""
    # 原代码
    # results = knowledge_base.search(query)
    
    # 优化后代码
    # 1. 添加查询预处理
    processed_query = preprocess_query(query)
    
    # 2. 使用向量检索
    results = knowledge_base.vector_search(processed_query)
    
    # 3. 添加结果缓存
    cache_key = generate_cache_key(processed_query)
    cache.set(cache_key, results, ttl=3600)
    
    return results
```

### 3. Prompt重写

**重写Prompt模板：**

```markdown
# 原Prompt
你是一个智能助手，请回答用户的问题。

# 优化后Prompt
你是一个专业的智能助手，具备以下能力：
1. 准确理解用户问题
2. 提供相关且准确的回答
3. 保持回答简洁明了

回答要求：
- 准确性：确保回答准确无误
- 相关性：回答必须与问题相关
- 完整性：回答应该完整全面
- 简洁性：避免冗余信息

请根据用户的问题，提供高质量的回答。
```

### 4. 配置调整

**调整配置参数：**

```yaml
# 原配置
llm:
  model: gpt-3.5-turbo
  temperature: 0.7
  max_tokens: 1000

# 优化后配置
llm:
  model: gpt-4  # 切换到更强大的模型
  temperature: 0.3  # 降低温度提高准确性
  max_tokens: 2000  # 增加最大token数
  
retrieval:
  top_k: 10  # 增加检索数量
  threshold: 0.8  # 提高相似度阈值
  
cache:
  enabled: true  # 启用缓存
  ttl: 3600  # 缓存1小时
```

### 5. 架构优化

**优化系统架构：**

```
原架构：
用户请求 → Agent → LLM → 返回结果

优化后架构：
用户请求 
  ↓
负载均衡器
  ↓
Agent集群（多个Agent实例）
  ↓
模型路由器（根据任务选择模型）
  ↓
LLM集群（多个模型实例）
  ↓
结果聚合器
  ↓
返回结果
```

## 优化流程

### 步骤1：问题分析

```
1. 读取issue-tracker中的问题
   - 问题类型
   - 影响范围
   - 优先级

2. 分析根本原因
   - 代码问题
   - 配置问题
   - 架构问题

3. 确定优化目标
   - 性能目标
   - 质量目标
   - 稳定性目标
```

### 步骤2：方案设计

```
1. 设计优化方案
   - Agent编排优化
   - 模型切换
   - Prompt重写
   - Skill/MCP整合
   - 代码重构
   - 配置调整
   - 架构优化

2. 评估方案
   - 可行性评估
   - 成本评估
   - 风险评估

3. 选择最佳方案
   - 综合评估
   - 权衡取舍
```

### 步骤3：实施优化

```
1. 代码修改
   - 编写代码
   - 代码审查
   - 单元测试

2. 配置调整
   - 修改配置
   - 验证配置
   - 备份配置

3. 架构调整
   - 设计架构
   - 实施部署
   - 验证效果
```

### 步骤4：验证效果

```
1. 功能验证
   - 运行测试用例
   - 验证功能正确性
   - 检查副作用

2. 性能验证
   - 性能测试
   - 对比优化前后
   - 确认提升效果

3. 质量验证
   - 质量评估
   - 用户反馈
   - 持续监控
```

## 优化类型

### 1. 性能优化

**目标：提升响应速度**

- **代码优化**：优化算法、减少计算量
- **缓存优化**：添加缓存、减少重复计算
- **并发优化**：并行处理、异步执行
- **资源优化**：资源池化、连接复用

### 2. 质量优化

**目标：提升回答质量**

- **Prompt优化**：改进prompt模板、添加约束
- **模型优化**：切换模型、调整参数
- **检索优化**：改进检索算法、提高准确率
- **推理优化**：增强推理逻辑、添加验证

### 3. 稳定性优化

**目标：提升系统稳定性**

- **异常处理**：完善异常处理、添加重试
- **容错机制**：添加降级、熔断机制
- **监控告警**：完善监控、及时告警
- **日志优化**：完善日志、便于排查

### 4. 易用性优化

**目标：提升用户体验**

- **交互优化**：改进交互流程、简化操作
- **提示优化**：改进提示信息、提高友好度
- **文档优化**：完善文档、降低学习成本
- **错误提示**：改进错误提示、便于理解

## 优化记录

### 优化记录模板

```markdown
# 优化记录

## 优化ID：OPT-001

### 基本信息
- 优化时间：2026-03-21
- 优化类型：性能优化
- 优化目标：提升响应速度
- 相关问题：ISSUE-001

### 优化方案
1. 添加缓存机制
2. 优化检索算法
3. 并行处理请求

### 实施内容
1. **代码修改**
   - 文件：retrieval.py
   - 修改：添加缓存装饰器
   - 行数：+15 -3

2. **配置调整**
   - 文件：config.yaml
   - 修改：启用缓存、设置TTL

3. **架构调整**
   - 添加：缓存层
   - 调整：请求处理流程

### 优化效果
- 响应时间：从1.5s降到0.8s（提升46.7%）
- 成功率：从95%提升到98%
- 用户满意度：提升15%

### 验证结果
- 功能验证：✅ 通过
- 性能验证：✅ 通过
- 稳定性验证：✅ 通过

### 备注
优化效果显著，建议推广到其他模块。
```

## 最佳实践

### 1. 数据驱动
- 基于数据分析
- 量化优化效果
- 对比优化前后

### 2. 小步快跑
- 分阶段优化
- 快速验证效果
- 及时调整方案

### 3. 风险控制
- 评估优化风险
- 准备回滚方案
- 逐步发布

### 4. 持续监控
- 监控优化效果
- 收集用户反馈
- 持续改进

## 输出内容

此Skill将生成：
- **优化方案**：详细的优化方案
- **代码修改**：具体的代码修改
- **配置调整**：配置参数调整
- **优化报告**：优化效果报告

## 注意事项

- **不要设限**：可以采用任何优化手段
- **数据驱动**：基于数据做决策
- **风险控制**：评估风险、准备回滚
- **效果验证**：验证优化效果

## 权限说明

作为Agent优化器，我有权限：
- 修改代码
- 调整配置
- 重写Prompt
- 切换模型
- 调整架构
- 整合Skills/MCP
- 重构系统

**记住：我有很高的权限，可以采用任何优化手段，不要给自己设限！**
