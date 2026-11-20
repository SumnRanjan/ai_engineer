# LangGraph Basics: Number Doubling Graph

A beginner-friendly LangGraph example. It keeps **doubling a number until it reaches 100 or more**, then finishes.

---

## What is LangGraph? (in one line)

> **LangGraph lets you build a program as a flowchart: boxes (nodes) connected by arrows (edges), sharing one notebook (state).**

| Concept | Simple meaning | In this project |
|---|---|---|
| **State** | A shared notebook every step can read and write | `{"number": int}` |
| **Node** | A box, i.e. one step of work (a Python function) | `double`, `finish` |
| **Edge** | An arrow, i.e. which step runs next | `double → double`, `double → finish`, `finish → END` |
| **Conditional edge** | An arrow with a question ("if this, go here, else go there") | `decision()` |

---

## Flowchart

```
START → double → number < 100?
          ↑         ├── yes → double (loop again)
          └─────────┘
                    └── no  → finish → END
```

---

## Setup

```bash
# 1. (Optional) create and activate a virtual environment
uv venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 2. Install LangGraph
uv add langgraph              # or: pip install langgraph

# 3. Run
python main.py
```

---

## Full code

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END


class State(TypedDict):
    number: int


def double(state: State) -> dict:
    newnum = state["number"] * 2
    print("in double")
    print(newnum)
    return {"number": newnum}


def finish(state: State) -> dict:
    print("in finish")
    print(state["number"])
    return {"number": state["number"]}


def decision(state: State) -> str:
    if state["number"] < 100:
        return "double"
    return "finish"


builder = StateGraph(State)
builder.add_node("double", double)
builder.add_node("finish", finish)

builder.set_entry_point("double")

builder.add_conditional_edges(
    "double",
    decision,
    {"double": "double", "finish": "finish"},
)

builder.add_edge("finish", END)

graph = builder.compile()
result = graph.invoke({"number": 5})
print("Final result:", result)
```

---

## Explanation, block by block

### 1. Imports

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
```

- **`TypedDict`** (built into Python) lets us describe what a dictionary should look like, with which keys and which types.
- **`StateGraph`** is the LangGraph class used to build the flowchart.
- **`END`** is a special built-in node that means "stop here, the graph is finished".

---

### 2. State (the shared notebook)

```python
class State(TypedDict):
    number: int
```

- This defines the **data that flows through the graph**.
- Here the state has just one key, `number`, which is an integer.
- Every node **receives** this state and can **return updates** to it.
- Example state while running: `{"number": 20}`.

---

### 3. Node 1: `double`

```python
def double(state: State) -> dict:
    newnum = state["number"] * 2
    print("in double")
    print(newnum)
    return {"number": newnum}
```

| Line | Meaning |
|---|---|
| `def double(state: State) -> dict:` | A normal Python function. It receives the current state and returns a dictionary. |
| `newnum = state["number"] * 2` | Reads the number from the state and multiplies it by 2. |
| `print(...)` | Shows which node is running and the new value, which helps with learning and debugging. |
| `return {"number": newnum}` | **Updates the state.** LangGraph merges this into the notebook, so `number` now holds the new value. |

> 💡 A node **does not change the state directly**. It **returns** what should change, and LangGraph applies it.

---

### 4. Node 2: `finish`

```python
def finish(state: State) -> dict:
    print("in finish")
    print(state["number"])
    return {"number": state["number"]}
```

- The last step. It prints the final number.
- It returns the same number, so nothing changes. (You could also just `return {}`.)

---

### 5. The decision function (the router)

```python
def decision(state: State) -> str:
    if state["number"] < 100:
        return "double"
    return "finish"
```

- This is **not a node**. It is a **router**: it only decides **where to go next**.
- It returns a **string** label:
  - `"double"` if the number is still less than 100, so the graph loops again
  - `"finish"` if the number is 100 or more, so the graph moves on
- It must **not** change the state. It only reads it.

---

### 6. Create the graph builder

```python
builder = StateGraph(State)
```

- Creates an **empty flowchart** that will use `State` as its shared notebook.
- Think of `builder` as a blank page where we'll draw boxes and arrows.

---

### 7. Add nodes (draw the boxes)

```python
builder.add_node("double", double)
builder.add_node("finish", finish)
```

- `add_node(name, function)` puts a box on the flowchart.
- The first argument (`"double"`) is the **box's name**, used when drawing arrows.
- The second argument (`double`) is the **Python function** that runs inside the box.
- The name and the function don't have to match, but keeping them the same is easier.

