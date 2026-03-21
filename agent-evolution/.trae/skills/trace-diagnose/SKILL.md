---
name: "trace-diagnose"
description: "诊断Agent的评测trace用例。当用户提到分析trace文件、诊断Agent表现、查看评测用例时调用。"
---

# Trace诊断器

这个Skill用于诊断Agent的评测trace用例。

## 何时调用

在以下情况下调用此Skill：
- 用户要求"分析trace文件"
- 用户要求"诊断Agent表现"
- 用户要求"查看评测用例"
- 用户提到trace相关分析

## 核心功能

### 1. Trace文件诊断

**从eval_script_zjq/cases/下读取trace文件：**

```python
import json
import os
from pathlib import Path

def load_trace_files(trace_dir="eval_script_zjq/cases/"):
    """加载所有trace文件"""
    trace_files = []
    trace_path = Path(trace_dir)
    
    for file in trace_path.glob("*.json"):
        with open(file, 'r') as f:
            trace_data = json.load(f)
            trace_files.append({
                "file_name": file.name,
                "data": trace_data
            })
    
    return trace_files
```

### 2. 逐条诊断

**诊断回答质量和响应速度：**

```python
def diagnose_trace(trace_data):
    """诊断单个trace"""
    diagnosis = {
        "trace_id": trace_data.get("trace_id"),
        "quality_score": 0,
        "speed_score": 0,
        "issues": [],
        "suggestions": []
    }
    
    # 诊断回答质量
    quality_issues = diagnose_quality(trace_data)
    diagnosis["quality_score"] = calculate_quality_score(quality_issues)
    diagnosis["issues"].extend(quality_issues)
    
    # 诊断响应速度
    speed_issues = diagnose_speed(trace_data)
    diagnosis["speed_score"] = calculate_speed_score(speed_issues)
    diagnosis["issues"].extend(speed_issues)
    
    # 生成优化建议
    diagnosis["suggestions"] = generate_suggestions(diagnosis["issues"])
    
    return diagnosis
```

### 3. 质量诊断

**诊断回答质量：**

```python
def diagnose_quality(trace_data):
    """诊断回答质量"""
    issues = []
    
    # 检查回答完整性
    if not trace_data.get("answer"):
        issues.append({
            "type": "quality",
            "severity": "high",
            "description": "回答为空",
            "suggestion": "检查Agent是否正常处理请求"
        })
    
    # 检查回答相关性
    if not is_relevant(trace_data.get("query"), trace_data.get("answer")):
        issues.append({
            "type": "quality",
            "severity": "medium",
            "description": "回答与问题不相关",
            "suggestion": "优化prompt或检索策略"
        })
    
    # 检查回答准确性
    if not is_accurate(trace_data.get("answer"), trace_data.get("expected")):
        issues.append({
            "type": "quality",
            "severity": "high",
            "description": "回答不准确",
            "suggestion": "改进知识库或推理逻辑"
        })
    
    return issues
```

### 4. 速度诊断

**诊断响应速度：**

```python
def diagnose_speed(trace_data):
    """诊断响应速度"""
    issues = []
    
    total_time = trace_data.get("total_time", 0)
    
    # 检查总响应时间
    if total_time > 5.0:
        issues.append({
            "type": "speed",
            "severity": "high",
            "description": f"响应时间过长: {total_time}s",
            "suggestion": "优化性能瓶颈"
        })
    
    # 检查各步骤耗时
    for step in trace_data.get("steps", []):
        step_time = step.get("duration", 0)
        if step_time > 2.0:
            issues.append({
                "type": "speed",
                "severity": "medium",
                "description": f"步骤 {step.get('name')} 耗时过长: {step_time}s",
                "suggestion": "优化该步骤性能"
            })
    
    return issues
```

### 5. 诊断报告

**生成结构化分析报告：**

