---
name: "eval-runner"
description: "对Agent服务执行评测。当用户提到跑评测用例、发测试请求、生成trace、批量测试、评估Agent服务时调用。"
---

# 评测运行器

这个Skill用于对Agent服务执行评测。

## 何时调用

在以下情况下调用此Skill：
- 用户要求"跑评测用例"
- 用户要求"发测试请求"
- 用户要求"生成trace"
- 用户要求"批量测试"
- 用户要求"评估Agent服务"

## 核心功能

### 1. 评测流程

**完整评测流程：**

```
步骤1：准备评测
├── 加载评测用例
├── 配置评测参数
├── 检查服务状态
└── 初始化环境

步骤2：执行评测
├── 发送请求
├── 收集响应
├── 记录trace
└── 保存日志

步骤3：分析结果
├── 解析trace
├── 评估质量
├── 生成报告
└── 提出建议
```

### 2. 请求发送

**发送测试请求：**

```python
import requests
import json
import time

def send_request(service_url, test_case):
    """发送测试请求"""
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{service_url}/api/chat",
            json=test_case,
            timeout=30
        )
        
        end_time = time.time()
        
        return {
            "status_code": response.status_code,
            "response": response.json(),
            "latency": end_time - start_time,
            "success": response.status_code == 200
        }
    except Exception as e:
        return {
            "status_code": None,
            "response": None,
            "latency": None,
            "success": False,
            "error": str(e)
        }
```

### 3. Trace收集

**收集trace日志：**

```python
def collect_trace(service_url, session_id):
    """收集trace日志"""
    try:
        response = requests.get(
            f"{service_url}/api/trace/{session_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            trace_data = response.json()
            
            # 保存trace文件
            trace_file = f"traces/{session_id}.json"
            with open(trace_file, 'w') as f:
                json.dump(trace_data, f, indent=2)
            
            return trace_data
        else:
            return None
    except Exception as e:
        print(f"收集trace失败: {e}")
        return None
```

### 4. Trace分析

**分析trace文档：**

```python
def analyze_trace(trace_data):
    """分析trace数据"""
    analysis = {
        "session_id": trace_data.get("session_id"),
        "total_time": 0,
        "steps": [],
        "issues": []
    }
    
    # 分析每个步骤
    for step in trace_data.get("steps", []):
        step_info = {
            "name": step.get("name"),
            "duration": step.get("duration"),
            "status": step.get("status"),
            "input": step.get("input"),
            "output": step.get("output")
        }
        
        analysis["steps"].append(step_info)
        analysis["total_time"] += step.get("duration", 0)
        
        # 检测问题
        if step.get("status") == "error":
            analysis["issues"].append({
                "step": step.get("name"),
                "error": step.get("error"),
                "severity": "high"
            })
    
    return analysis
```

### 5. 评测报告

**生成评测报告：**

```markdown
# 评测报告

## 基本信息
- 评测时间：2026-03-21
- 服务地址：http://localhost:8000
- 用例数量：100

## 评测概览
- 成功率：95%
- 平均响应时间：1.2s
- 最大响应时间：3.5s
- 最小响应时间：0.8s

## 详细结果

### 成功用例
| Case ID | 输入 | 响应时间 | 输出质量 |
|---------|------|----------|----------|
| TC001 | ... | 1.1s | 优秀 |
| TC002 | ... | 1.3s | 良好 |

### 失败用例
| Case ID | 输入 | 错误信息 | 原因分析 |
|---------|------|----------|----------|
| TC003 | ... | Timeout | 响应超时 |

## Trace分析

### 性能分析
- 总耗时：120s
- 平均步骤数：5
- 最慢步骤：LLM调用（0.8s）

### 问题分析
1. **问题1**：响应超时
   - 影响用例：TC003, TC007
   - 原因：LLM调用时间过长
   - 建议：优化prompt或切换模型

2. **问题2**：输出质量不佳
   - 影响用例：TC015, TC023
   - 原因：prompt设计不合理
   - 建议：优化prompt模板

## 优化建议
1. 优化LLM调用性能
2. 改进prompt设计
3. 添加超时重试机制
4. 优化响应格式

## 结论
服务整体表现良好，但需要优化性能和部分用例的输出质量。
```

## 评测流程

### 步骤1：准备阶段

```
1. 加载评测用例
   - 从文件加载
   - 或动态生成
   - 验证格式

2. 配置评测参数
   - 服务地址
   - 超时时间
   - 并发数

3. 检查服务状态
   - 健康检查
   - 版本确认
   - 配置验证
```

### 步骤2：执行阶段

```
1. 发送请求
   - 批量发送
   - 记录时间
   - 收集响应

2. 收集trace
   - 获取trace日志
   - 保存trace文件
   - 解析trace数据

3. 记录日志
   - 请求日志
   - 响应日志
   - 错误日志
```

### 步骤3：分析阶段

```
1. 解析trace
   - 提取关键信息
   - 分析性能
   - 识别问题

2. 评估质量
   - 准确性评估
   - 完整性评估
   - 相关性评估

3. 生成报告
   - 汇总数据
   - 分析问题
   - 提出建议
```

## 评测用例格式

### 标准用例格式

```json
{
  "case_id": "TC001",
  "input": {
    "query": "用户问题",
    "context": "上下文信息"
  },
  "expected_output": {
    "answer": "预期答案",
    "confidence": 0.9
  },
  "metadata": {
    "category": "分类",
    "difficulty": "难度",
    "priority": "优先级"
  }
}
```

### 批量用例格式

```json
{
  "test_suite": "评测套件名称",
  "version": "1.0",
  "cases": [
    {
      "case_id": "TC001",
      "input": {...},
      "expected_output": {...}
    },
    {
      "case_id": "TC002",
      "input": {...},
      "expected_output": {...}
    }
  ]
}
```

## 评测指标

### 性能指标
- **响应时间**：从请求到响应的时间
- **吞吐量**：单位时间处理的请求数
- **并发数**：同时处理的请求数

### 质量指标
- **准确率**：正确回答的比例
- **完整率**：回答完整的比例
- **相关率**：回答相关的比例

### 稳定性指标
- **成功率**：请求成功的比例
- **错误率**：请求失败的比例
- **超时率**：请求超时的比例

## 最佳实践

### 1. 用例设计
- 覆盖多种场景
- 包含边界条件
- 考虑异常情况

### 2. 性能优化
- 并发执行
- 异步处理
- 结果缓存

### 3. 结果分析
- 详细记录
- 分类统计
- 趋势分析

### 4. 问题追踪
- 记录问题
- 分类管理
- 追踪修复

## 输出内容

此Skill将生成：
- **评测报告**：完整的评测结果
- **Trace文件**：详细的trace日志
- **问题列表**：发现的问题清单
- **优化建议**：改进建议

## 注意事项

- **服务可用**：确保服务正常运行
- **用例合理**：设计合理的测试用例
- **结果准确**：准确记录评测结果
- **分析深入**：深入分析问题原因

## 权限说明

作为评测运行器，我有权限：
- 发送测试请求
- 收集trace日志
- 分析评测结果
- 生成评测报告
- 提出优化建议
