# Customer Ticket Information Extractor

A beginner-friendly AI engineering project using **Python, Groq,
Pydantic, and JSON** to extract structured information from an
unstructured customer support ticket.

## Overview

A customer may describe a problem in plain language. This project sends
that text to a Large Language Model (LLM), asks it to extract selected
fields, and returns the result as JSON.

The extracted fields are: - Customer name - Email address - Issue
description

Python parses the JSON response and Pydantic validates it against the
`Ticket` model.

## Technologies Used

-   **Python** --- application logic
-   **Groq API** --- sends prompts to the LLM
-   **GPT-OSS-120B** --- model used for extraction
-   **Pydantic** --- defines and validates the expected data structure
-   **python-dotenv** --- loads the API key from a `.env` file
-   **JSON** --- represents the extracted information

## Project Workflow

1.  Load the Groq API key from the environment.
2.  Define a Pydantic model for the expected ticket fields.
3.  Generate a JSON Schema from the Pydantic model.
4.  Create a system message containing extraction instructions and the
    schema.
5.  Add the customer ticket as a user message.
6.  Send both messages to the Groq Chat Completions API in JSON mode.
7.  Read the model's response.
8.  Parse the JSON string into a Python dictionary.
9.  Validate the dictionary using Pydantic.
10. Access the validated fields.

``` text
Customer ticket (plain text)
          |
          v
Python prompt + system instructions
          |
          v
Groq API / GPT-OSS-120B
          |
          v
JSON response (string)
          |
          v
json.loads()
          |
          v
Python dictionary
          |
          v
Pydantic Ticket validation
          |
          v
Validated ticket fields
```

## Project Structure

``` text
day4/
├── .venv/
├── .env
├── .gitignore
├── json_pydantic.py
└── README.md
```

## Setup

### 1. Create and activate a virtual environment

On Windows PowerShell:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

``` powershell
python -m pip install groq pydantic python-dotenv
```

### 3. Add your Groq API key

Create a `.env` file in the project directory:

``` env
GROQ_API_KEY=your_groq_api_key_here
```

Keep this key private. Do not commit `.env` to Git.

### 4. Add a `.gitignore` file

``` gitignore
.venv/
.env
__pycache__/
*.pyc
```

## Implementation

Save the following code as `json_pydantic.py`:

``` python
import os
import json

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel


# 1. Load environment variables
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# 2. Initialize Groq client
client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"


# 3. Define the expected output structure
class Ticket(BaseModel):
    name: str
    email: str
    issue: str


# 4. Generate JSON Schema from the Pydantic model
schema = Ticket.model_json_schema()

# 5. Request JSON-formatted output
response_format = {
    "type": "json_object"
}

# 6. Define the system instructions
system_prompt = f"""
Extract the following information from the customer ticket:
- name
- email
- issue

Return a JSON object that follows this schema:

{json.dumps(schema, indent=2)}

If a field is missing, return an empty string for that field.
Do not invent information.
"""

system_message = {
    "role": "system",
    "content": system_prompt
}


# 7. Customer ticket
text = """
Hello, my name is Suman Ranjan.
I have an iPhone which is not working at all.
My address is Deoghar, Jharkhand.
My email is abc@gmail.com.
My contact number is 82134.
"""

prompt = f"""
This is a customer support ticket.
Extract the required information from it:

{text}
"""

user_message = {
    "role": "user",
    "content": prompt
}

messages = [system_message, user_message]


# 8. Send the request to Groq
response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format
)


# 9. Get the JSON response text
answer = response.choices[0].message.content

if answer is None:
    raise ValueError("The model returned an empty response.")

print("Raw JSON response:")
print(answer)


# 10. Parse JSON text into a Python dictionary
data = json.loads(answer)


# 11. Validate the dictionary with Pydantic
ticket = Ticket(**data)

# 12. Access the validated fields
print("\\nValidated ticket information:")
print("Name:", ticket.name)
print("Email:", ticket.email)
print("Issue:", ticket.issue)
```

## Important Concepts Learned

### 1. Pydantic `BaseModel`

``` python
class Ticket(BaseModel):
    name: str
    email: str
    issue: str
```

Defines the expected Python data structure. Pydantic checks that
supplied values satisfy the declared field types.

### 2. `model_json_schema()`

``` python
schema = Ticket.model_json_schema()
```

Converts the Pydantic model into a JSON Schema describing the expected
fields and their types.

### 3. Chat message roles

``` python
system_message = {
    "role": "system",
    "content": system_prompt
}

user_message = {
    "role": "user",
    "content": prompt
}
```

-   `system` provides instructions for the assistant.
-   `user` contains the customer ticket.
-   `content` contains the actual message text.

Use `content`, not `context`, in Chat Completions messages.

### 4. JSON Mode

``` python
response_format = {
    "type": "json_object"
}
```

Requests a valid JSON object from the model. JSON Mode does **not**
guarantee that every key and type matches the Pydantic schema. Local
Pydantic validation is still needed.

### 5. `json.loads()`

``` python
data = json.loads(answer)
```

The API returns JSON as text. `json.loads()` parses that text into a
Python dictionary.

For example:

``` python
raw_json = '{"name": "Suman Ranjan", "email": "abc@gmail.com", "issue": "iPhone not working"}'
data = json.loads(raw_json)
print(data["name"])
```

### 6. Pydantic validation

``` python
ticket = Ticket(**data)
```

The `**` operator unpacks dictionary key-value pairs as keyword
arguments. Pydantic validates the values and creates a `Ticket` object.

Access its fields with dot notation:

``` python
ticket.name
ticket.email
ticket.issue
```

You can also parse and validate JSON directly:

``` python
ticket = Ticket.model_validate_json(answer)
```

This combines JSON parsing and Pydantic validation in one step.

## JSON Mode vs. Structured Outputs

-   **JSON Mode** asks the model to return valid JSON.
-   **Structured Outputs** use a supported strict JSON Schema response
    format to constrain the output to a specified schema.
-   **Pydantic validation** checks the received data in your Python
    application.

This project uses JSON Mode followed by local Pydantic validation. It
does not use strict Structured Outputs.

## Run the Project

With the virtual environment activated:

``` powershell
python json_pydantic.py
```

The response should contain a JSON object similar to:

``` json
{
  "name": "Suman Ranjan",
  "email": "abc@gmail.com",
  "issue": "iPhone is not working at all"
}
```

The exact wording of the `issue` field may vary because it is generated
by the model.

## Key Takeaways

-   An LLM can extract information from unstructured text.
-   A prompt combines instructions with dynamic input.
-   Pydantic models define the structure expected by the application.
-   JSON Schema describes that structure.
-   JSON Mode requests JSON, but does not enforce the complete schema.
-   `json.loads()` converts JSON text into a Python dictionary.
-   Pydantic validates the data and provides a convenient Python object.
-   API keys should be stored in environment variables, never hardcoded
    or committed.

## Possible Improvements

-   Add `address` and `contact_number` fields to the `Ticket` model.
-   Validate email addresses using Pydantic's `EmailStr` type (install
    `email-validator`).
-   Handle malformed JSON and Pydantic validation errors.
-   Process multiple customer tickets.
-   Save validated ticket data to MongoDB or PostgreSQL.
-   Explore strict Structured Outputs and function calling.