```markdown
# Trace诊断报告

## 基本信息
- 诊断时间：2026-03-21
- Trace文件数：50
- 诊断用例数：50

## 诊断概览
- 平均质量得分：8.5/10
- 平均速度得分：7.8/10
- 问题总数：15
- 严重问题：3
- 一般问题：12

## 质量诊断

### 问题分布
| 问题类型 | 数量 | 严重程度 |
|---------|------|----------|
| 回答为空 | 2 | 高 |
| 回答不相关 | 5 | 中 |
| 回答不准确 | 3 | 高 |

### 典型问题
1. **问题1**：回答为空
   - 影响用例：TC003, TC007
   - 原因：Agent未正常处理请求
   - 建议：检查Agent逻辑

2. **问题2**：回答不相关
   - 影响用例：TC015, TC023, TC031
   - 原因：检索策略不合理
   - 建议：优化检索算法

## 速度诊断

### 性能分析
- 平均响应时间：1.2s
- 最大响应时间：3.5s
- 最慢步骤：LLM调用（0.8s）

### 性能问题
1. **问题1**：响应时间过长
   - 影响用例：TC012, TC045
   - 原因：LLM调用耗时过长
   - 建议：优化prompt或切换模型

2. **问题2**：步骤耗时过长
   - 影响步骤：检索步骤
   - 原因：检索算法效率低
   - 建议：优化检索性能

## 优化建议

### 质量优化
1. 改进检索策略
2. 优化prompt设计
3. 完善知识库
4. 增强推理逻辑

### 性能优化
1. 优化LLM调用
2. 改进检索算法
3. 添加缓存机制
4. 并行处理请求

## 结论
Agent整体表现良好，但需要优化部分用例的质量和性能。
```

## 诊断流程

### 步骤1：加载Trace

```
1. 读取trace文件
   - 从指定目录加载
   - 解析JSON格式
   - 验证数据完整性

2. 提取关键信息
   - 查询内容
   - 回答内容
   - 响应时间
   - 步骤信息
```

### 步骤2：质量诊断

```
1. 完整性检查
   - 回答是否为空
   - 信息是否完整
   - 格式是否正确

2. 相关性检查
   - 回答是否相关
   - 是否答非所问
   - 是否偏离主题

3. 准确性检查
   - 回答是否准确
   - 是否有错误
   - 是否符合预期
```

### 步骤3：速度诊断

```
1. 总体性能
   - 总响应时间
   - 是否超时
   - 是否符合要求

2. 步骤性能
   - 各步骤耗时
   - 性能瓶颈
   - 优化空间

3. 资源消耗
   - CPU使用
   - 内存使用
   - 网络消耗
```

### 步骤4：生成报告

```
1. 汇总数据
   - 统计问题数量
   - 计算得分
   - 分类问题

2. 分析问题
   - 识别共性问题
   - 分析根本原因
   - 评估影响范围

3. 提出建议
   - 质量优化建议
   - 性能优化建议
   - 架构优化建议
```

## 诊断指标

### 质量指标
- **完整性**：回答是否完整
- **相关性**：回答是否相关
- **准确性**：回答是否准确
- **可读性**：回答是否易读

### 速度指标
- **响应时间**：总响应时间
- **步骤时间**：各步骤耗时
- **资源消耗**：CPU、内存使用

### 综合指标
- **质量得分**：0-10分
- **速度得分**：0-10分
- **综合得分**：加权平均

## 最佳实践

### 1. 全面诊断
- 质量和速度并重
- 覆盖所有用例
- 深入分析问题

### 2. 数据驱动
- 基于实际数据
- 统计分析方法
- 量化评估指标

### 3. 问题追踪
- 记录所有问题
- 分类管理问题
- 追踪修复状态

### 4. 持续优化
- 定期诊断
- 对比历史数据
- 追踪优化效果

## 输出内容

此Skill将生成：
- **诊断报告**：完整的诊断结果
- **问题列表**：发现的问题清单
- **优化建议**：改进建议
- **统计数据**：诊断统计数据

## 注意事项

- **客观公正**：基于事实诊断
- **详细记录**：记录所有细节
- **深入分析**：分析根本原因
- **可操作**：提供可操作建议

## 权限说明

作为Trace诊断器，我有权限：
- 读取trace文件
- 分析trace数据
- 生成诊断报告
- 提出优化建议
- 记录问题状态
