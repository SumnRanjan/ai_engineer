# Restaurant Order Management Agent (LangGraph)

An AI agent that takes a food order, checks the menu, cooks and serves the order, and handles failures with retry limits. It is built with **LangGraph** and uses a **Groq LLM** to understand the customer and write friendly replies.

```
user_input -> llm -> order_confirm -> llm -> cook -> llm -> serve -> llm -> END
```

---

## 1. Big picture

The **`llm` node is the brain**. Every other node does one job, writes a `status` into the state and goes back to the `llm`. The `llm` reads the state (status + retry counters), talks to the customer and decides **which node runs next**.

| Node | Job | Writes `status` |
|---|---|---|
| `user_input` | Reads what the customer types | (adds a message) |
| `llm` | Understands the message, talks to the customer, decides the next step | `placed`, `cook`, `serve`, `awaiting_user`, `done`, `failed` |
| `order_confirm` | Checks the dish and quantity against the `MENU` | `confirmed`, `partial`, `unavailable` |
| `cook` | Cooks the dish (60% success) | `ready`, `cook_failed` |
| `serve` | Serves the dish (60% success) | `complete`, `serve_failed` |

```
                ┌──────────────┐
      START ──► │  user_input  │ ◄─────────────── awaiting_user
                └──────┬───────┘                       │
                       ▼                               │
                ┌──────────────┐ ── placed ──► order_confirm ──┐
                │     llm      │ ── cook   ──► cook ───────────┤
                │   (brain)    │ ── serve  ──► serve ──────────┤
                └──────┬───────┘ ◄─────────────────────────────┘
                       │ done / failed
                       ▼
                      END
```

---

## 2. Setup

```bash
uv add langgraph langchain-groq python-dotenv
```

Create a `.env` file:

```
GROQ_API_KEY=your_key_here
```

Run:

```bash
python restaurant_agent.py
```

---

## 3. Configuration

```python
MODEL = "openai/gpt-oss-120b"

MENU = {"pizza": 5, "burger": 3, "biryani": 10, "dosa": 2, "pasta": 0}

ORDER_RETRIES = 3        # order attempts
COOK_RETRIES = 2         # re-cooks allowed
SERVE_RETRIES = 2        # re-serves allowed
COOK_SUCCESS_PROB = 0.6  # 60% success, 40% fail
SERVE_SUCCESS_PROB = 0.6
```

- **`MENU`** maps each dish to the quantity in stock. `pasta: 0` means it is on the menu but sold out.
- **`sys.stdout.reconfigure(encoding="utf-8")`** stops the Windows console from crashing on the fancy quotes the model sometimes writes.

### `find_menu_item(name)`: fuzzy menu matching

It finds the right menu item even if the customer types it a bit differently:

| Customer types | Matched to | How |
|---|---|---|
| `pizza` | `pizza` | Exact match |
| `margherita pizza` | `pizza` | The menu word is inside the text |
| `piza`, `burgr` | `pizza`, `burger` | Closest spelling (`difflib`) |
| `noodles` | `None` | Nothing close, so not available |

---

## 4. State (the shared notebook)

```python
class OrderDetails(TypedDict):
    dish_name: str
    required_quantity: int
    available_quantity: int      # written by order_confirm (0 if not on menu)

class State(TypedDict):
    messages: Annotated[list, add_messages]   # chat history (user + AI)
    order: OrderDetails
    status: Status
    order_retries: int     # 3
    cook_retries: int      # 2
    serve_retries: int     # 2
    final_result: str      # "COMPLETED" or "NOT COMPLETED: <reason>"
```

| Field | Meaning |
|---|---|
| `messages` | Full conversation. `add_messages` **appends** new messages instead of replacing the list. |
| `order` | What the customer wants, plus how much is available |
| `status` | The current step's result, and the routing signal |
| `*_retries` | How many attempts are left; `0` means used up |
| `final_result` | Outcome shown at the end |

### Status values

`Status` is a `Literal`, so only these exact words are allowed.

