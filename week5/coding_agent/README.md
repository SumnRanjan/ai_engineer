# Week 5: Mini Coding Agent

A small AI agent that fixes simple bugs in C++ code. You describe the bug in plain English; the LLM uses tools to find the bug, edits the line, and the agent compiles and runs the code to check the fix.

No LangGraph or framework: just a plain Python loop, so the agent mechanics are easy to see.

---

## 1. How it works

```
You ──bug──► main.py ──"which tool?"──► LLM (Groq)
                ▲                           │
                │        "call replace_line(...)"
                │                           ▼
                └────── result ◄──── tools.py ──► edits cpp_code/main.cpp
```

1. You describe the bug in simple English.
2. The LLM calls tools to find the file, read the code and replace the wrong line.
3. The agent compiles and runs the code with **g++** and shows the output.
4. Compile fails → next attempt (compiler errors are sent back to the LLM).
   Compile passes → you say whether the bug is fixed.
5. Not fixed in **3 attempts** → "cannot solve" and all files are **restored** to the original.

---

## 2. Project structure

```
coding_agent/
├── main.py        # the brain: LLM loop, attempts, compile + verify
├── tools.py       # the hands: tool schemas + tool functions
├── .env           # GROQ_API_KEY=...
└── cpp_code/
    └── main.cpp   # buggy C++ program to fix
```

### Why two Python files?

| File | Role | Contains |
|---|---|---|
| `main.py` | **Brain**: decides the flow | Groq client, system prompt, tool-calling loop, retries, g++ verify, restore on failure |
| `tools.py` | **Hands**: what the agent can do | `TOOLS` (schemas the LLM reads), `code_files()`, `make_tools()` |

Keeping them separate means you add a new tool by editing only `tools.py`, and the same tools can be reused with another loop (e.g. LangGraph) or exposed as an **MCP server**.

---

## 3. The tools

| Tool | What it does | Example |
|---|---|---|
| `search_files(keyword)` | Finds files whose name or content contains the keyword, with match counts. Empty keyword lists all files. | `search_files("total")` |
| `search_in_file(path, keyword)` | Shows matching lines **with line numbers**. Empty keyword shows the whole file. | `search_in_file("main.cpp", "for")` |
| `replace_line(path, line_number, new_line)` | Replaces one whole line; keeps the original indentation; returns before/after. | `replace_line("main.cpp", 6, "for (size_t i = 0; ...")` |

**Safety built in:**
- The LLM can only touch files **inside the workspace** (paths like `../` are blocked).
- Tool errors (wrong path, bad line number) are returned as text, so the LLM can correct itself.
- Files are snapshotted before the run and restored if the agent fails.

---

## 4. Setup (Windows + uv)

```powershell
uv venv
.venv\Scripts\activate
uv add groq python-dotenv
```

Create `.env`:
```
GROQ_API_KEY=your_key_here
```

Install **g++** (MinGW / MSYS2) so the agent can compile. If g++ is missing, the agent skips compiling and asks you to check manually.

---

## 5. Run

```powershell
uv run main.py                  # works on the default folder
uv run main.py some/other/dir   # work on another folder
```

Expected start:
```
============================================================
MINI CODING AGENT
============================================================
Workspace: ...\coding_agent\cpp_code
Files    : main.cpp

Describe the bug in simple English:
```

---

## 6. Test bugs in `cpp_code/main.cpp`

Buggy output:
```
Total   : 240
Average : 60
Highest : 65
```

| # | Bug to type | Root cause | Correct fix |
|---|---|---|---|
| 1 | `The total is wrong. It prints 240 but 70+85+90+65 should be 310.` | Loop starts at index 1 | `for (size_t i = 0; i < v.size(); i++) {` |
| 2 | `Highest prints 65 but it should be 90, the biggest mark.` | Uses `<` instead of `>` | `if (x > best) best = x;` |
| 3 | `Average prints a whole number. It should be 77.5.` | Integer division | `return (double)total(v) / v.size();` |

Correct output after all fixes:
```
Total   : 310
Average : 77.5
Highest : 90
```

---

## 7. Key settings (in `main.py`)

| Setting | Value | Meaning |
|---|---|---|
| `MODEL` | `openai/gpt-oss-120b` | Groq model used |
| `MAX_ATTEMPTS` | 3 | Fix attempts before giving up |
| `MAX_STEPS` | 10 | Tool calls allowed per attempt |
| `max_retries` | 10 | Groq SDK auto-retries on free-tier rate limits |

---

## 8. Agent concepts used

- **Tool calling:** the LLM returns a structured tool call; Python runs it and sends the result back.
- **Agent loop:** repeat "LLM → tool → result" until the LLM replies without a tool call.
- **Feedback from the environment:** compiler errors and program output go back to the LLM.
- **Human-in-the-loop:** the user confirms whether the bug is really fixed.
- **Guardrails:** step and attempt limits, workspace-only file access, restore on failure.

---

## 9. Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `Files : (none)` | C++ files not in the workspace folder | Put `main.cpp` inside `cpp_code/` (check for `.cpp.txt` names) |
| `ModuleNotFoundError: groq` / `dotenv` | Packages installed in the wrong Python | `uv add groq python-dotenv`, run with `uv run` |
| `g++ not found` | Compiler not installed or not on PATH | Install MinGW/MSYS2 and add its `bin` to PATH |
| `Groq rejected a malformed tool call` | Model produced a bad tool call | Handled automatically: the agent asks again |
| Rate limit errors | Groq free tier | SDK waits and retries (`max_retries=10`) |

---

## 10. Ideas to extend

- Add a `run_tests` tool so the agent checks expected output itself (no human y/n).
- Add `insert_line` / `delete_line` for fixes that need more than one-line changes.
- Show a diff of all changes at the end.
- Expose `tools.py` as an **MCP server** so Claude Desktop or any MCP client can use these tools.
- Rebuild the loop in **LangGraph** (nodes: plan → act → verify).