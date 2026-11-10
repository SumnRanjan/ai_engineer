# ReAct AI Agent – Reasoning and Tool Calling

A basic AI Agent built using Python and Groq API that demonstrates the **ReAct (Reason + Act) architecture**. The agent uses an LLM to reason about user queries, select appropriate tools, execute Python functions, observe their outputs, and generate a final response.

## Concepts Learned

- **ReAct Architecture:** Combining reasoning and actions to solve tasks.
- **LLM Integration:** Connecting Python applications with Groq API.
- **System Prompts:** Defining agent behaviour and tool usage instructions.
- **Tool Calling:** Allowing an LLM to interact with external Python functions.
- **Tool Registry:** Managing available tools using a Python dictionary.
- **Action and Observation:** Executing tools and returning their results to the LLM.
- **Conversation Memory:** Maintaining conversation history using messages.
- **Agent Loop:** Repeatedly reasoning and executing tools until the task is complete.

## Tech Stack

- Python
- Groq API
- OpenAI GPT-OSS 120B
- python-dotenv
- Regular Expressions (`re`)

## Available Tools

The agent currently has two tools:

| Tool | Description |
|---|---|
| `get_product_price()` | Retrieves simulated product prices. |
| `calculator()` | Performs mathematical calculations. |

## How ReAct Works

The agent follows a continuous Reason–Act–Observe cycle:

1. **Thought:** The LLM determines what needs to be done.
2. **Action:** The LLM selects a tool and provides its argument.
3. **Observation:** Python executes the selected tool and returns the result.
4. **Repeat:** The LLM uses the observation to decide the next action.
5. **Final Answer:** The agent provides the completed response.

## Example

**User Prompt:**

"I have 5000 rupees. What is the price of an iPhone 17, and how much money will I have left?"

**Agent Execution:**

```text
Action: get_product_price("iPhone 17")
Observation: 1000

Action: calculator("5000 - 1000")
Observation: 4000
```

**Final Answer:**

```text
iPhone 17 Price: ₹1,000
Remaining Balance: ₹4,000
```

*Note: Product prices are hardcoded demonstration values.*

## Project Setup

### 2. Create a virtual environment

```bash
uv venv
```

### 3. Activate the environment (Windows)

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
uv add groq python-dotenv
```

### 5. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your API key to GitHub.

### 6. Run the application

```bash
python main.py
```

## Key Takeaway

This project helped me understand how an LLM can go beyond generating text and interact with external tools to complete tasks.

I learned the fundamentals of AI Agent architecture, including reasoning, tool execution, observations, and iterative decision-making using the ReAct pattern.