| Written by the nodes (a report) | Written by the llm (a decision) | Goes to |
|---|---|---|
| `new` (start) | `awaiting_user` | `user_input` |
| `confirmed` / `partial` / `unavailable` | `placed` | `order_confirm` |
| `ready` / `cook_failed` | `cook` | `cook` |
| `complete` / `serve_failed` | `serve` | `serve` |
| | `done` / `failed` | `END` |

---

## 5. LLM helpers

### `OrderIntent`: what the LLM extracts

```python
class OrderIntent(BaseModel):
    intent: Literal["new_order", "accept_partial", "unrelated"]
    dish_name: Optional[str]
    quantity: Optional[int]
```

| Intent | Example message |
|---|---|
| `new_order` | "2 pizzas please" → dish `pizza`, quantity `2` |
| `accept_partial` | "ok, go ahead with what you have" |
| `unrelated` | "what is the capital of France?" |

### `extract_order(state)`

- Sends the latest user message, the menu, and whether a partial order was just offered to the LLM.
- `with_structured_output(OrderIntent)` makes the LLM return **clean structured data** (an `OrderIntent` object) instead of free text.

### `say(instruction, state)`

- Asks the LLM to write **1–2 friendly sentences** to the customer.
- The code decides **what** to say, for example "apologise, cook failed", and the LLM decides **how** to say it nicely.

---

## 6. Nodes explained

### `user_input`

```python
read = config.get("configurable", {}).get("input_fn", input)
text = read("\nYou: ")
return {"messages": [HumanMessage(text)]}
```

- Normally uses Python's `input()`.
- Tests can pass a fake `input_fn` through `config`, so scripted answers replace typing.

### `llm_node` (the brain)

Reads `status` and decides:

| Status it reads | What it does | Next |
|---|---|---|
| `new` / `awaiting_user` + **new order** | Saves dish + quantity | `placed` → order_confirm |
| `awaiting_user` + **accept partial** | Sets quantity = available | `cook` |
| `new` / `awaiting_user` + **unrelated** | "I'm a food-ordering agent only", **order retry −1** | `awaiting_user`, or `failed` if 0 |
| `confirmed` | "Order confirmed, sending to kitchen" | `cook` |
| `partial` | Offers the smaller quantity, **order retry −1** | `awaiting_user`, or `failed` if 0 |
| `unavailable` | "Not available, order something else", **order retry −1** | `awaiting_user`, or `failed` if 0 |
| `ready` | "Food is ready" | `serve` |
| `cook_failed` | If cook retries > 0: **cook retry −1**, cook again. Otherwise apologise. | `cook` / `failed` |
| `complete` | "Order complete, enjoy!" | `done` |
| `serve_failed` | If serve > 0 **and** cook > 0: **both −1**, re-cook. Otherwise apologise. | `cook` / `failed` |

### `order_confirm`

1. Fuzzy-matches the dish to the menu.
2. Writes `available_quantity` (0 if not found).
3. Sets the status:
   - `available == 0` → `unavailable`
   - `available < required` → `partial`
   - otherwise → `confirmed`

### `cook` and `serve`

```python
if _outcome(config, "cook_outcomes", COOK_SUCCESS_PROB):
    return {"status": "ready"}
return {"status": "cook_failed"}
```

- `_outcome()` is a 60/40 coin flip: `random.random() < 0.6` means success.
- Tests can **script** the results: `cook_outcomes=[False, True]` means fail first, then succeed.
- These nodes **don't** retry by themselves. They report back, and the **llm decides** whether to retry.

---

## 7. Edges

```python
builder.add_edge(START, "user_input")
builder.add_edge("user_input", "llm")
builder.add_edge("order_confirm", "llm")
builder.add_edge("cook", "llm")
builder.add_edge("serve", "llm")

builder.add_conditional_edges("llm", route_after_llm, {...})
```

- **Normal edges:** every worker node always goes back to `llm`.
- **Conditional edge:** after `llm`, `route_after_llm` reads `status`:

