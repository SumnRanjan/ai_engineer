# Multi-Agent AI System (Without LangGraph)

A tool-using AI agent project built with **Python, Groq, and Tavily**. It demonstrates two approaches to building AI agents:

1. **Single Agent** — one LLM decides when to search the web or perform calculations.
2. **Multi-Agent System** — a manager LLM delegates research and calculation tasks to specialized helper agents.

The project uses Groq's chat completions API for LLM calls, Tavily for web search, and a restricted Python math environment for calculations. It also tracks token usage across LLM calls.

---

## Features

- **Groq LLM integration** using `openai/gpt-oss-120b`.
- **Web search** through the Tavily API.
- **Calculator tool** for arithmetic and supported mathematical functions.
- **Function/tool calling** so the LLM can choose which tool to invoke.
- **Single-agent workflow** with a maximum of five tool-call attempts.
- **Multi-agent workflow** with a manager and two specialist agents:
  - Search LLM — searches for facts and returns source URLs.
  - Maths LLM — performs calculations using the calculator tool.
- **Notes-based coordination** — helper results are written to `notes.md`, which the manager reads in later rounds.
- **Token tracking** grouped by agent label.

---

## Project Structure

```text
multiagent/
│
├── .env                 # API keys (do not commit this file)
├── .gitignore
├── pyproject.toml
├── uv.lock
│
├── tools.py             # Groq, Tavily, tools, and TokenTracker
├── single_agent.py      # Single-agent implementation
├── multi_agent.py       # Manager + specialist agents
│
└── notes.md             # Generated during a multi-agent run
```

Keep these Python files in the same directory so imports such as `from tools import ...` work.

---

## 1. Requirements

