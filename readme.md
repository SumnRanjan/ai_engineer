# 🚀 AI Engineering – My Learning Journey

Welcome to my **AI Engineering Learning Journey**! This repository documents my progress as I learn AI Engineering through hands-on practice, concepts, experiments, and real-world projects.

My goal is to understand how modern AI applications work and become capable of building, deploying, and evaluating production-ready AI systems.

---

## 📊 Progress at a Glance

| Area | Status |
|---|---|
| LLM Fundamentals & Prompt Engineering | ✅ Completed |
| RAG & Vector Databases | ✅ Completed |
| AI Agents & LangGraph | ✅ Completed |
| Multi-Agent Systems | ✅ Completed |
| AI Agent Evaluation | ✅ Completed |
| MCP (Model Context Protocol) | ✅ Completed |
| Coding Agent | ✅ Completed |
| Evaluation, Observability & Guardrails | ✅ Completed |
| Deployment & Production | ✅ Completed |

---

## 🎯 Learning Goals

- Understand Large Language Models (LLMs) and how they work.
- Build applications using LLM APIs.
- Learn prompt engineering and structured outputs.
- Build AI agents and multi-agent systems.
- Understand Retrieval-Augmented Generation (RAG).
- Work with embeddings and vector databases.
- Learn LangChain and LangGraph.
- Build and connect tools using MCP.
- Evaluate, monitor, and deploy AI applications.
- Develop practical AI engineering projects.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM APIs | Groq (`openai/gpt-oss-120b`), OpenAI-compatible APIs |
| LLM Concepts | Tokens, Context Windows, Embeddings, Tool Calling |
| Data Validation | Pydantic, JSON |
| Prompt Engineering | Prompt Design, Prompt Chaining, ReAct |
| AI Frameworks | LangChain, LangGraph |
| Vector Databases | Qdrant |
| AI Architecture | RAG, AI Agents, Multi-Agent Systems |
| Tool Integration | MCP (Python SDK 2.x) |
| Evaluation | Golden datasets, Output & Trajectory evaluation |
| Code Verification | g++ (compile + run inside the coding agent) |
| Development Tools | VS Code, Git, GitHub, uv |
| Deployment | Python application deployment |

---

## 📚 Learning Roadmap

This roadmap follows the topics covered in the AI Engineering playlist.

### LLM Fundamentals and Prompt Engineering

- [x] Introduction to AI Engineering
- [x] Python environment and project setup
- [x] Understanding your first LLM API call
- [x] System, User, and Assistant roles
- [x] Temperature and response generation
- [x] Tokens and tokenization
- [x] Pydantic and structured JSON responses
- [x] First AI mini project
- [x] Prompt Engineering
- [x] Introduction to ReAct and AI Agents
- [x] Prompt Chaining
- [x] Streaming responses
- [x] Personal Portfolio AI mini project

### RAG and Vector Databases

- [x] Introduction to RAG (Retrieval-Augmented Generation)
- [x] Understanding Embeddings
- [x] Build your first RAG system
- [x] Introduction to Qdrant Vector Database
- [x] Multi-Tenant RAG with Qdrant
- [x] Convert a DSA playlist into a RAG application
- [x] Chunking strategies for RAG
- [x] RAG Evaluation

### AI Agents and LangGraph

- [x] Understanding why LLMs struggle with basic mathematics
- [x] Build your first AI Agent
- [x] Introduction to LangGraph
- [x] LangGraph implementation (State, Nodes, Edges)
- [x] Design a Restaurant AI Agent
- [x] Build an AI Agent using LangGraph
- [x] Introduction to Multi-Agent Systems
- [x] Build a Multi-Agent AI System (supervisor + workers)
- [x] AI Agent Evaluation

### MCP and Advanced AI Engineering

- [x] Understanding Model Context Protocol (MCP)
- [x] Build an MCP Server
- [x] Connect an MCP Server to Claude
- [x] Design a Coding Agent
- [x] Build a Coding Agent
- [x] AI Engineering interview preparation
- [x] AI concepts revision
- [x] Evaluation, Observability, and Guardrails

### Deployment and Production

- [x] Understanding AI application deployment
- [x] Deploy an AI application
- [x] Review production considerations
- [x] Build and refine end-to-end AI projects

---

## 🏗️ Projects

| Project | Description | Technologies | Folder | Status |
|---|---|---|---|---|
| First LLM Application | Make an LLM API call from Python | Python, Groq | `week1/` | ✅ |
| AI Mini Project | Build an application using LLMs | Python, LLM API | `week1/` | ✅ |
| Personal Portfolio AI | AI chat assistant on my portfolio that answers recruiter questions about my skills | Python, LLM API | `week2/ai-portfolio/` | ✅ |
| RAG Application | Question-answering system over documents | Python, Embeddings, Qdrant | `week2/` | ✅ |
| LangGraph Basics | Doubling graph with state, nodes, edges and conditional edges | LangGraph | `week3/` | ✅ |
| Restaurant AI Agent | LLM handles each step: take order, confirm, cook, serve | LangGraph | `week4/restraunt-ai-agent/` | ✅ |
| Multi-Agent System | Multiple LLM agents (supervisor + workers) collaborating | Python, LangGraph | `week5/multiagent/` | ✅ |
| MCP Server + Client | Order-lookup MCP server exposing tools, resources and prompts, with a Python client | Python, MCP | `week5/mcp/` | ✅ |
| Mini Coding Agent | LLM + tools agent that finds and fixes C++ bugs, verifies with g++, retries and rolls back on failure | Python, Groq, Tool Calling | `week5/coding_agent/` | ✅ |
| Deployed AI App | Deploy an end-to-end AI application | Python, Deployment | – | ✅ |

