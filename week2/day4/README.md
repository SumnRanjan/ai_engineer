# LLM Streaming – Real-Time Response Generation

A Python project demonstrating **Streaming in Large Language Models (LLMs)** using the Groq API.

This project explores how an LLM can generate and deliver responses incrementally in chunks instead of waiting for the entire response to be generated.

Streaming improves the user experience by allowing applications to display AI-generated content in real time.

## Concepts Learned

- **LLM Streaming:** Receiving generated responses incrementally.
- **Non-Streaming vs Streaming:** Understanding the difference between complete responses and incremental responses.
- **Groq API Integration:** Connecting Python applications with an LLM.
- **Stream Parameter:** Enabling streaming using `stream=True`.
- **Chunk Processing:** Iterating through response chunks.
- **Delta Content:** Extracting newly generated text from each chunk.
- **Flush:** Displaying output immediately in the terminal.

## Tech Stack

- Python
- Groq API
- OpenAI GPT-OSS 120B
- python-dotenv

## How Streaming Works

Normally, an LLM generates a complete response before returning it to the application.

With streaming, the model sends response chunks progressively while generation is still happening.

### Streaming Workflow

```text
       User Prompt
            |
            v
       Groq API Request
            |
            v
       LLM Processes Prompt
            |
            v
       Generates Response
            |
            v
     Streams Response Chunks
            |
            v
       Python Receives Chunks
            |
            v
     Displays Output Immediately
            |
            v
       Complete Response
```

## Implementation

### 1. Initialize Groq Client

Load the API key from environment variables and initialize the Groq client.

```python
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API KEY NOT FOUND")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
```

### 2. Prepare the Prompt

```python
prompt = "Explain how internet works."

message = {
    "role": "user",
    "content": prompt
}

messages = [message]
```

### 3. Enable Streaming

Set `stream=True` when creating the chat completion request.

```python
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True
)
```

### 4. Process Streaming Chunks

Iterate over the incoming chunks and extract the generated text.

```python
for chunk in stream:

    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
```

## Important Parameters

| Parameter | Purpose |
|---|---|
| `stream=True` | Enables incremental response delivery. |
| `chunk` | Represents an incoming response chunk. |
| `delta.content` | Contains newly generated text in a chunk. |
| `end=""` | Prevents adding a newline after every chunk. |
| `flush=True` | Displays buffered output immediately. |

## Streaming vs Non-Streaming

| Feature | Non-Streaming | Streaming |
|---|---|---|
| Response delivery | Complete response | Incremental chunks |
| User experience | Waits for completion | Sees output progressively |
| API parameter | `stream=False` (default) | `stream=True` |
| Processing | Single response | Iteration over chunks |
| Best suited for | Simple API requests | Interactive AI applications |

## Use Cases

- AI chatbots
- Real-time AI assistants
- AI coding assistants
- Content generation applications
- Interactive customer support systems
- AI-powered writing tools

## Project Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-folder>
```

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

This project helped me understand how LLM streaming works and how to implement real-time response generation using Python and the Groq API.

I learned how `stream=True` allows an application to receive generated content incrementally and how to process individual chunks using a Python loop.

**Important:** Streaming improves perceived responsiveness and reduces the time before the first output appears, but it does not necessarily reduce the total time required to generate a response.

## Learning Journey

**AI Engineering**

Learning by building practical AI applications and exploring LLM concepts with Python and Groq.