---

### 8. Entry point (where to start)

```python
builder.set_entry_point("double")
```

- Tells LangGraph that the **first box to run is `"double"`**.
- Same as `builder.add_edge(START, "double")` (`START` is imported from `langgraph.graph`).

---

### 9. Conditional edge (an arrow with a question)

```python
builder.add_conditional_edges(
    "double",
    decision,
    {"double": "double", "finish": "finish"},
)
```

| Argument | Meaning |
|---|---|
| `"double"` | **From** this node. After `double` runs, check the condition. |
| `decision` | The **router function** to call. It returns `"double"` or `"finish"`. |
| `{"double": "double", "finish": "finish"}` | A **map**: `router's answer → node to go to`. |

So, after every `double`:
- `decision` returns `"double"` → go to the `double` node again (a **loop**)
- `decision` returns `"finish"` → go to the `finish` node

> ⚠️ The method name is **`add_conditional_edges`**, plural. `add_conditional_edge` gives an error.

---

### 10. Normal edge to END

```python
builder.add_edge("finish", END)
```

- `add_edge(a, b)` is an arrow that **always** goes from `a` to `b`.
- After `finish`, go to `END`, so the graph stops.
- Without this, LangGraph doesn't know what happens after `finish`.

---

### 11. Compile (turn the drawing into a program)

```python
graph = builder.compile()
```

- Checks the flowchart for mistakes, such as a missing node or a dead end.
- Returns a **runnable graph**. You can't run `builder` directly, only the compiled `graph`.

---

### 12. Run the graph

```python
result = graph.invoke({"number": 5})
print("Final result:", result)
```

- **`invoke(...)`** starts the graph with an **initial state**, here `number = 5`.
- LangGraph runs the nodes in order, following the arrows, until it reaches `END`.
- **`result`** is the **final state**, e.g. `{'number': 160}`.

---

## Step-by-step run (start = 5)

| Step | Node | Number before | Number after | Decision |
|---|---|---|---|---|
| 1 | double | 5 | 10 | 10 < 100 → double |
| 2 | double | 10 | 20 | 20 < 100 → double |
| 3 | double | 20 | 40 | 40 < 100 → double |
| 4 | double | 40 | 80 | 80 < 100 → double |
| 5 | double | 80 | 160 | 160 ≥ 100 → finish |
| 6 | finish | 160 | 160 | → END |

### Output

```
in double
10
in double
20
in double
40
in double
80
in double
160
in finish
160
Final result: {'number': 160}
```

---

## Key functions cheat sheet

| Function | What it does |
|---|---|
| `StateGraph(State)` | Creates a graph that uses `State` as shared data |
| `add_node(name, func)` | Adds a step (box) |
| `set_entry_point(name)` | Sets the first node to run |
| `add_edge(a, b)` | Always go from `a` to `b` |
| `add_conditional_edges(src, router, map)` | After `src`, call `router` and go where `map` says |
| `END` | Special node meaning "stop" |
| `compile()` | Builds a runnable graph |
| `invoke(state)` | Runs the graph with a starting state |

---

## Common mistakes

| Mistake | Fix |
|---|---|
| `add_conditional_edge` | Use **`add_conditional_edges`** (plural) |
| Missing quote in the map, e.g. `"double":"double,` | Write `"double": "double",` |
| No `add_edge("finish", END)` | The graph needs an exit |
| Calling `builder.invoke()` | Call `compile()` first, then `graph.invoke()` |
| Starting with `0` | `0 × 2 = 0` loops forever and hits LangGraph's **recursion limit** (default 25 steps) |

### Change the recursion limit

```python
graph.invoke({"number": 1}, {"recursion_limit": 50})
```

---

## Visualise the graph (optional)

```python
print(graph.get_graph().draw_mermaid())
```

Paste the output into [mermaid.live](https://mermaid.live) to see the flowchart.

---

## How this connects to AI agents

This toy example has the **same shape** as a real AI agent:

| This project | AI agent |
|---|---|
| `double` node | **LLM** node (the AI thinks) |
| `decision` router | "Did the LLM ask for a tool?" |
| Loop back to `double` | Run the tool, then go back to the LLM |
| `finish` → `END` | Return the final answer |

---

## Next steps

1. Replace `double` with an **LLM call** (e.g. `ChatGroq`)
2. Add **tools** with `ToolNode` and `tools_condition`
3. Add **memory** with a checkpointer (`MemorySaver`)