---

## 🔍 Project Highlights

### 🤖 Mini Coding Agent (`week5/coding_agent/`)
- Describe a bug in plain English; the agent finds the file, reads the code and edits the line using **3 tools**: `search_files`, `search_in_file`, `replace_line`.
- Verifies each fix by **compiling and running** the code with g++.
- Feeds compiler errors and user feedback back to the LLM, with up to **3 attempts**, and **restores files** if it fails.
- Guardrails: step limits, workspace-only file access, run timeout.

### 🔌 MCP Server (`week5/mcp/`)
- MCP server exposing all three primitives: **Tools** (`add`, `get_order_status`), **Resource** (`orders://{id}`), **Prompt** (`summarize_order`).
- Python client that connects over stdio, discovers capabilities and calls them.

### 🧑‍🤝‍🧑 Multi-Agent System (`week5/multiagent/`)
- Supervisor agent routes tasks to specialised worker agents in LangGraph.

---

## 📂 Repository Structure

```text
ai_engineer/
│
├── week1/                   # LLM fundamentals & prompt engineering
│   ├── day1/ … day5/
│
├── week2/                   # RAG, embeddings, Qdrant
│   ├── ai-portfolio/
│   ├── day1/ … day4/
│
├── week3/                   # AI agents & LangGraph
│   ├── day1/ … day6/
│
├── week4/                   # Agents & restaurant agent
│   ├── agents/
│   ├── day1/
│   ├── day2/
│   └── restraunt-ai-agent/
│
├── week5/                   # Multi-agent, MCP, coding agent
│   ├── coding_agent/
│   ├── mcp/
│   └── multiagent/
│
├── .env                     # local only, never committed
├── .gitignore
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SumnRanjan/ai_engineer.git
cd ai_engineer
```

### 2. Create and activate a virtual environment

```bash
uv venv --python 3.14
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
uv pip install groq python-dotenv
```

> Use `uv pip install` (not plain `pip`) inside a uv venv. A uv venv has no pip of its own, so plain `pip` installs into the system Python instead.

Project-specific dependencies (e.g. `langgraph`, `qdrant-client`, `"mcp[cli]"`) are installed per project.

### 4. Configure environment variables

Create a `.env` file in the repo root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Make sure `.env` is listed in `.gitignore`. Never commit API keys.

### 5. Run a project

```bash
cd week5/coding_agent
uv run main.py
```

---

## 🧠 Key Learnings

- **Agents = LLM + tools + loop.** The LLM picks a tool, code runs it, and the result goes back to the LLM until it's done.
- **Tool descriptions matter.** The LLM chooses tools purely from their name, description and parameter schema.
- **Evaluate both output and trajectory.** A correct answer can hide a bad process.
- **MCP turns M×N integrations into M+N.** Build a tool server once, use it from any MCP client.
- **Agentic search vs RAG.** Keyword tools work well for small codebases; semantic (vector) search helps when the query wording doesn't match the code.
- **Environment feedback improves agents.** Compiler errors and test output make the agent self-correct.

---

## 🔮 Next Steps

- Connect the MCP server to Claude Desktop.
- Add a `run_tests` tool and a semantic-search (RAG) tool to the coding agent.
- Build a golden dataset and evaluate the coding agent (fix rate, tokens per bug).
- Add observability (tracing) and guardrails.
- Deploy an end-to-end AI application.

---

## 📖 Learning Resources

- **YouTube Course:** [AI Engineer in 8 Weeks – Padho with Pratyush](https://www.youtube.com/watch?v=ahaLgJr3HcU&list=PLW4OpyGE0RdY)
- **Python Documentation:** https://docs.python.org/3/
- **Groq Documentation:** https://console.groq.com/docs
- **OpenAI Documentation:** https://platform.openai.com/docs
- **LangChain Documentation:** https://python.langchain.com/docs/
- **LangGraph Documentation:** https://docs.langchain.com/oss/python/langgraph/overview
- **Qdrant Documentation:** https://qdrant.tech/documentation/
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **MCP Documentation:** https://modelcontextprotocol.io/

---

## 💡 My Learning Approach

I believe in learning by building rather than only watching tutorials.

1. Understand the concept.
2. Implement it using Python.
3. Experiment with different approaches.
4. Build practical applications.
5. Document my learning in this repository.
6. Improve the implementation and learn from mistakes.

---

## 🎯 Final Goal

My goal is to become a skilled **AI Engineer** who can build intelligent applications using LLMs, RAG, AI Agents, Vector Databases, and modern AI frameworks.

This repository represents my continuous learning, experimentation, and practical implementation.

---

## 👨‍💻 About Me

**Suman Ranjan**  
B.E. Computer Science | Chitkara University

- GitHub: [@SumnRanjan](https://github.com/SumnRanjan)
- LinkedIn: [Suman Ranjan](https://www.linkedin.com/in/suman-ranjan-12719338a/)

---

⭐ If you find this repository useful, feel free to explore it and follow my AI Engineering journey!

**Learning. Building. Experimenting. Growing. 🚀**