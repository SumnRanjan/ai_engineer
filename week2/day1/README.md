# Prompt Engineering – Customer Complaint Classification

A beginner-friendly Prompt Engineering project built using **Python, Groq API, and Large Language Models (LLMs)**.

This project demonstrates how to design structured prompts to guide an LLM to classify customer complaints into predefined categories. It explores how different prompt components influence the model's responses and help produce consistent, controlled outputs.

## Learning Objectives

- Understand the fundamentals of Prompt Engineering.
- Learn how to structure effective prompts.
- Understand how to assign roles to an LLM.
- Define clear tasks and constraints.
- Control model responses using output formatting instructions.
- Use examples to guide model behaviour (Few-shot Prompting).
- Handle unrelated inputs using fallback instructions.
- Integrate an LLM into a Python application using the Groq API.

## Prompt Engineering Concepts Covered

| Concept | Implementation |
|---|---|
| Role Prompting | Assigning the model the role of a customer support assistant |
| Task Definition | Asking the model to classify customer complaints |
| Constraints | Restricting classification to predefined categories |
| Output Formatting | Instructing the model to return only one word |
| Example-based Prompting | Providing an example of a refund complaint |
| Fallback Instructions | Returning `OTHER` for unrelated complaints |

## Classification Categories

The LLM is instructed to classify complaints into four categories:

- **BILLING** – Payment-related issues.
- **TECHNICAL** – Hardware or software-related issues.
- **RETURN** – Product returns and refund requests.
- **OTHER** – Issues unrelated to the specified categories.

## Example

**Input:**
```text
My marriage is broke
```

**Expected Output:**
```text
OTHER
```

The complaint is unrelated to mobile or laptop customer support, so the model should return `OTHER`.

## Tech Stack

- Python
- Groq API
- OpenAI GPT-OSS 120B
- python-dotenv

## Project Structure

```text
prompt-engineering/
│
├── main.py
├── .env
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd prompt-engineering
```

### 2. Create a Virtual Environment

```bash
uv venv
```

Activate the environment:

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
uv add groq python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

### 5. Run the Application

```bash
python main.py
```

## Key Takeaway

This project helped me understand that **Prompt Engineering is not just about asking questions to an LLM; it is about providing clear instructions, defining boundaries, and controlling the expected output.**

It is an initial step in my journey toward becoming an AI Engineer.

---
