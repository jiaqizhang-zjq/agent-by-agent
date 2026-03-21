# LangGraph Graph API 文档

> 来源: https://docs.langchain.com/oss/python/langgraph/graph-api.md
> 获取时间: 2026-03-21

## 文档索引

获取完整文档索引: https://docs.langchain.com/llms.txt

---

# Graph API 概述

## Graphs（图）

LangGraph 的核心是将 Agent 工作流建模为图。使用三个关键组件定义 Agent 的行为：

### 1. State（状态）
一个共享数据结构，表示应用程序的当前快照。可以是任何数据类型，但通常使用共享状态模式定义。

### 2. Nodes（节点）
编码 Agent 逻辑的函数。它们接收当前状态作为输入，执行某些计算或副作用，并返回更新后的状态。

### 3. Edges（边）
根据当前状态确定下一个要执行的 `Node` 的函数。可以是条件分支或固定转换。

通过组合 `Nodes` 和 `Edges`，可以创建复杂的、循环的工作流，随时间演进状态。真正的威力来自 LangGraph 如何管理该状态。

**强调**: `Nodes` 和 `Edges` 只是函数——它们可以包含 LLM 或只是普通代码。

**简而言之**: 节点做工作，边告诉下一步做什么。

### 消息传递机制

LangGraph 的底层图算法使用[消息传递](https://en.wikipedia.org/wiki/Message_passing)来定义通用程序。当节点完成操作时，它沿着一条或多条边向其他节点发送消息。这些接收节点然后执行其函数，将结果消息传递给下一组节点，过程继续。受 Google 的 [Pregel](https://research.google/pubs/pregel-a-system-for-large-scale-graph-processing/) 系统启发，程序以离散的"超步"进行。

**超步（Super-step）** 可以被视为图节点的单次迭代。并行运行的节点属于同一超步，而顺序运行的节点属于不同的超步。在图执行开始时，所有节点都处于 `inactive` 状态。当节点在其任何传入边（或"通道"）上接收到新消息（状态）时，它变为 `active`。然后活动节点运行其函数并响应更新。在每个超步结束时，没有传入消息的节点通过将自己标记为 `inactive` 来投票 `halt`。当所有节点都处于 `inactive` 且没有消息在传输时，图执行终止。

---

## StateGraph

[`StateGraph`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph) 类是主要的图类。它由用户定义的 `State` 对象参数化。

---

## 编译图

构建图时，首先定义[状态](#state)，然后添加[节点](#nodes)和[边](#edges)，最后编译它。

**编译是什么，为什么需要？**

编译是一个相当简单的步骤。它对图的结构提供一些基本检查（没有孤立节点等）。也是可以指定运行时参数如[检查点](/oss/python/langgraph/persistence)和断点的地方。

通过调用 `.compile` 方法编译图：

```python
graph = graph_builder.compile(...)
```

> **警告**: 在使用图之前**必须**编译它。

---

## State（状态）

定义图时首先要做的是定义图的 `State`。`State` 由[图的模式](#schema)以及指定如何将更新应用于状态的[`reducer` 函数](#reducers)组成。`State` 的模式将是图中所有 `Nodes` 和 `Edges` 的输入模式，可以是 `TypedDict` 或 `Pydantic` 模型。所有 `Nodes` 都会发出对 `State` 的更新，然后使用指定的 `reducer` 函数应用这些更新。

### Schema（模式）

指定图模式的主要文档化方式是使用 [`TypedDict`](https://docs.python.org/3/library/typing.html#typing.TypedDict)。如果想在状态中提供默认值，请使用 [`dataclass`](https://docs.python.org/3/library/dataclasses.html)。如果需要递归数据验证，我们也支持使用 Pydantic [`BaseModel`](/oss/python/langgraph/use-graph-api#use-pydantic-models-for-graph-state) 作为图状态（但请注意 Pydantic 的性能不如 `TypedDict` 或 `dataclass`）。

默认情况下，图将具有相同的输入和输出模式。如果要更改此设置，也可以直接指定显式输入和输出模式。当有很多键，一些显式用于输入而另一些用于输出时，这很有用。

> **注意**: `langchain` 中的更高级 [`create_agent`](/oss/python/langchain/agents) 工厂不支持 Pydantic 状态模式。

#### 多模式

通常，所有图节点使用单一模式进行通信。这意味着它们将读写相同的状态通道。但在某些情况下，我们需要更多控制：

- **输入模式**: 只包含用户输入相关的字段
- **输出模式**: 只包含用户应该看到的输出字段
- **内部模式**: 包含所有内部状态字段

```python
from typing import TypedDict

class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    graph_output: str

class OverallState(TypedDict):
    user_input: str
    graph_output: str
    internal_state: str
```

### Reducers（归约器）

Reducers 定义了如何将更新应用于状态。默认情况下，更新将直接覆盖状态值。但有时我们想要更复杂的行为：

```python
from typing import Annotated, TypedDict
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

**内置 Reducers**:
- `add_messages`: 合并消息列表
- 自定义 reducer 函数

---

## Nodes（节点）

节点是执行工作的函数。它们接收当前状态并返回更新：

```python
def my_node(state: State) -> State:
    # 执行一些工作
    return {"key": "new_value"}
```

### 节点类型

1. **普通节点**: 执行计算并返回状态更新
2. **工具节点**: 调用外部工具
3. **LLM 节点**: 调用语言模型

---

## Edges（边）

边确定控制流：

### 1. 普通边
固定从一个节点到另一个节点：

```python
graph.add_edge("node_a", "node_b")
```

### 2. 条件边
根据状态动态路由：

```python
def route_function(state: State) -> str:
    if state["condition"]:
        return "node_b"
    return "node_c"

graph.add_conditional_edges("node_a", route_function)
```

### 3. 入口点
图的起始点：

```python
graph.set_entry_point("start_node")
```

### 4. 条件入口点

```python
graph.set_conditional_entry_points(entry_function)
```

---

## 完整示例

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages

# 定义状态
class State(TypedDict):
    messages: Annotated[list, add_messages]
    context: str

# 定义节点
def process_input(state: State) -> State:
    return {"context": "processed"}

def generate_response(state: State) -> State:
    return {"messages": [{"role": "assistant", "content": "response"}]}

# 构建图
graph_builder = StateGraph(State)
graph_builder.add_node("process", process_input)
graph_builder.add_node("generate", generate_response)

# 添加边
graph_builder.set_entry_point("process")
graph_builder.add_edge("process", "generate")
graph_builder.set_finish_point("generate")

# 编译图
graph = graph_builder.compile()

# 运行
result = graph.invoke({"messages": [], "context": ""})
```

---

## 关键概念总结

| 概念 | 说明 |
|------|------|
| **State** | 共享数据结构，表示应用状态 |
| **Nodes** | 函数，执行工作并更新状态 |
| **Edges** | 函数，确定下一个节点 |
| **StateGraph** | 主要图类 |
| **compile()** | 编译图，必须步骤 |
| **Reducers** | 定义如何应用状态更新 |
| **Super-step** | 图的单次迭代 |

---

## 相关链接

- [LangGraph 官方文档](https://docs.langchain.com/oss/python/langgraph/)
- [API 参考](https://reference.langchain.com/python/langgraph/)
- [示例代码](https://github.com/langchain-ai/langgraph/tree/main/examples)