| `status` | Goes to |
|---|---|
| `awaiting_user` | `user_input` |
| `placed` | `order_confirm` |
| `cook` | `cook` |
| `serve` | `serve` |
| `done` / `failed` | `END` |

---

## 8. Retry rules

| Counter | Starts | Goes down by 1 when | At 0 |
|---|---|---|---|
| `order_retries` | 3 | Unrelated message, **partial** order, unavailable dish | END: "no valid order / order attempts exhausted" |
| `cook_retries` | 2 | Every **re-cook** (after a cook failure **or** a serve failure) | END: apology |
| `serve_retries` | 2 | Every **re-serve** after a serve failure | END: apology |

- The **first** cook and serve are free. Only retries cost a counter.
- A serve failure needs a **re-cook first**, so it costs **1 cook retry and 1 serve retry**.

---

## 9. Running the agent

### `run(config)`

```python
for final in graph.stream(initial_state(), config=config, stream_mode="values"):
```

- `graph.stream(..., stream_mode="values")` gives the **full state after every step**, so new AI messages are printed **as they happen**.
- `recursion_limit: 100` allows enough steps for all the retries. The default limit of 25 can be too low.

### `simulate(...)`: scripted tests (no typing)

```python
simulate(
    user_inputs=["2 pizzas"],
    cook_outcomes=[False, True, True],
    serve_outcomes=[False, True],
)
```

- `user_inputs`: what the "customer" types, in order. When the list runs out it sends `"bye"`.
- `cook_outcomes` / `serve_outcomes`: forced success or failure for each attempt.
- The LLM still runs, so a Groq API key is needed.

---

## 10. Test scenarios

```python
# TC1: unrelated → partial → unavailable → END (order retries)
simulate(["what is the capital of France?", "5 burgers", "no, give me 2 pasta"])

# TC2: cook fail → cook ok → serve fail → re-cook ok → serve ok → COMPLETED
simulate(["2 pizzas"], cook_outcomes=[False, True, True], serve_outcomes=[False, True])

# TC3: partial → new full order → cook fail → ok → serve fail → re-cook ok → serve fail → FAIL
simulate(["5 burgers", "no, 2 pizzas instead"],
         cook_outcomes=[False, True, True], serve_outcomes=[False, False])
```

| Test | Counter trace | Final result |
|---|---|---|
| TC1 | order 3→2 (unrelated) → 1 (partial) → 0 (pasta unavailable) | NOT COMPLETED: order attempts exhausted |
| TC2 | cook 2→1 (cook fail) → serve fail: cook 1→0, serve 2→1 | COMPLETED |
| TC3 | order 3→2 (partial); cook 2→1; serve fail: cook 1→0, serve 2→1; serve fails again with cook = 0 | NOT COMPLETED: serve failed and cook retries exhausted |

---

## 11. Known behaviours / limitations

- **A partial offer costs an order attempt** when it is offered. If it happens on the last attempt, the customer can't accept it, because the session ends first.
- **"No" without a new dish** counts as `unrelated`, so it costs another attempt. In tests, reject and re-order in **one** message (e.g. "no, 2 pizzas instead").
- **Stock doesn't go down** after an order is served.
- **One dish per order.** Multi-dish orders are not supported yet.
- `gpt-oss-120b` sometimes makes invalid tool calls with structured output. If you see `tool_use_failed`, try `llama-3.3-70b-versatile`.

---

## 12. Key concepts used

| Concept | Where |
|---|---|
| `TypedDict` state | `State`, `OrderDetails` |
| `Annotated[list, add_messages]` | `messages` appends instead of overwriting |
| `Literal` | `Status`, `OrderIntent.intent`: only fixed values allowed |
| Pydantic + structured output | `OrderIntent` + `with_structured_output` |
| Hub-and-spoke graph | `llm` is the hub, the other nodes are the spokes |
| Conditional edges | `route_after_llm` |
| `RunnableConfig` | Injects test input and outcomes without changing the code |
| `graph.stream` | Live output step by step |