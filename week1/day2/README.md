# Day 2 – System Role & Temperature in LLMs

## Overview

On Day 2 of my AI Engineering learning journey, I explored two important concepts in Large Language Models (LLMs):

1. **System Role** – Defines the behaviour, personality, and instructions of an AI assistant.
2. **Temperature** – Controls the randomness and diversity of AI-generated responses.

I implemented these concepts using Python and the Groq API by building a simple AI-powered food brand name generator.

## Tech Stack

- Python
- Groq API
- GPT-OSS 120B
- Groq Python SDK
- python-dotenv

## Project Description

The objective of this project is to understand how system instructions and temperature influence LLM responses.

I created an AI application that suggests creative names for a food company.

The system role instructs the model to behave like a professional brand manager, while temperature controls the creativity and variation in the generated suggestions.

## Concepts Learned

### 1. System Role

The system role provides instructions that guide the AI's behaviour and response style.

Example:

```python
message_system = {
    "role": "system",
    "content": "You are a brand manager who suggests names for food brands."
}
```

**Why do we need it?**

Without a system role, the model responds based on the user prompt and its general instructions.

With a system role, we can guide the model to perform a specific task or adopt a particular professional perspective.

Examples:

- Python coding assistant
- Technical interviewer
- Customer support assistant
- Marketing strategist
- Food brand manager

### 2. User Role

The user role contains the actual question or instruction provided to the AI.

```python
message = {
    "role": "user",
    "content": "Suggest name for my food company"
}
```

The model uses this input along with the system instructions to generate a response.

### 3. Temperature

Temperature controls the randomness of token selection during text generation.

It influences how predictable or diverse the AI-generated responses can be.

General behaviour:

| Temperature | Behaviour |
|---|---|
| 0.0 | More predictable |
| 0.2 | Focused responses |
| 0.5 | Balanced responses |
| 0.7 | More variation |
| 1.0 | More creative and varied |
| 1.5 | Highly varied |
| 2.0 | Very experimental |

**Important:** Higher temperature does not necessarily mean better answers. It simply increases variation.

For creative tasks like brand naming, a higher temperature can be useful.

For tasks like data extraction and factual responses, a lower temperature is often preferable.

### 4. Messages Structure

The LLM receives messages as a list of dictionaries.

```python
messages = [
    message_system,
    message
]
```

Each message contains:

- `role`: Defines the message source.
- `content`: Contains the instructions or text.

Common roles:

| Role | Purpose |
|---|---|
| system | Defines assistant behaviour |
| user | Contains user input |
| assistant | Contains assistant responses |

## Implementation

### Complete Python Code

```python
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND")

# Initialize Groq client
client = Groq(api_key=my_api_key)

# Select LLM model
model = "openai/gpt-oss-120b"

# System role
message_system = {
    "role": "system",
    "content": "You are a brand manager who suggests names for food brands."
}

# User prompt
message = {
    "role": "user",
    "content": "Suggest name for my food company"
}

# Prepare conversation
messages = [message_system, message]

# Generate response
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1
)

# Extract AI response
answer = response.choices[0].message.content

print(answer)
```

## How It Works

The application follows this flow:

1. Load the API key from the `.env` file.
2. Initialize the Groq client.
3. Select the GPT-OSS 120B model.
4. Define a system role as a food brand manager.
5. Provide a user prompt requesting food company names.
6. Combine system and user messages.
7. Send the request with temperature set to 1.
8. Extract and display the AI-generated response.

## Project Structure

```text
day2/
│
├── .venv/
├── .env
├── .gitignore
├── main.py
└── README.md
```

## Key Learnings

Through this implementation, I learned:

- What system roles are and why they are important.
- How to define AI behaviour using system instructions.
- How user messages are passed to an LLM.
- How temperature affects response generation.
- How to combine multiple messages in a conversation.
- How to build a task-specific AI application using an LLM API.

## Future Improvements

- Generate multiple food brand names.
- Add different brand personalities.
- Allow users to control temperature dynamically.
- Generate brand taglines and descriptions.
- Build an interactive food brand name generator.

---

## Learning Progress

**Week 1 | Day 2 – Completed**

**Topics:** System Role, User Role, Messages Structure & Temperature.

*Learning AI Engineering one concept and one implementation at a time.*