- Python 3.10 or later
- A [Groq API key](https://console.groq.com/keys)
- A [Tavily API key](https://app.tavily.com/)

This project uses [`uv`](https://docs.astral.sh/uv/) for Python dependency and environment management.

---

## 2. Setup with uv

Open a terminal in the project directory.

If this is a new project and you do not already have a `pyproject.toml`, initialize it:

```bash
uv init
```

Add the required packages:

```bash
uv add groq tavily-python python-dotenv
```

`json`, `pathlib`, `os`, and `math` are part of Python's standard library, so they do not need to be installed.

---

## 3. Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholder values with your actual API keys.

**Security:** Never hardcode API keys in Python files or commit `.env` to GitHub. Add this to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
notes.md
```

You can omit `notes.md` from `.gitignore` if you want to keep generated notes in version control.

---

## 4. How the Project Works

### A. Single-Agent Architecture

The single agent uses one LLM with access to two tools:

- `web_search(query)` — retrieves current information from the web using Tavily.
- `calculate(expression)` — evaluates a mathematical expression using the calculator.

The agent receives a question and decides whether to call one or both tools. Tool results are added to the conversation, allowing the LLM to use them when preparing its answer.

```text
                 User Question
                       |
                       v
                 Single LLM
                       |
              Decide which tool
                 to call
                 /       \
                v         v
          Web Search   Calculator
                \         /
                 v       v
              Tool Results
                    |
                    v
               Single LLM
                    |
                    v
               Final Answer
```

The agent allows up to five tool-call rounds. If it reaches the limit, it makes a final request without tools and includes the collected tool results.

**Run it:**

```bash
uv run python single_agent.py
```

### B. Multi-Agent Architecture

The multi-agent system uses a manager LLM and two specialized helper LLMs.

**Manager LLM**

- Receives the user's question.
- Reads the current contents of `notes.md`.
- Decides which helper should handle each task.
- Can call multiple independent helpers in the same round.
- Produces the final answer when the notes contain enough information.

**Search LLM**

- Receives a self-contained research task from the manager.
- Has access only to the `web_search` tool.
- Returns facts, numbers, and source URLs.

**Maths LLM**

- Receives a calculation task from the manager.
- Has access only to the `calculate` tool.
- Returns calculation steps and the final result.
- Does not search the web, so the manager must include the required numbers in its task.

```text
                       User Question
                              |
                              v
                         Manager LLM
                              |
                   Reads notes.md file
                              |
                  Decides which helper to call
                         /          \
                        v            v
                  Search LLM      Maths LLM
                      |               |
                  Tavily API      Calculator
                      |               |
                      v               v
                 Search result   Calculation result
                      \               /
                       \             /
                        v           v
                         notes.md
                             |
                             v
                         Manager LLM
                             |
                    Enough information?
                         /       \
                       No         Yes
                       |           |
                 Next round    Final Answer
```

The manager can run for a maximum of five rounds. Each helper result is written to `notes.md`, and the manager reads those notes again in the next round.

**Run it:**

```bash
uv run python multi_agent.py
```

---

## 5. Important Code Concepts

### Tool Calling

A tool is described to the LLM using a function schema. For example, the search tool accepts a `query` string:

```python
SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for current information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
}
```

The LLM does not execute Python functions directly. It returns a tool-call request. The application reads the function name and arguments, executes the matching Python function, and sends the result back to the LLM.

### Tool Execution

The `AVAILABLE_TOOLS` dictionary maps tool names to Python functions:

```python
AVAILABLE_TOOLS = {
    "web_search": web_search,
    "calculate": calculate,
}
```

The agent checks whether a requested tool is allowed before executing it.

### Specialized Agents

The helper agents reuse the `ask_llm()` function from `single_agent.py`, but receive different system prompts and different tool lists.

```python
def ask_search_llm(task, tracker):
    return ask_llm(
        task,
        tracker,
        SEARCH_PROMPT,
        [SEARCH_TOOL],
        label="search_llm"
    )
```

This is an example of specialization through **different instructions and tool access**, rather than using a different model for every agent.

### Notes File as Shared Memory

The manager does not directly receive the raw helper result as a tool response in its conversation. Instead, the application writes each helper's task and answer into `notes.md`.

```python
def write_note(round_no, helper, task, answer):
    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(
            f"## Round {round_no} — {helper}\n"
            f"**Task:** {task}\n\n"
            f"**Answer:**\n{answer}\n\n"
        )
```

The manager reads this file at the start of every round. This provides a simple form of persistent working memory during one run.

### Token Tracking

`TokenTracker` records usage for each LLM label:

- Number of calls
- Prompt tokens
- Completion tokens
- Total tokens

At the end of execution:

```python
tracker.report("multi agent")
```

This helps compare token usage between the single-agent and multi-agent approaches.

---

## 6. Example Questions

Try questions that require both research and calculations.

**Research + calculation:**

```text
Find the populations of India and Japan. Calculate the percentage
by which India's population is greater than Japan's.
```

**Research only:**

```text
What are the latest features announced for Python?
Include source URLs.
```

**Calculation only:**

```text
If a product costs 1250 and has a 18% discount, what is its final price?
```

The exact response depends on the model's tool-selection decisions and the information returned by the search provider.

---

## 7. Run Commands

Run these commands from the project directory:

```bash
# Run the single-agent system
uv run python single_agent.py

# Run the multi-agent system
uv run python multi_agent.py

# Add a dependency
uv add package-name

# List project dependencies
uv tree

# Sync the environment with the lock file
uv sync
```

---

## 8. Important Implementation Notes

- `tools.py`, `single_agent.py`, and `multi_agent.py` must be importable from the same project directory.
- `multi_agent.py` imports `ask_llm` from `single_agent.py`; this is intentional code reuse.
- The multi-agent manager's five-round limit is separate from each helper's five-attempt limit.
- A multi-agent run can therefore make more LLM calls than a single-agent run.
- Groq rate limits may apply. The Groq client is configured with retries, but retries do not guarantee that every request will succeed.
- The calculator uses Python `eval()` with restricted built-ins and a math-function allowlist. This is a learning-project safeguard, not a complete security sandbox. For production use, parse and validate expressions with a safer arithmetic parser.
- The current implementation assumes the model returns valid tool-call arguments. For production use, add handling for malformed JSON, unknown helper names, missing response content, and API failures.
- The notes file is reset at the start of each multi-agent run. It is not long-term memory.

---

## 9. What I Learned

By building this project, I practised:

- Connecting an LLM to external APIs using Groq.
- Understanding function calling and tool execution.
- Designing tool schemas with JSON parameters.
- Building a single-agent tool-calling loop.
- Creating specialized agents with different system prompts and tool permissions.
- Implementing manager-based task delegation.
- Sharing information between agents through a notes file.
- Managing conversation rounds and tool-call limits.
- Tracking prompt, completion, and total token usage.
- Managing Python dependencies and virtual environments using `uv`.

---

## 10. Future Improvements

- Add LangGraph to manage agent state and workflow transitions.
- Add structured output validation with Pydantic.
- Add better error handling and retry logic.
- Add conversation history and configurable memory.
- Add parallel execution for independent helper tasks.
- Add logging and tracing for every agent and tool call.
- Compare single-agent and multi-agent token usage, latency, and answer quality.

---

## License

This project is intended for learning and experimentation. Add a license file if you plan to distribute or publish it.
