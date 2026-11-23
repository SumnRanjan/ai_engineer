# Week 5: MCP (Model Context Protocol)

---

## 1. What is MCP?

**MCP (Model Context Protocol)** is an open standard (introduced by Anthropic, Nov 2024) that lets LLM apps and agents connect to external tools, data and systems in one consistent way.

> **One-liner:** MCP is like **USB-C for AI**: build a tool integration once, and any MCP-compatible app or agent can use it.

### The problem it solves

| Without MCP | With MCP |
|---|---|
| Every AI app writes a custom integration for every tool | Each tool exposes **one** MCP server; each app implements **one** MCP client |
| 10 apps × 20 tools = **200** integrations (M×N) | 10 + 20 = **30** integrations (M+N) |

---

## 2. Architecture

```
┌──────────────────────── HOST (AI app: Claude Desktop, IDE, your agent) ──┐
│                                                                          │
│   LLM  ◄──►  MCP Client 1  ──────►  MCP Server A  (GitHub)               │
│              MCP Client 2  ──────►  MCP Server B  (Database)             │
│              MCP Client 3  ──────►  MCP Server C  (Our order server)     │
└──────────────────────────────────────────────────────────────────────────┘
```

| Component | Role |
|---|---|
| **Host** | The AI app the user interacts with (Claude Desktop, Cursor, your own agent) |
| **Client** | Lives inside the host; keeps a **1:1** connection with one server |
| **Server** | Lightweight program wrapping a tool/data source and exposing it via MCP |
| **Transport** | `stdio` (local process) or Streamable HTTP (remote). Messages use **JSON-RPC 2.0** |

---

## 3. The three primitives a server exposes

| Primitive | Controlled by | What it is | Example in this repo |
|---|---|---|---|
| **Tools** | **Model** decides when to call | Actions / functions | `add`, `get_order_status` |
| **Resources** | **App** decides what to load | Read-only data / context | `orders://{order_id}` |
| **Prompts** | **User** picks them | Reusable prompt templates | `summarize_order` |

---

## 4. How a request flows

```
1. Client connects  ──►  initialize (handshake, exchange capabilities)
2. Client asks      ──►  tools/list, resources/list, prompts/list
3. Tool schemas are given to the LLM
4. LLM decides      ──►  "call get_order_status(order_id='4521')"
5. Client sends     ──►  tools/call  ──►  Server runs the function
6. Server returns result ──►  added to LLM context ──►  LLM writes final answer
```

---

## 5. MCP vs Function Calling

| | Function calling | MCP |
|---|---|---|
| **What** | The model's ability to output a structured tool call | A protocol for discovering and running tools across apps |
| **Scope** | Defined per app, per model provider | Standard, reusable across any MCP host |
| **Relationship** | Building block | Built **on top of** function calling, doesn't replace it |

---

## 6. Project structure

```
mcp/
├── server.py    # MCP server: tools, resource, prompt (fake restaurant orders)
├── client.py    # MCP client: connects over stdio, discovers & calls everything
└── README.md
```

---

## 7. Setup & run (Windows + uv)

```powershell
cd mcp
uv venv
.venv\Scripts\activate
uv pip install "mcp[cli]"      # use uv pip, NOT plain pip, inside a uv venv
python client.py
```

**Expected output:**
```
Tools: ['add', 'get_order_status']
Prompts: ['summarize_order']
add(2, 3) = 5
Order 4521: Pizza is delivered (Rs 450)
Resource: {'item': 'Burger', 'status': 'preparing', 'amount': 250}
Prompt: Look up order 4521 and write a friendly 2-line status update for the customer.
```

> The client starts `server.py` itself as a subprocess (stdio transport), so you **don't** run the server separately.

---

## 8. Code walkthrough

### server.py

```python
from mcp.server.mcpserver import MCPServer   # mcp 2.x (was FastMCP in 1.x)

mcp = MCPServer("demo-server")

@mcp.tool()                                  # Tool: model-controlled
def get_order_status(order_id: str) -> str:
    """Get the status of a restaurant order by its ID."""   # docstring = tool description for the LLM
    ...

@mcp.resource("orders://{order_id}")         # Resource: app-controlled data
def order_resource(order_id: str) -> str: ...

@mcp.prompt()                                # Prompt: user-selected template
def summarize_order(order_id: str) -> str: ...

mcp.run()                                    # stdio transport by default
```

Key points:
- **Type hints → input schema.** `order_id: str` becomes the JSON schema the LLM sees.
- **Docstring → tool description.** Write it clearly; the LLM uses it to decide when to call the tool.

### client.py

```python
server_params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()                          # handshake
        tools = await session.list_tools()                  # discovery
        result = await session.call_tool("add", {"a": 2, "b": 3})
        res = await session.read_resource("orders://4522")
        prompt = await session.get_prompt("summarize_order", {"order_id": "4521"})
```

- `sys.executable` means the server runs with the **same Python/venv** as the client.
- In a real agent, the **LLM** picks which tool to call; here we call them manually to see the mechanics.

---

## 9. Use the server in Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "demo": {
      "command": "C:\\Users\\ASUS\\ai_engi\\week5\\mcp_demo\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\ASUS\\ai_engi\\week5\\mcp_demo\\server.py"]
    }
  }
}
```

Restart Claude Desktop, then ask: *"What's the status of order 4521?"*

---

## 10. Troubleshooting (errors I hit)

| Error | Cause | Fix |
|---|---|---|
| `can't open file '...\week5\client.py'` | Running from the wrong folder | `cd` into the folder that contains `client.py` |
| `No module named 'mcp'` | `uv venv` has no pip, so `pip install` went to **system** Python | Use `uv pip install "mcp[cli]"` inside the venv |
| `No module named 'mcp.server.fastmcp'` | mcp **2.x** renamed `FastMCP` → `MCPServer` | `from mcp.server.mcpserver import MCPServer` (or pin `"mcp<2"` for v1 code) |
| Weird import errors | Project folder named `mcp` shadows the library | Rename folder (e.g. `mcp_demo`) |

---

## 11. Security notes (interview points)

- **Prompt injection via tool outputs:** treat server responses as untrusted data.
- **Least privilege:** give servers only the permissions they need (e.g. read-only DB user).
- **Untrusted third-party servers:** review code before installing; they run on your machine.
- **Auth for remote servers:** use OAuth; never hard-code secrets.
- **Human-in-the-loop** for destructive actions (delete, pay, send).

---

## 12. Interview quick answers

- **What is MCP?** An open protocol standardizing how LLM apps connect to tools and data, turning M×N integrations into M+N.
- **Host vs client vs server?** Host = AI app; client = connector inside the host (1:1 per server); server = wraps a tool/data source.
- **Tools vs resources vs prompts?** Model-controlled actions vs app-controlled data vs user-selected templates.
- **Transports?** stdio for local, Streamable HTTP for remote; JSON-RPC 2.0 messages.
- **MCP vs function calling?** Function calling is the model capability; MCP is the interoperable protocol built on it.